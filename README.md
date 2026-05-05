# VisionMaster 脚本开发技能

> 版本 2.5.0 · 直接赋值范式 · 作者 ChrisYang

本技能为 VisionMaster (VM) C# 脚本开发辅助能力——生成、修改、排查 VM 脚本，优先输出可直接使用的代码。

## 快速开始

1. **了解规则** → 阅读 [SKILL.md](SKILL.md) 中的类型映射规则和代码生成工作流
2. **找参考** → [examples/](examples/) 包含完整脚本示例、类型映射表、代码模式库

## 项目结构

```
vm-script-skill/
├── SKILL.md                 # 技能定义（v2.5.0，直接赋值范式）
├── README.md                # 本文件
├── assets/
│   └── find_msbuild.ps1     # MSBuild 查找脚本（编译校验用）
├── examples/                # 代码生成资源（示例 + 映射表 + 模式库）
│   ├── 01-basic-template.cs
│   ├── 02-canny-edge-detection.cs
│   ├── 03-roi.cs
│   ├── 04-trans-CAD-file.cs
│   ├── interface-quickref.md
│   ├── code-patterns.md
│   └── README.md
└── references/              # 原始接口定义（查接口签名和数据结构时使用）
    ├── Script.Interface.cs
    ├── Script.DataStruct.cs
    ├── Script.ExMethods.cs
    └── README.md
```

## 运行依赖

| 依赖           | 版本要求 | 说明                 |
| -------------- | -------- | -------------------- |
| .NET Framework | 4.6.1+   | VM 脚本运行时        |
| VisionMaster   | 4.4.x    | 目标平台             |
| Windows        | 10/11    | 操作系统             |
| Visual Studio  | 2019+    | 编译校验（可选）     |
| OpenCvSharp    | —        | 图像处理扩展（可选） |

## 核心范式

v2.5.0 起，变量读写一律使用**直接赋值**，不使用 Get/Set 遗留接口：

```csharp
int val = in0;              // 读取标量
out0 = val * 2;             // 写入标量
PointData[] pts = in0;      // 读取复合类型
out0 = pts;                 // 写入复合类型
ImageData img = imgIn;      // 读取图像
imgOut = img;               // 写入图像
```

Get/Set 遗留接口仅在需要动态变量名访问时才使用。

## 支持范围

| 场景             | 状态        |
| ---------------- | ----------- |
| 2D 脚本（标准）  | ✅ 已支持   |
| OpenCvSharp 集成 | ✅ 已支持   |
| 3D 脚本          | 🔲 待扩展   |
| 其他第三方库     | 🔲 按需扩展 |
