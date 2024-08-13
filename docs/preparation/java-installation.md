---
title: 安装 JDK
sidebar_position: 1
---

# 安装 JDK

Java 开发工具包（JDK）是开发插件所必需的。以下是安装 JDK 的详细步骤：

## Windows 系统

1. **下载 JDK：**

- 访问 [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) 或 [OpenJDK](https://adoptium.net/zh-CN/temurin/releases/)。（我们更推荐使用 [Zulu JDK](https://www.azul.com/downloads/)，他有着更好的优化以及更少的内存占用）

- 选择适合 Windows 系统和版本的 JDK 进行下载，但请确保下载与服务器兼容的版本。

| 游戏版本 | 推荐 JDK 版本 |
|--|--|
| 1.16 之前 | JDK 8 |
| 1.16 - 1.16.5 | JDK 16 |
| 1.17 - 1.20.4 | JDK 17 |
| 1.20.5 - 1.21 及之后 | JDK 21 |

2. **安装 JDK：**

- 运行下载的安装程序，按照安装向导的提示进行安装。

- 在安装过程中，建议选择默认的安装路径（例如 `C:\Program Files\Java\jdk-xx`）。

3. **配置环境变量：**

- 打开 "控制面板" > "系统和安全" > "系统" > "高级系统设置"。

- 在 "系统属性" 窗口中，点击 "环境变量"。

- 在 "系统变量" 部分，找到名为 `Path` 的变量，选择它并点击 "编辑"。

- 添加 JDK 的 `bin` 目录路径，例如 `C:\Program Files\Java\jdk-xx\bin`。点击 "确定" 保存更改。

- 创建或修改 `JAVA_HOME` 变量：

    - 在 "系统变量" 部分，点击 "新建"。

    - 变量名输入 `JAVA_HOME`，变量值输入 JDK 安装路径，例如 `C:\Program Files\Java\jdk-xx`。

    - 点击 "确定" 保存更改。

4. **验证安装：**

- 打开命令提示符（按 `Win + R`，输入 `cmd`，然后按 `Enter`）。

- 输入 `java -version`，检查 JDK 是否正确安装。如果显示 JDK 的版本信息，则安装成功。

## macOS 系统

1. **下载 JDK：**

- 访问 [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) 或 [OpenJDK](https://adoptium.net/zh-CN/temurin/releases/)。（我们更推荐使用 [Zulu JDK](https://www.azul.com/downloads/)，他有着更好的优化以及更少的内存占用）

- 选择适合 macOS 系统和版本的 JDK 进行下载，但请确保下载与服务器兼容的版本。

2. **安装 JDK：**

- 双击下载的 `.dmg` 文件，打开安装程序。

- 按照安装向导的提示完成 JDK 的安装。

3. **配置环境变量：**

- macOS 通常会自动配置环境变量，但你可以手动检查或配置：

    - 打开终端（Terminal）。

    - 输入 `nano ~/.bash_profile` 或 `nano ~/.zshrc`（取决于你使用的 shell），然后添加以下行：

    ```jsx title="bash"
    export JAVA_HOME=$(/usr/libexec/java_home)
    export PATH=$JAVA_HOME/bin:$PATH
    ```

    - 保存并关闭文件（`Ctrl + X`，然后 `Y` 和 `Enter`）。

    - 运行 `source ~/.bash_profile` 或 `source ~/.zshrc` 以使更改生效。

4. **验证安装：**

- 打开终端（Terminal）。

- 输入 `java -version`，检查 JDK 是否正确安装。如果显示 JDK 的版本信息，则安装成功。

## Linux 系统

1. **安装 JDK：**

- 对于基于 Debian 的系统（如 Ubuntu），可以使用以下命令：

```jsx title="bash"
sudo apt update
sudo apt install openjdk-21-jdk
```

- 对于基于 Red Hat 的系统（如 Fedora），可以使用以下命令：

```jsx title="bash"
sudo dnf install java-21-openjdk
```

- 对于其他 Linux 发行版，请参考相应的包管理器文档进行安装。

2. **配置环境变量：**

- 打开终端。

- 编辑你的 shell 配置文件（例如 `~/.bashrc` 或 `~/.zshrc`）：

```jsx title="bash"
nano ~/.bashrc
```

- 添加以下行：
```jsx title="bash"
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export PATH=$JAVA_HOME/bin:$PATH
```

- 保存并关闭文件（`Ctrl + X`，然后 `Y` 和 `Enter`）。

- 运行 `source ~/.bashrc` 或 `source ~/.zshrc` 以使更改生效。

3. **验证安装：**

- 打开终端。
- 输入 `java -version`，检查 JDK 是否正确安装。如果显示 JDK 的版本信息，则安装成功。
