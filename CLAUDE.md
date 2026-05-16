# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库用途

本仓库是 **Claude Code Skill 集合**，目前包含一个 VisionMaster 脚本开发辅助技能（`visionmaster-scripthelper/`）。每个子目录对应一个 Skill，包含技能定义文件（`SKILL.md`）、代码示例和接口参考。

## 项目结构

```
zixuan_Agenthub/
└── visionmaster-scripthelper/
    ├── SKILL.md                    # 技能定义（触发规则、代码生成工作流、约束）
    ├── README.md                   # 快速上手
    ├── assets/find_msbuild.ps1     # 编译校验脚本（MSBuild 路径查找）
    ├── examples/                   # 代码生成资源
    │   ├── 01-basic-template.cs    # 基础生命周期模板
    │   ├── 02-canny-edge-detection.cs   # OpenCV 图像处理示例
    │   ├── 03-roi.cs               # ROI 网格分割示例
    │   ├── 04-trans-CAD-file.cs    # CAD 文件转换示例
    │   ├── interface-quickref.md   # 变量类型映射 + 接口速查
    │   └── code-patterns.md        # 12 种场景代码模式
    └── references/                 # VM 接口原始定义（只读权威来源）
        ├── Script.Interface.cs     # 遗留接口签名
        ├── Script.DataStruct.cs    # 数据结构字段
        └── Script.ExMethods.cs     # ImageData ↔ Mat/Bitmap 转换方法
```

## VisionMaster 脚本开发核心规则

> 这是本仓库最重要的约束，生成任何 VM 脚本代码时必须遵守。

### 直接赋值范式（v2.5.0）

所有变量读写**必须**使用直接赋值，**禁止**使用 Get/Set 遗留接口：

```csharp
int val = in0;          // 读标量
out0 = val * 2;         // 写标量
PointData[] pts = in0;  // 读复合类型
out0 = pts;             // 写复合类型
ImageData img = imgIn;  // 读图像
imgOut = img;           // 写图像
```

**唯一例外**：需要按字符串动态访问变量名时（如遍历全局变量列表）可使用 `GetIntValue` / `SetIntValue`。

### 类型映射规则

| VM 类型 | C# 类型 |
|---------|---------|
| INT / FLOAT / STRING / DOUBLE / BYTE | `int` / `float` / `string` / `double` / `byte[]` |
| IMAGE | `ImageData`（非数组） |
| POINT / ROIBOX / CIRCLE / RECT 等复合类型 | `PointData[]` / `RoiboxData[]` 等 `<Type>Data[]` 数组 |
| INT[] / FLOAT[] 等数组 | `int[]` / `float[]` 等 |

### 硬性约束

- 基于 **.NET Framework 4.6.1**，不得使用 4.6.1 之后的 API
- **绝对禁止**读取或搜索 VM 安装目录下的任何文件；所有 API 信息只能来自 `references/` 和 `examples/`
- 生成代码前必须先读取用户工作目录中的 `UserProperty.cs`（输入输出定义）和 `UserScript.cs`
- `UserProperty.cs` 只读，不可修改
- `ImageData` 直接赋值是引用传递；需要独立副本时须通过 `ImageDataToMat` → 处理 → `MatToImageData`

### 代码生成工作流

1. 读取 `UserProperty.cs` 和 `UserScript.cs`，建立变量映射表
2. 按照 `examples/interface-quickref.md` 确认类型映射
3. 在 `examples/code-patterns.md` 中匹配场景模式（12 种）
4. 组装代码：`Process()` 在上，辅助方法在下，每个方法加 XML 注释，删除结构化注释
5. 自校验后尝试运行 `./assets/find_msbuild.ps1` 编译验证；无法运行时进行静态审查并告知用户

### 按需查阅的参考文件

| 需求 | 必读文件 |
|------|---------|
| 类型映射 / 直接赋值 | `examples/interface-quickref.md` |
| ImageData ↔ Mat / Bitmap 转换 | `references/Script.ExMethods.cs` |
| 图像处理示例 | `examples/02-canny-edge-detection.cs` |
| ROI 处理 | `examples/03-roi.cs` + `references/Script.DataStruct.cs` |
| 数据结构字段名 | `references/Script.DataStruct.cs` |
| CAD 文件操作 | `examples/04-trans-CAD-file.cs` |
| 遗留接口签名（仅动态名场景） | `references/Script.Interface.cs` |

## 扩展新 Skill

在根目录新建子目录，结构参考 `visionmaster-scripthelper/`：必须包含 `SKILL.md`（技能定义）；可选包含 `references/`（权威 API 定义）和 `examples/`（示例与速查文档）。
