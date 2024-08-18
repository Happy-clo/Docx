---
title: 代码中的 MC 世界
sidebar_position: 2
---

如果你玩过《Minecraft》(简称 MC)，那么你可能想象过将 MC 代码化是怎样的体验。特别是如果你有 Java 开发经验，那么你可能对 JavaDoc 有所了解，而 SpigotMC 官方提供了与 MC 开发相关的 JavaDoc 文档。

**链接：**

- 最新版本 JavaDoc 网址: [点击这里](https://hub.spigotmc.org/javadocs/spigot/)
- 旧版本 JavaDoc 网址 (1.7.10): [点击这里](http://jd.bukkit.org/)
- 中文 JavaDoc 网址: [点击这里](https://bukkit.windit.net/javadoc/)
- 中文 JavaDoc GitHub 地址: [点击这里](https://github.com/BukkitAPI-Translation-Group/Chinese_BukkitAPI)

本章将大致按照 JavaDoc 上的包分类，介绍 BukkitAPI 所提供的各种系统与功能。

## 世界、方块与材质 (Material) 🗺️

在 MC 中，一个完整的世界并不会存储在单一的文件中。事实上，世界是由多个“区块”(Chunk)组成的，每个区块的范围是 X 和 Z 坐标为 16x16 的区域。我们在开发时，将每个世界视为一个 `World` 对象，每个区块视为一个 `Chunk` 对象，而每个方块则是一个 `Block` 对象。

例如，如果我们想要操作世界中的某个方块，可以通过 `World` 对象的方法直接访问，而不需要手动查找对应的区块。  
此外，BukkitAPI 引入了“材质”(Material)的概念，比如一个石头方块的材质就是 `STONE`，如果一个物品的材质也是 `STONE`，那么这个物品就是玩家手中的石头。

**示例代码：**

```java
Block b = 方块;
b.setType(Material.STONE);
```

删除一个方块：

```java
b.setType(Material.AIR); // 设置为空气
```

### 特殊方块 🌟

一些方块具有特定的属性和功能，比如告示牌上可以显示文字。在 BukkitAPI 中，`Block` 类有许多子类，例如 `Sign` 表示一个告示牌对象。你可以修改告示牌上的文字：

```java
Block b = 你获取到的告示牌方块;
Sign s = (Sign) b; // 强制转换为 Sign 对象
s.setLine(0, "测试"); // 修改第一行文字为“测试”
```

### 方块子类 🔨

所有的方块子类都在 `org.bukkit.block` 包内，你可以通过 JavaDoc 查找所需的子类并查看它们的用法。Material 枚举量的具体内容也可以在 JavaDoc 中查到。

## 生物与位置对象 (Location) 🐑

### 生物 (Entities)

在 MC 中，所有的生物，例如羊、僵尸、甚至玩家，都是 `Entity` 类型的对象。甚至像被点燃的 TNT 也是一个实体 (`TNTPrimed` 对象)。与 `Block` 类类似，`Entity` 也有许多子类，其中最常见的是 `Player` 类，它代表在线玩家。

### 位置对象 (Location)

每一个坐标位置都可以由一个 `Location` 对象来表示。常见的实体对象是 `Entity` 的子类，因此它们都提供 `getLocation` 方法来获取其坐标位置。值得注意的是，通过 `getLocation` 获取到的是实体的脚部位置。如果你想要移动一个实体，Bukkit 提供了 `teleport` 方法，而不是直接修改位置。

**坐标运算：** `Location` 提供了 `add` (加) 和 `subtract` (减) 方法。

**两点间距离：** `Location` 提供了 `distance` 方法，可以计算两点间的距离。

## 物品 (Items) 🎒

玩家手中的物品被称为物品(Items)，它们的材质被称为 `Material`。有些物品的材质和对应的方块 `Material` 不一致，例如红石比较器物品的种类是 `Material.REDSTONE_COMPARATOR`，而放置后的方块种类又分为 `Material.REDSTONE_COMPARATOR_ON` (开启状态) 和 `Material.REDSTONE_COMPARATOR_OFF` (关闭状态)。

`ItemStack` 类表示一种物品堆叠方式，它包含了物品的种类（`Material`）和数量等信息。例如，玩家手中有三个苹果，这三个苹果实际上就是一个 `ItemStack`，它包含了种类(`Material.APPLE`)、数量（3）以及其他信息。

## 事件系统 (Event System) 🎉

### 事件的概念

事件指的是服务器里发生的事情，比如天气变化、玩家移动、方块破坏等等。事件分为可控事件和不可控事件，其区别在于是否可以取消（`setCancelled`）。例如，玩家退出服务器的事件是不可取消的，而玩家移动的事件是可取消的。

### 事件监听器 (Listener)

你可以通过编写事件监听器来监听事件，并在事件触发时执行代码。监听器类需要实现 `Listener` 接口，并在方法上添加 `@EventHandler` 注解。

**示例代码：**

```java
public class DemoListener implements Listener {
    @EventHandler
    public void onPlayerMove(PlayerMoveEvent e) {
        // 当玩家移动时触发此方法
    }
}
```

## 命令系统 (Command System) 💬

MC 中的命令是一种字符串，用于实现游戏中的高级功能。命令通常在聊天框内输入，并以斜杠 `/` 开头。你可以通过 BukkitAPI 解析这些命令，并根据输入参数执行不同的功能。

**示例代码：**

```java
if (args.length == 0) {
    // 玩家没有输入参数
} else if (args[0].equalsIgnoreCase("example")) {
    // 玩家输入了 /命令名 example
}
```

## 权限系统 (Permissions) 🔐

BukkitAPI 提供了一套权限系统，用于控制玩家是否可以执行某些操作。权限通常是一个字符串，例如 `plugin.command.use`，你可以通过 `Player` 类的 `hasPermission` 方法来检查玩家是否拥有某个权限。

## 配置 API (Configuration API) ⚙️

配置 API 允许你以文件形式存储和读取插件的配置数据。它支持 YAML 格式，非常适合存储配置信息。

## 交流系统 (Conversation API) 💬

虽然使用频率较低，但 Bukkit 提供了一个 `Conversation` API，用于实现与玩家的对话系统。例如，当玩家在商店购买物品时，可以通过对话的方式与插件交互。

## 背包系统 (Inventory) 🎒

`Inventory` 对象表示玩家背包或箱子中存放的所有物品。你可以通过 `Inventory` 对象操作背包或箱子内的物品。

## 服务器底层 (NMS & OBC) 🛠️

MC 的原版服务器部分在 `net.minecraft.server` 包内，称为 `NMS`，而 Bukkit 的底层实现部分在 `org.bukkit.craftbukkit` 包内，称为 `OBC`。在某些情况下，你可能需要手动操作这些底层代码来实现特定功能。

以上就是 BukkitAPI 的基本介绍，希望能帮助你更好地理解和使用它来开发 Minecraft 插件！🚀
