---
title: 安装服务器
sidebar_position: 2
---

要开发和测试插件，你需要一个服务器。以下是安装和配置服务器的步骤：

1. **下载服务端：** 访问 [GetBukkit](https://getbukkit.org/) 或 [PaperMC](https://papermc.io/downloads/paper) 等网站下载服务端（如 Spigot, Paper 等）。

2. **配置服务端：**

   - 创建一个新的文件夹用于存放服务器文件。

   - 将下载的服务器 JAR 文件放入该文件夹。

   - 在文件夹中创建一个新的文本文件（例如 `start.bat` 或 `start.sh`），用于启动服务器。内容如下（根据实际 JAR 文件名进行调整）：

   ```jsx title="bash"
   java -Xmx2G -Xms2G -jar server.jar nogui
   ```

3. **启动服务端：**

   - 双击运行用于启动服务器的文件。服务器将自动生成配置文件和插件文件夹。

   - 启动服务器后，文件夹中将生成 `eula.txt` 文件，打开并将 `eula=false` 修改为 `eula=true`，以接受最终用户许可协议。

   - 再次运行启动文件启动服务器。
