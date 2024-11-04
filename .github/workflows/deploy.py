import argparse
import asyncio
import os
import paramiko
import io
import zipfile
import hashlib
import logging
import aiofiles
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 设置日志记录
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def remove_remote_files(sftp, remote_dir):
    """删除给定远程目录中的所有文件和文件夹。"""
    try:
        # 获取远程目录中所有条目
        entries = sftp.listdir(remote_dir)

        for entry in entries:
            remote_path = os.path.join(remote_dir, entry)
            try:
                if sftp.stat(remote_path).st_mode & 0o40000:  # 检查是否为目录
                    await remove_remote_files(sftp, remote_path)  # 递归删除目录内容
                    sftp.rmdir(remote_path)  # 删除空目录
                else:
                    sftp.remove(remote_path)  # 删除文件
            except Exception as e:
                logging.warning(f"删除 {remote_path} 时出错: {e}")

        logging.info(f"已清除远程目录: {remote_dir}")
    except Exception as e:
        logging.error(f"清除远程目录时出错: {e}")


async def checksum_for_file(file_path, algo="md5"):
    """异步计算给定文件的校验和。"""
    hash_obj = hashlib.md5() if algo == "md5" else hashlib.sha256()
    async with aiofiles.open(file_path, "rb") as f:
        while True:
            chunk = await f.read(4096)
            if not chunk:
                break
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


async def execute_command_async(client, command):
    """异步执行远程命令并返回输出。"""
    loop = asyncio.get_event_loop()
    stdin, stdout, stderr = await loop.run_in_executor(
        None, lambda: client.exec_command(command)
    )
    stdout_data = await loop.run_in_executor(None, stdout.read)
    stderr_data = await loop.run_in_executor(None, stderr.read)
    return stdin, stdout_data.decode(), stderr_data.decode()


async def verify_files_checksums(local_dir, remote_dir, client):
    """验证本地和远程文件的MD5和SHA校验和。"""
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_file_path = os.path.join(root, file)
            local_md5 = await checksum_for_file(local_file_path, "md5")
            local_sha = await checksum_for_file(local_file_path, "sha256")

            remote_file_path = os.path.join(
                remote_dir, os.path.relpath(local_file_path, local_dir)
            )
            md5_command = f"md5sum {remote_file_path} | cut -d ' ' -f 1"
            sha_command = f"sha256sum {remote_file_path} | cut -d ' ' -f 1"

            # 异步执行MD5命令
            stdin, stdout, stderr = await execute_command_async(client, md5_command)
            remote_md5 = stdout.strip()

            # 异步执行SHA命令
            stdin, stdout, stderr = await execute_command_async(client, sha_command)
            remote_sha = stdout.strip()

            if local_md5 == remote_md5 and local_sha == remote_sha:
                logging.info(f"校验成功: {remote_file_path}")
            else:
                logging.warning(f"校验不匹配: {remote_file_path}，正在重新上传...")
                return False  # 返回 False，表示校验不匹配

    return True  # 所有文件校验成功


async def synchronize_files(
    local_dir,
    remote_dir,
    server_ip,
    server_port,
    username,
    private_key,
    delete_old_files,
):
    """同步本地目录到远程目录。"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    private_key_obj = paramiko.RSAKey(file_obj=private_key)
    try:
        client.connect(
            server_ip, port=server_port, username=username, pkey=private_key_obj
        )

        sftp = client.open_sftp()  # 使用同步方式打开 SFTP 连接
        try:
            # 确保远程目录存在
            try:
                sftp.stat(remote_dir)
            except FileNotFoundError:
                sftp.mkdir(remote_dir)

            if delete_old_files:
                # 删除远程目录中的现有文件和文件夹
                await remove_remote_files(sftp, remote_dir)

            # 压缩本地目录
            zip_file_path = f"{local_dir}.zip"
            await compress_directory(local_dir, zip_file_path)

            # 上传压缩包
            remote_zip_file_path = os.path.join(
                remote_dir, os.path.basename(zip_file_path)
            )
            logging.info(f"正在上传压缩包: {zip_file_path} 到 {remote_zip_file_path}")
            sftp.put(zip_file_path, remote_zip_file_path)

            # 在远程服务器上解压缩文件
            await execute_command_async(
                client, f"unzip -o {remote_zip_file_path} -d {remote_dir}"
            )

            # 验证每个文件的MD5和SHA校验和
            checksums_match = await verify_files_checksums(
                local_dir, remote_dir, client
            )

            if checksums_match:
                logging.info("文件同步完成！")
            else:
                logging.info("重新上传文件...")

            # 清理
            os.remove(zip_file_path)  # 删除本地压缩包

        finally:
            sftp.close()  # 确保关闭 SFTP 连接

    except Exception as e:
        logging.error(f"连接错误: {e}")
    finally:
        client.close()


async def compress_directory(local_dir, zip_file_path):
    """压缩指定的本地目录。"""
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                local_file_path = os.path.join(root, file)
                zipf.write(local_file_path, os.path.relpath(local_file_path, local_dir))
    logging.info(f"已压缩目录: {local_dir} 到 {zip_file_path}")


async def main():
    """主函数，运行整个同步过程。"""
    parser = argparse.ArgumentParser(description="同步本地文件到远程服务器")
    parser.add_argument("-d", action="store_true", help="删除远程目录中的所有文件")
    args = parser.parse_args()

    current_directory = os.path.abspath(os.getcwd())
    logging.info(f"当前脚本绝对目录：{current_directory}")

    # 从环境变量获取参数
    local_dir = os.getenv("LOCAL_DIR")
    remote_dir = os.getenv("REMOTE_DIR")
    server_ip = os.getenv("SERVER_IP")
    server_port = int(os.getenv("SERVER_PORT", 22))  # 默认端口22
    username = os.getenv("REMOTE_USER", "root")  # 获取远程服务器用户名
    private_key_str = os.getenv("PRIVATE_KEY")  # 获取私钥字符串

    # 将私钥字符串转换为文件对象
    private_key = io.StringIO(private_key_str)

    await synchronize_files(
        local_dir,
        remote_dir,
        server_ip,
        server_port,
        username,
        private_key,
        delete_old_files=args.d,  # 根据命令行参数传递删除选项
    )


if __name__ == "__main__":
    asyncio.run(main())
