---
name: visionmaster-scripthelper
description: "用户正在开发、修改或调试 VisionMaster 脚本（UserScript.cs / *.py），或询问 VM 变量类型映射、模块参数读写、全局变量、图像处理等 VM 脚本具体问题时触发。"
version: 2.8.0
author: ChrisYang
tags:
  - VisionMaster
  - 脚本开发
  - C# 编程
  - 数据处理
  - 图像处理
  - 模块参数
  - 全局变量
  - 调试输出
---

# VisionMaster 脚本开发技能

## 目标

帮助用户编写、修改、排查 VisionMaster 脚本；严格遵守 VM 接口约束，根据文件类型，输出可直接使用的 C# 代码，或者python代码。

## 触发范围

当用户在讨论以下内容时使用本 skill：

- 脚本，输入输出
- `UserScript` / `IProcessMethods` / `Script.Methods`
- 变量直接赋值 / 数组 / 图像 / ROI 等数据类型
- 模块参数、全局变量、模块间读写、调试输出

## 必须遵守

- **【最高优先级】绝对禁止搜索、读取、反编译 VM 安装目录下的任何文件**（包括但不限于 .cs, .xml, .dll, .txt, .config 等）。
- 所有 API 信息、数据类型用法、转换方法，必须且仅能从本 skill 的 `references/`、`examples/csharp/` 和 `examples/python/` 中获取。违反此规则将生成不可用的代码。
- 确认已有的输入输出定义和脚本逻辑，再结合用户需求进行下一步
- 判断用户要完成的脚本类型并做决策，如果无法判断则明确向用户提问：

  > **C# / csharp 脚本** → 参考 [CSharp代码约束规范](#csharp代码约束规范) 及 [ScriptCSharpRules.md](./references/ScriptCSharpRules.md)
  > **Python 脚本** → 参考 [python代码约束规范](#python代码约束规范) 及 [ScriptPythonRules.md](./references_py/ScriptPythonRules.md)

## CSharp代码约束规范

- **必须先读取** [ScriptCSharpRules.md](./references/ScriptCSharpRules.md) 作为脚本的主要指导（内含完整 6 步代码生成工作流：获取已有代码 → 分析需求 → 确认变量映射 → 强制查阅参考 → 组装代码 → 自校验）。
- 基于 .NET Framework 4.6.1；不得使用 C# 5.0 以后的语法。
- 首先尝试读取工作目录中的 `UserProperty.cs` 和 `UserScript.cs`；无法访问则要求用户提供。
- `UserProperty.cs` 为只读定义，不可更改。
- 变量读写一律使用直接赋值（如 `out0 = in0`）；Get/Set 遗留接口仅限按字符串动态访问变量名时使用。
- 仅在需要显式释放资源时才编写 `Dispose()`；`Mat` 用完须 Dispose，大对象用字段缓存避免每帧 new。
- 需要第三方库时，先分析 `*.csproj` 确认库存在；缺少则中断生成并提示用户。
- 需要的信息不在 `references/` 或 `examples/csharp/` 中时，中断生成并提示用户，不要臆造，不要外部搜索。
- 每次生成完毕后执行编译校验：先运行 `assets/find_msbuild.ps1` 定位 MSBuild，再执行 `msbuild *.csproj` 编译；无法运行时做静态审查并告知用户手动验证。
- 代码组织：`Process()` 在上，辅助方法在下；删除结构化注释，为每个方法添加 XML 注释。以逻辑简单清晰为首要目标。

## python代码约束规范

- **必须**先读取 [ScriptPythonRules.md](./references_py/ScriptPythonRules.md) 作为脚本的主要指导。
- 基于 Python 3.7 版本的语法规则进行代码编写。
- **【核心约束】类型映射强制规则**：输入变量在代码中**一律按数组处理**——即使 VM 中声明为 `int` / `float` / `string`，脚本中也必须按 `int[]` / `float[]` / `str[]` 对待。完整映射见 `dict_type` 字典（位于 [ScriptPythonRules.md](./references_py/ScriptPythonRules.md) 第 4 步）。
- 必须使用 `IoHelper` 框架（定义见 [Script.ioHelper.py](./references_py/Script.ioHelper.py)）管理变量生命周期；**业务代码中仅允许通过 `moduleVar` 读写变量**（模板中 `globalVar` / `localVar` 的初始化是框架惯例，业务逻辑不应使用它们）。
- 变量读写遵循「先建列表再赋值」模式：`matchPointX = moduleVar.in0`；输入变量只读，输出变量只写。
- 代码应当使用空格作为缩进，禁止使用 Tab 作为缩进。
- 代码基于模板使用 `try-except` 结构包裹，通过 `PrintMsg(e)` 打印异常信息。
- 需要的信息不在 `references_py/` 或 `examples/python/` 中时，中断生成并提示用户，不要臆造补全，不要尝试外部搜索。
- 编写完毕后，做一次全面检查再输出：缩进一致性（空格/Tab 不混用）、类型映射与 `dict_type` 一致、`try-except` 结构完整。

### Python 代码生成工作流摘要

> 完整五步工作流见 [ScriptPythonRules.md](./references_py/ScriptPythonRules.md)，此处为关键节点摘要：

1. **询问输入变量**：以 `in0,int;in1,float` 格式收集所有输入变量名和类型
2. **询问输出变量**：同上格式收集所有输出变量
3. **分析数据需求**：根据 `dict_type` 映射表确认类型，输入变量一律按数组处理
4. **确认需求**：自检变量映射，推测用户目的，确认后开始编写
5. **完成编写**：以模板为骨架填充业务逻辑，做一次全面检查（缩进、类型、异常处理）再输出

## 参考资料与注意事项

### 文件索引

| 文件                                                                 | 用途                              |
| -------------------------------------------------------------------- | --------------------------------- |
| [references/Script.Interface.cs](./references/Script.Interface.cs)   | 遗留接口签名原始定义              |
| [references/Script.DataStruct.cs](./references/Script.DataStruct.cs) | 数据结构字段定义                  |
| [references/Script.ExMethods.cs](./references/Script.ExMethods.cs)   | Mat / Bitmap ↔ ImageData 转换方法 |
| [references/ScriptCSharpRules.md](./references/ScriptCSharpRules.md) | C# 脚本开发规则、生命周期、变量映射、工作流与自校验 |
| [references_py/ScriptPythonRules.md](./references_py/ScriptPythonRules.md) | Python 脚本开发规则与工作流   |
| [references_py/Script.pyDataStruct.py](./references_py/Script.pyDataStruct.py) | Python 数据结构定义          |
| [references_py/Script.ioHelper.py](./references_py/Script.ioHelper.py) | Python IoHelper 运行时库         |
| [examples/csharp/interface-quickref.md](./examples/csharp/interface-quickref.md) | 变量类型映射 + 接口速查索引（C#）  |
| [examples/csharp/code-patterns.md](./examples/csharp/code-patterns.md)           | 代码模式库（14 种场景模板，C#）    |
| [examples/csharp/](./examples/csharp/)                                           | C# 完整脚本示例（01~05）           |
| [examples/python/](./examples/python/)                                           | Python 完整脚本示例                |



---

## 扩展范式

本 skill 采用**分层架构**，便于后续增量扩展。新增场景支持时，按以下范式操作：

### 扩展步骤

1. **references/** — 新增接口/数据结构的原始定义文件（如 `Script.3D.cs`）
2. **examples/csharp/** — 新增 C# 示例脚本 + 更新 `interface-quickref.md` 类型映射 + 更新 `code-patterns.md` 新增模式；**examples/python/** — 新增 Python 示例脚本
3. **SKILL.md** — 在本节记录扩展清单；如需修改“必须遵守”或“标准模板”，同步更新
4. **references_py/** - 新增python类型脚本的rules

### 扩展清单

| 场景                       | 状态        | 说明                                           |
| -------------------------- | ----------- | ---------------------------------------------- |
| 2D 脚本（标准）            | ✅ 已支持   | ScriptMethods + IProcessMethods                |
| 3D 深度图 / 点云提取       | ✅ 已支持   | StereoImageData + GetStereoImageValue，示例 05；注意：`PointCloudData` 结构体解析暂不支持 |
| OpenCvSharp 集成           | ✅ 已支持   | 示例 02 + 模式 4                               |
| System.Drawing.Bitmap 集成 | ✅ 已支持   | Script.ExMethods.cs + 模式 4b                  |
| 其他第三方库               | 🔲 按需扩展 | 新增 references + examples + 校验 .csproj      |

> 扩展时注意：references/ 放原始定义，examples/csharp/ 和 examples/python/ 放可运行示例和速查文档，SKILL.md 只放规则和链接，不重复详细内容。
