# VisionMaster 脚本开发技能

> 版本 2.8.0 · 双语言支持 · 作者 ChrisYang

本技能为 VisionMaster (VM) 脚本开发辅助能力，同时支持 **C#** 和 **Python** 脚本——生成、修改、排查 VM 脚本，优先输出可直接使用的代码。

## 快速开始

1. **了解规则** → 阅读 [SKILL.md](SKILL.md) — C# 和 Python 各有独立的约束规范与代码生成工作流
2. **查参考** → C#：[examples/csharp/](examples/csharp/)（示例 + 类型映射 + 代码模式库）；Python：[examples/python/](examples/python/)（模板示例）
3. **接口定义** → C#：[references/](references/)（接口签名 + 数据结构 + 转换方法）；Python：[references_py/](references_py/)（开发规则 + 数据结构 + IoHelper 运行时）

## 项目结构

```
vm-script-skill/
├── SKILL.md                 # 技能定义（v2.8.0，双语言约束规范）
├── README.md                # 本文件
├── assets/
│   └── find_msbuild.ps1     # MSBuild 查找脚本（编译校验用）
├── examples/                    # 代码生成资源（示例 + 映射表 + 模式库）
│   ├── README.md
│   ├── csharp/                  # C# 脚本示例与参考
│   │   ├── interface-quickref.md
│   │   ├── code-patterns.md
│   │   ├── 01-basic-template.cs
│   │   ├── 02-canny-edge-detection.cs
│   │   ├── 03-roi.cs
│   │   ├── 04-trans-CAD-file.cs
│   │   └── 05-stereo-depth-pointcloud.cs
│   └── python/                  # Python 脚本示例
│       └── 01-template.py
├── references/              # C# 原始接口定义（查接口签名和数据结构时使用）
│   ├── README.md
│   ├── Script.Interface.cs
│   ├── Script.DataStruct.cs
│   ├── Script.ExMethods.cs
│   └── ScriptCSharpRules.md
└── references_py/           # Python 脚本参考（开发规则 + 数据结构 + 运行时）
    ├── ScriptPythonRules.md
    ├── Script.pyDataStruct.py
    └── Script.ioHelper.py
```

## 运行依赖

| 依赖           | 版本要求 | 说明                     |
| -------------- | -------- | ------------------------ |
| VisionMaster   | 4.4.x    | 目标平台                 |
| .NET Framework | 4.6.1+   | C# 脚本运行时            |
| Python         | 3.7      | Python 脚本运行时        |
| Windows        | 10/11    | 操作系统                 |
| Visual Studio  | 2019+    | C# 编译校验（可选）      |
| OpenCvSharp    | —        | C# 图像处理扩展（可选）  |

## 核心范式

### C# — 直接赋值

变量读写一律使用**直接赋值**，不使用 Get/Set 遗留接口：

```csharp
int val = in0;              // 读取标量
out0 = val * 2;             // 写入标量
PointData[] pts = in0;      // 读取复合类型
out0 = pts;                 // 写入复合类型
ImageData img = imgIn;      // 读取图像
imgOut = img;               // 写入图像
```

> Get/Set 遗留接口仅限按字符串动态访问变量名时使用。

### Python — 先建列表再赋值

变量读写遵循**先建列表再赋值**模式，使用 `IoHelper` 框架；**输入变量一律按数组处理**（即使 VM 中声明为 `int` / `float` / `string`，脚本中也按 `int[]` / `float[]` / `str[]` 对待）：

```python
def Process(data) -> int:
    moduleVar = IoHelper(data, INIT_MODULE_VAR)
    try:
        matchPointX = moduleVar.in0    # 输入只读
        moduleVar.out0 = result        # 输出只写
    except BaseException as e:
        PrintMsg(e)
    return 0
```

> 禁止使用 `globalVar` 和 `localVar`，仅允许 `moduleVar`。

## 支持范围

| 场景              | 状态        |
| ----------------- | ----------- |
| C# 2D 脚本        | ✅ 已支持   |
| C# OpenCvSharp    | ✅ 已支持   |
| C# 3D 深度图/点云 | ✅ 已支持   |
| Python 脚本       | ✅ 已支持   |
| 其他第三方库      | 🔲 按需扩展 |
