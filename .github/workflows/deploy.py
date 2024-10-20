import asyncio
import os
import paramiko
import io
import zipfile
import hashlib


async def remove_remote_files(sftp, remote_dir):
    """删除给定远程目录中的所有文件。"""
    for entry in sftp.listdir(remote_dir):
        remote_path = os.path.join(remote_dir, entry)
        if sftp.stat(remote_path).st_mode & 0o40000:  # 检查是否为目录
            await remove_remote_files(sftp, remote_path)
            sftp.rmdir(remote_path)  # 删除目录
        else:
            sftp.remove(remote_path)  # 删除文件
    print(f"已清除远程目录: {remote_dir}")


def md5_for_file(file_path):
    """计算给定文件的MD5校验和。"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


async def synchronize_files(local_dir, remote_dir, server_ip, server_port, private_key):
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 使用私钥连接到远程服务器
    private_key_obj = paramiko.RSAKey(file_obj=private_key)
    try:
        client.connect(
            server_ip, port=server_port, username="root", pkey=private_key_obj
        )
        sftp = client.open_sftp()

        # 确保远程目录存在
        try:
            sftp.stat(remote_dir)
        except FileNotFoundError:
            sftp.mkdir(remote_dir)

        # 删除远程目录中的现有文件
        await remove_remote_files(sftp, remote_dir)

        # 压缩本地目录
        zip_file_path = f"{local_dir}.zip"
        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(local_dir):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    zipf.write(
                        local_file_path, os.path.relpath(local_file_path, local_dir)
                    )

        # 上传压缩包
        remote_zip_file_path = os.path.join(remote_dir, os.path.basename(zip_file_path))
        print(f"正在上传压缩包: {zip_file_path} 到 {remote_zip_file_path}")
        sftp.put(zip_file_path, remote_zip_file_path)

        # 在远程服务器上解压缩文件
        unzip_command = f"unzip -o {remote_zip_file_path} -d {remote_dir}"
        stdin, stdout, stderr = client.exec_command(unzip_command)
        print(stdout.read().decode())
        print(stderr.read().decode())

        # 验证每个文件的MD5校验和
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                local_file_path = os.path.join(root, file)
                local_md5 = md5_for_file(local_file_path)

                remote_file_path = os.path.join(
                    remote_dir, os.path.relpath(local_file_path, local_dir)
                )
                md5_command = f"md5sum {remote_file_path} | cut -d ' ' -f 1"
                stdin, stdout, stderr = client.exec_command(md5_command)
                remote_md5 = stdout.read().decode().strip()

                if local_md5 == remote_md5:
                    print(f"MD5校验成功: {remote_file_path}")
                else:
                    print(f"MD5不匹配: {remote_file_path}")

        # 清理
        os.remove(zip_file_path)  # 删除本地压缩包
        sftp.close()
        print("文件同步完成！")

    except Exception as e:
        print(f"连接错误: {e}")
    finally:
        client.close()


async def main():
    # 打印脚本的绝对目录
    current_directory = os.path.abspath(os.getcwd())
    print(f"当前脚本绝对目录：{current_directory}")

    # 从环境变量获取参数
    local_dir = os.getenv("LOCAL_DIR")
    remote_dir = os.getenv("REMOTE_DIR")
    server_ip = os.getenv("SERVER_IP")
    server_port = int(os.getenv("SERVER_PORT", 22))  # 默认端口22
    private_key_str = os.getenv("PRIVATE_KEY")  # 获取私钥字符串

    # 将私钥字符串转换为文件对象
    private_key = io.StringIO(private_key_str)

    await synchronize_files(local_dir, remote_dir, server_ip, server_port, private_key)


if __name__ == "__main__":
    asyncio.run(main())
