---
title: 安装和配置服务器
sidebar_position: 2
---

为了开发和测试插件，你需要一个服务器。下面是详细的安装和配置步骤：

### 1. 下载服务端

访问以下网站下载服务端（如 Spigot 或 Paper）：

- [GetBukkit](https://getbukkit.org/)
- [PaperMC](https://papermc.io/downloads/paper)

### 2. 配置服务端

1. **创建文件夹：** 在你的计算机上创建一个新的文件夹，用于存放服务器文件。

2. **放置 JAR 文件：** 将下载的服务器 JAR 文件（如 `server.jar`）放入刚刚创建的文件夹中。

3. **创建启动脚本：**

   - 在文件夹中创建一个新的文本文件，命名为 `start.bat`（Windows）或 `start.sh`（macOS/Linux）。
   - 将以下内容粘贴到文件中，并根据实际 JAR 文件名进行调整：

     ```bash
     java -Xmx2G -Xms2G -jar server.jar nogui
     ```

     > **提示：** `-Xmx2G` 和 `-Xms2G` 是设置最大和最小内存的参数，可以根据你计算机的实际内存进行调整。

### 3. 启动服务端

1. **运行启动文件：** 双击你创建的启动文件。此时，服务器会自动生成必要的配置文件和插件文件夹。

2. **接受 EULA：** 启动服务器后，会生成一个 `eula.txt` 文件。打开这个文件，将 `eula=false` 修改为 `eula=true`，以接受最终用户许可协议。

3. **重新启动服务器：** 再次运行启动文件，服务器将开始运行，并生成所需的配置文件和插件文件夹。
