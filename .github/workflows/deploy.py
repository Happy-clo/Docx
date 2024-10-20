import asyncio
import os
import paramiko


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


async def synchronize_files(local_dir, remote_dir, server_ip, server_port, private_key):
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 使用私钥字符串连接到远程服务器
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

        # 同步文件
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                local_file_path = os.path.join(root, file)
                remote_file_path = os.path.join(
                    remote_dir, os.path.relpath(local_file_path, local_dir)
                )
                remote_file_dir = os.path.dirname(remote_file_path)

                # 确保远程子目录存在
                try:
                    sftp.stat(remote_file_dir)
                except FileNotFoundError:
                    sftp.mkdir(remote_file_dir)

                # 上传文件
                print(f"正在上传文件: {local_file_path} 到 {remote_file_path}：")
                sftp.put(local_file_path, remote_file_path)

        sftp.close()
        print("文件同步完成！")

    except Exception as e:
        print(f"连接错误: {e}：")
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
    private_key_str = os.getenv("PRIVATE_KEY")  # 这里获取私钥字符串

    # 将私钥字符串转换为文件对象
    private_key = io.StringIO(private_key_str)

    await synchronize_files(local_dir, remote_dir, server_ip, server_port, private_key)


if __name__ == "__main__":
    asyncio.run(main())
