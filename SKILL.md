---
name: vm-script-skill
description: "VisionMaster（VM）脚本开发辅助。用户提到：帮我编写脚本、写脚本，输入输出，图像处理，模块参数，全局变量，调试输出等相关内容时触发。优先输出可直接使用的 C# 代码。"
version: 2.2.1
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

帮助用户编写、修改、排查 VisionMaster 脚本；优先输出可直接使用的 C# 代码，并严格遵守 VM 接口约束。

## 触发范围

当用户在讨论以下内容时使用本 skill：

- 脚本，输入输出
- `UserScript` / `IProcessMethods` / `Script.Methods`
- 变量直接赋值 / 数组 / 图像 / ROI 等数据类型
- 模块参数、全局变量、模块间读写、调试输出

## 必须遵守

- 基于 .NET Framework 4.6.1，不得使用 4.6.1 之后引入的 API
- 首先查找工作目录中的 `UserProperty.cs` 和 `UserScript.cs`，`UserProperty.cs`文件是只读不可更改和编辑的。
- 确认已有的输入输出定义和脚本逻辑，再结合用户需求进行下一步。
- 代码组织：`Process()` 放在上方，辅助方法放在下方
- 生成代码时删除脚本结构化注释，给每一个方法添加 XML 注释
- **变量读写一律使用直接赋值方式**（如 `out0 = in0`），不要使用 Get/Set 遗留接口；仅当需要按变量名字符串动态访问时才使用遗留接口作为后备
- 仅在需要显式释放资源时才编写 `Dispose()`
- 以逻辑简单清晰为首要目标，不做过度优化，但基本的资源管理必须做（如 `Mat` 用完 Dispose、大对象用字段缓存避免每帧 new）
- 简单逻辑自行实现或调用 `references/` 下的方法；避免为简单逻辑引入不必要的第三方库
- 需要第三方库时，先分析 `*.csproj` 确认库存在；缺少则中断生成并提示用户
- 需要的信息不在 `references/` 中时，中断生成并提示用户，不要臆造
- 只能查看 skill 内的文件和当前路径下的文件，不能访问其他路径的文件
- 每次脚本生成完毕后，都要尝试调用 `./assets/find_msbuild.ps1` 来编译校验；有报错则根据信息修正，直到编译通过

## 明确不支持

遇到以下请求时，直接说明不支持，避免继续展开：

- 控制器 IO 发送
- 界面层操作 / UI 自动化
- 非托管资源的外部封装方案
- 通讯协议解析

如用户需要上述能力，可建议改用外部程序、上位机或其他 SDK 方案。

## 生命周期

| 方法        | 修饰                  | 触发时机              | 用途                                     |
| ----------- | --------------------- | --------------------- | ---------------------------------------- |
| `Init()`    | `public void`         | 加载方案 / 预编译时   | 初始化变量、创建句柄、加载资源           |
| `Process()` | `public bool`         | 每次流程执行          | 业务逻辑、数据处理；返回 `true` 表示成功 |
| `Dispose()` | `public virtual void` | 关闭方案 / 重新编译时 | 释放资源、关闭句柄                       |

执行顺序：编译 → `Init()` → 静默模式下首次 `Process()` → 每次执行 `Process()` → 关闭时 `Dispose()`

## 变量输入与输出（直接赋值）

VM 脚本的输入输出变量在 `UserProperty.cs` 中定义，在 `UserScript.cs` 中**直接通过变量名访问**，无需调用 Get/Set 接口。

### 类型映射规则

三条核心规则，记住即可：

| 规则 | VM 类型示例 | 脚本 C# 类型 | 示例 |
|------|-----------|-------------|------|
| 标量 → 基础类型 | INT, FLOAT, STRING, DOUBLE | `int`, `float`, `string`, `double` | `int val = in0; out0 = val;` |
| IMAGE → ImageData | IMAGE | `ImageData`（特例，非数组） | `ImageData img = imgIn; imgOut = img;` |
| 复合 → `<Type>Data[]` | POINT, ROIBOX, CIRCLE, RECT, LINE, ELLIPSE, ANNULUS, POLYGON, CONTOUR_POINT | `PointData[]`, `RoiboxData[]` … | `PointData[] pts = in0; out0 = pts;` |
| 数组 → 直接用 | INT 数组, FLOAT 数组, STRING 数组, DOUBLE 数组 | `int[]`, `float[]`, `string[]`, `double[]` | `int[] arr = in0; out0 = arr;` |

