---
title: 创建你的第一个插件
sidebar_position: 1
---

现在，让我们开始创建你的第一个插件吧！

1. **创建项目：**

- 首先，打开 Intellij IDEA，在左侧选择"项目"，点击上方的"新建项目"，然后在弹出的新界面中，左侧的生成器选择"Minecraft"。

- 然后，你需要在右面设置插件必需的一些设置。

  - "Groups"选项改为"Plugin"，表示你要创建一个插件。

  - "Templates"选项改为"Spigot"，表示你要生成一个 Spigot 插件的模板。

  - "构建系统"建议选择"Gradle"，相对于 Maven 来说有着更好的性能与灵活性。

  - "JDK"选择安装好的 JDK，一般 IDEA 会自己识别到，直接选择即可。

- 最后，你就可以修改你插件的信息了！

  - 输入项目名称，例如 `MyFirstPlugin`，本节后面的例子都采用了这个。

  - 选择项目保存的位置，建议保存在一个方便打开的位置。

  - 选择我的世界的版本，初学可以直接使用最新版。

  - 修改你的"组 ID"，一般格式为 `com.xxx`，你也可以使用类似于 `me.xxx` 这样的 ID，其中 `xxx` 一般改为作者。

  - 展开"Optional Settings"（可选设置），你可以自己修改简介、作者、网站等设置，也可以留空。

- 完成后，点击"创建"，等待他安装 Gradle 并构建，直到它不再有后台任务为止。

2. **了解结构：**

这时候，你可以展开你的项目，它的结构应该是这样的（这里只放比较重要的文件）：

```jsx title="scss"
MyFirstPlugin
│
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── example/
│   │               └── myFirstPlugin/
│   │                   └── MyFirstPlugin.java
│   └── resources/
│       └── plugin.yml
│
└── build.gradle
```

    1. `src/main/java/`

        - **目录作用：** 这个目录存放所有 Java 源代码文件，是插件的主要开发目录。

        - **包结构：** 在 `java` 目录下，通常会创建一个遵循域名反转规则的包结构（如 `com.example.myfirstplugin`）。这种命名方式有助于避免命名冲突，并且是 Java 项目的最佳实践。

        - **主类文件：** `MyFirstPlugin.java` 是插件的主类文件，它通常继承自 `JavaPlugin`，并包含 `onEnable`、`onDisable` 等方法，用于定义插件在启用和禁用时的行为。

    2. `src/main/resources/`

        - **目录作用：** 这个目录存放资源文件，如插件配置文件和其他静态资源。所有放在此目录下的文件在编译时会自动打包到插件 JAR 文件中。

        - `plugin.yml` **文件：** 这是插件的描述文件，定义了插件的名称、版本、主类路径、API 版本、依赖关系等。这个文件是 Bukkit/Spigot 服务器识别和加载插件的关键配置文件。

    3. `build.gradle`

        - **文件作用：** `build.gradle` 是项目的配置文件，定义了项目的依赖、构建任务和插件配置。

3. **编写代码：**

在你的主类中，默认会有这些代码：

```jsx title="MyFirstPlugin.java"
package com.example.myFirstPlugin;

import org.bukkit.plugin.java.JavaPlugin;

public final class MyFirstPlugin extends JavaPlugin {

    @Override
    public void onEnable() {
        // Plugin startup logic

    }

    @Override
    public void onDisable() {
        // Plugin shutdown logic
    }
}
```

其中 `onEnable()` 与 `onDisable()` 方法用于在插件启用和禁用时执行特定的代码。

我们可以在 `onEnable()` 方法中添加这么一行代码来输出插件启用时的信息：

```jsx title="MyFirstPlugin.java"
@Override
public void onEnable() {
    getLogger().info("My First Plugin has been successfully enabled! YEAH!!!");
}
```

4. **构建插件：**

- 在右边的侧边栏中有一个大象的图标，鼠标指针停留在上面的时候会提示 Gradle，我们把它点开。

- 依次展开 `MyFirstPlugin`、`Tasks`、`build`，然后双击 `build`，这样就可以构建插件了。

- 构建完插件后，你的目录会多出一个 `build` 文件夹，它其中的 `libs` 文件夹中，会有一个名为 `MyFirstPlugin-1.0.0-SNAPSHOT.jar` 的文件，这就是我们构建出来的插件了。

5. **测试插件：**

- 把它放进我们服务端的 `plugins` 文件夹下，运行服务端

- 这时在服务端中应该可以看到这么一条信息，这代表着我们已经成功了：

```
[11:45:14 INFO]: [MyFirstPlugin] My First Plugin has been successfully enabled! YEAH!!!
```

> 这一节涵盖了插件开发的基础知识，包括插件的基本概念、创建第一个插件项目、插件的结构和重要文件，以及如何编译和测试插件。掌握这些内容将为你后续的插件开发奠定坚实的基础。
