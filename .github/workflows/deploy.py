import asyncio
import os
import paramiko
import io
import zipfile
import hashlib
import subprocess
import logging
import aiofiles

# 设置日志记录
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def remove_remote_files(sftp, remote_dir):
    """删除给定远程目录中的所有文件。"""
    for entry in sftp.listdir(remote_dir):
        remote_path = os.path.join(remote_dir, entry)
        if sftp.stat(remote_path).st_mode & 0o40000:  # 检查是否为目录
            await remove_remote_files(sftp, remote_path)
            sftp.rmdir(remote_path)  # 删除目录
        else:
            sftp.remove(remote_path)  # 删除文件
    logging.info(f"已清除远程目录: {remote_dir}")


async def md5_for_file(file_path):
    """异步计算给定文件的MD5校验和。"""
    hash_md5 = hashlib.md5()
    async with aiofiles.open(file_path, "rb") as f:
        while True:
            chunk = await f.read(4096)
            if not chunk:
                break
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def print_summary_system_info():
    """打印系统当前重要配置。"""
    logging.info("当前系统配置:")

    # 获取操作系统信息
    try:
        os_info = subprocess.check_output("cat /etc/os-release", text=True)
        logging.info(os_info.strip())
    except Exception as e:
        logging.error(f"获取操作系统信息失败: {e}")

    # 获取内核信息
    try:
        kernel_info = subprocess.check_output("uname -r", text=True).strip()
        logging.info(f"内核版本: {kernel_info}")
    except Exception as e:
        logging.error(f"获取内核信息失败: {e}")

    # 获取CPU信息
    try:
        cpu_info = subprocess.check_output(
            "lscpu | grep 'Model name'", text=True
        ).strip()
        logging.info(cpu_info)
    except Exception as e:
        logging.error(f"获取CPU信息失败: {e}")

    # 获取内存信息
    try:
        mem_info = subprocess.check_output(
            "free -h | awk 'NR==2{printf \"内存: %s (已用: %s, 可用: %s)\", \$2, \$3, \$7}'",
            text=True,
        )
        logging.info(mem_info)
    except Exception as e:
        logging.error(f"获取内存信息失败: {e}")

    # 获取磁盘使用情况
    try:
        disk_info = subprocess.check_output(
            "df -h / | awk 'NR==2{printf \"根分区: %s (已用: %s, 可用: %s)\", \$2, \$3, \$4}'",
            text=True,
        )
        logging.info(disk_info)
    except Exception as e:
        logging.error(f"获取磁盘信息失败: {e}")

    # 打印虚拟化信息
    try:
        virtualization_info = subprocess.check_output(
            "lscpu | grep 'Virtualization'", text=True
        ).strip()
        logging.info(virtualization_info)
    except Exception as e:
        logging.error(f"获取虚拟化信息失败: {e}")


async def test_network_speed():
    """测试本机当前网速。"""
    logging.info("正在测试网络速度...")
    result = subprocess.run(["speedtest-cli"], capture_output=True, text=True)
    logging.info(result.stdout)


async def synchronize_files(
    local_dir, remote_dir, server_ip, server_port, username, private_key
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

            # 删除远程目录中的现有文件
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
            await execute_command(
                client, f"unzip -o {remote_zip_file_path} -d {remote_dir}"
            )

            # 验证每个文件的MD5校验和
            await verify_files_md5(local_dir, remote_dir, client)

            # 清理
            os.remove(zip_file_path)  # 删除本地压缩包
            logging.info("文件同步完成！")

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


async def execute_command(client, command):
    """在远程服务器上执行命令并打印输出。"""
    stdin, stdout, stderr = client.exec_command(command)
    logging.info(stdout.read().decode())
    logging.error(stderr.read().decode())


async def verify_files_md5(local_dir, remote_dir, client):
    """验证本地和远程文件的MD5校验和。"""
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_file_path = os.path.join(root, file)
            local_md5 = await md5_for_file(local_file_path)  # 异步计算本地文件的MD5

            remote_file_path = os.path.join(
                remote_dir, os.path.relpath(local_file_path, local_dir)
            )
            md5_command = f"md5sum {remote_file_path} | cut -d ' ' -f 1"
            stdin, stdout, stderr = client.exec_command(md5_command)
            remote_md5 = stdout.read().decode().strip()

            if local_md5 == remote_md5:
                logging.info(f"MD5校验成功: {remote_file_path}")
            else:
                logging.warning(f"MD5不匹配: {remote_file_path}")


async def main():
    """主函数，运行整个同步过程。"""
    current_directory = os.path.abspath(os.getcwd())
    logging.info(f"当前脚本绝对目录：{current_directory}")

    print_summary_system_info()  # 打印系统重要信息
    await test_network_speed()  # 测试网络速度

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
        local_dir, remote_dir, server_ip, server_port, username, private_key
    )


if __name__ == "__main__":
    asyncio.run(main())