**约束**：变量名称必须保证唯一性，多个变量不能使用同一个名称。

> 完整类型映射表与读写示例见 [interface-quickref.md](./examples/interface-quickref.md#1-变量类型映射)

### 遗留接口（不推荐）

`GetIntValue`、`SetIntValue` 等为上一代接口，**新代码不要使用**。仅当需要按变量名字符串动态访问时才考虑。

遗留接口签名见 [Script.Interface.cs](./references/Script.Interface.cs)

## 标准模板

```csharp
using System;
using Script.Methods;

public partial class UserScript : ScriptMethods, IProcessMethods
{
    int processCount;

    public void Init()
    {
        processCount = 0;
    }

    public bool Process()
    {
        // 业务逻辑
        return true;
    }

    public virtual void Dispose()
    {
    }
}
```

> 完整示例见 [examples/](./examples/)（基础模板、图像处理、ROI 处理）

## 输出要求

- 用户要求"改代码"或"补功能"时，返回整理好的完整脚本
- 只需说明思路时，先给简短结论，再补关键接口和注意点
- 涉及变量、数组、图像、ROI 时，必须写清输入、输出
- 不要臆造变量名或数据结构字段；不确定时说明需要查参考文件
- **不要使用 Get/Set 遗留接口**，除非场景确实需要动态变量名访问

## 参考资料与注意事项

### 文件索引

| 文件 | 用途 |
|------|------|
| [references/Script.Interface.cs](./references/Script.Interface.cs) | 遗留接口签名原始定义 |
| [references/Script.DataStruct.cs](./references/Script.DataStruct.cs) | 数据结构字段定义 |
| [references/Script.ExMethods.cs](./references/Script.ExMethods.cs) | Mat ↔ ImageData 转换方法 |
| [examples/interface-quickref.md](./examples/interface-quickref.md) | 变量类型映射 + 接口速查索引 |
| [examples/code-patterns.md](./examples/code-patterns.md) | 代码模式库（13 种场景模板） |
| [examples/](./examples/) | 完整脚本示例 |

### 注意事项

- 非托管资源（如 DLL 句柄）必须在 `Dispose()` 中释放
- `ShowMessageBox` 会暂停流程，仅用于开发调试
- 若本文与参考文件冲突，以参考文件为准

## 代码生成工作流

当用户请求生成、修改、补全脚本代码时，**严格按以下步骤执行**：

### Step 1：读取已有代码

1. 读取当前工作目录下的 `UserProperty.cs`（输入输出定义）和 `UserScript.cs`（脚本逻辑）
2. 如果文件不存在，向用户提问要求提供文件路径
3. 从 `UserProperty.cs` 中提取已有的输入输出变量名和类型，建立变量映射表
4. 用户的请求需要第三方库时，分析 `*.csproj` 文件确认库是否存在；缺少则中断生成并提示用户

### Step 2：分析用户需求

根据用户描述，确定以下要素：

| 要素 | 说明 |
|------|------|
| 数据类型 | 涉及哪些 VM 变量类型，对应脚本中什么 C# 类型（查类型映射规则） |
| 数据流向 | 哪些是输入，哪些是输出，是否需要中间变量 |
| 处理逻辑 | 算法/计算/变换的具体要求 |
| 外部依赖 | 是否需要 OpenCvSharp、通信模块等 |
| 生命周期 | 是否需要 Init() 初始化 / Dispose() 释放资源 |

### Step 3：确认变量映射

根据 `UserProperty.cs` 中的定义和类型映射规则，确认：

1. **每个输入变量**：变量名 → C# 类型（如 `in0` → `int`，`in1` → `PointData[]`）
2. **每个输出变量**：变量名 → C# 类型
3. **需要的数据结构字段**：查 [Script.DataStruct.cs](./references/Script.DataStruct.cs) 确认
4. **需要的转换方法**：如 `ImageDataToMat` / `MatToImageData`，见 [Script.ExMethods.cs](./references/Script.ExMethods.cs)

**关键原则**：

- 所有变量读写使用直接赋值，不用 Get/Set 遗留接口
- 非数组 VM 变量类型对应 `<Type>Data[]` 数组类型
- 变量名必须与 `UserProperty.cs` 中定义一致

### Step 4：查阅示例与模式

**在生成代码前，先浏览 [./examples/](./examples/) 目录**，寻找与用户需求匹配的参考：

- [01-basic-template.cs](./examples/01-basic-template.cs) — 基础脚本框架，几乎所有场景的起点
- [02-canny-edge-detection.cs](./examples/02-canny-edge-detection.cs) — 图像处理场景参考
- [03-roi.cs](./examples/03-roi.cs) — ROI 处理场景参考
- [interface-quickref.md](./examples/interface-quickref.md) — 确认类型映射与接口时查阅
- [code-patterns.md](./examples/code-patterns.md) — 按场景匹配代码模式

根据需求在代码模式库中选择匹配的模式，可组合使用。模式匹配详见 [code-patterns.md](./examples/code-patterns.md#模式组合指南)。

### Step 5：组装代码

1. **using 声明**：根据需求添加（OpenCvSharp、System.Runtime.InteropServices 等）
2. **类声明**：`UserScript : ScriptMethods, IProcessMethods`
3. **字段声明**：在类顶部声明所有需要的字段，包括 `processCount`
4. **Init()**：初始化所有字段，预分配可复用资源
5. **Process()**：直接赋值获取输入 → 处理逻辑 → 直接赋值设置输出；合理拆分为辅助方法
6. **辅助方法**：放在 Process() 下方，每个方法添加 XML 注释
7. **Dispose()**：仅在需要释放非托管资源时编写

### Step 6：自校验

生成代码后，逐项检查：

- [ ] 变量名与 `UserProperty.cs` 中定义一致
- [ ] 变量类型映射正确（非数组 VM 类型 → `<Type>Data[]`）
- [ ] 所有变量读写使用直接赋值，无遗留 Get/Set 接口调用
- [ ] 图像处理流程中 `Mat` 对象已 Dispose
- [ ] 没有臆造变量名或数据结构字段
- [ ] 代码基于 .NET Framework 4.6.1，未使用 4.6.1 之后的 API
- [ ] 每个方法都有 XML 注释
- [ ] 结构化注释（如 `//You can add your codes here`）已删除
- [ ] 当工作目录中存在 `*.csproj` 文件时，调用 `./assets/find_msbuild.ps1` 尝试编译；有报错则根据信息修正，直到编译通过

---

## 扩展范式

本 skill 采用**分层架构**，便于后续增量扩展。新增场景支持时，按以下范式操作：

### 扩展步骤

1. **references/** — 新增接口/数据结构的原始定义文件（如 `Script.3D.cs`）
2. **examples/** — 新增完整示例脚本（如 `04-3d-pointcloud.cs`）+ 更新 `interface-quickref.md` 类型映射 + 更新 `code-patterns.md` 新增模式
3. **SKILL.md** — 在本节记录扩展清单；如需修改"必须遵守"或"标准模板"，同步更新

### 扩展清单

| 场景 | 状态 | 说明 |
|------|------|------|
| 2D 脚本（标准） | ✅ 已支持 | ScriptMethods + IProcessMethods |
| 3D 脚本 | 🔲 待扩展 | 需新增 VM3DScriptBase 基类、3D 类型映射、3D 示例 |
| OpenCvSharp 集成 | ✅ 已支持 | 示例 02 + 模式 4 |
| 其他第三方库 | 🔲 按需扩展 | 新增 references + examples + 校验 .csproj |

> 扩展时注意：references/ 放原始定义，examples/ 放可运行示例和速查文档，SKILL.md 只放规则和链接，不重复详细内容。
