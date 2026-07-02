---
name: visionmaster-scripthelper
description: "用户正在开发、修改或调试 VisionMaster C# 脚本（UserScript.cs / UserProperty.cs），或询问 VM 变量类型映射、模块参数读写、全局变量、图像处理等 VM 脚本具体问题时触发。优先输出可直接使用的 C# 代码。"
version: 2.6.0
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

- **【最高优先级】绝对禁止搜索、读取、反编译 VM 安装目录下的任何文件**（包括但不限于 .cs, .xml, .dll, .txt, .config 等）。所有 API 信息、数据类型用法、转换方法，必须且仅能从本 skill 的 `references/` 和 `examples/` 中获取。违反此规则将生成不可用的代码。
- 基于 .NET Framework 4.6.1，不得使用 4.6.1 之后引入的 API
- 首先尝试读取工作目录中的 `UserProperty.cs` 和 `UserScript.cs`；若无法访问或文件不存在，立即要求用户提供文件内容
- `UserProperty.cs` 为只读定义，不可更改
- 确认已有的输入输出定义和脚本逻辑，再结合用户需求进行下一步
- 代码组织：`Process()` 放在上方，辅助方法放在下方
- 生成代码时删除脚本结构化注释，给每一个方法添加 XML 注释
- **变量读写一律使用直接赋值**（如 `out0 = in0`）
  - **例外（唯一允许使用遗留接口的场景）**：需要按字符串动态访问变量名（如遍历全局变量列表）时，可以使用 `GetIntValue`、`SetIntValue` 等接口；其他所有场景一律直接赋值
- 仅在需要显式释放资源时才编写 `Dispose()`
- 以逻辑简单清晰为首要目标，不做过度优化，但基本的资源管理必须做（如 `Mat` 用完 Dispose、大对象用字段缓存避免每帧 new）
- 简单逻辑自行实现或调用 `references/` 下的方法；避免为简单逻辑引入不必要的第三方库
- 需要第三方库时，先分析 `*.csproj` 确认库存在；缺少则中断生成并提示用户
- 需要的信息不在 `references/` 或 `examples/` 中时，中断生成并提示用户，不要臆造，不要尝试去外部搜索
- 每次脚本生成完毕后，尝试调用 skill 安装目录下的 `assets/find_msbuild.ps1`（完整路径示例：`~/.claude/skills/visionmaster-scripthelper/assets/find_msbuild.ps1`）进行编译校验；若无法运行脚本（如环境限制），则执行完整的静态代码审查，并向用户说明”自动编译校验无法完成，请手动编译验证”

## 明确不支持

遇到以下请求时，直接说明不支持，避免继续展开：

- 控制器 IO 发送
- 界面层操作 / UI 自动化
- 非托管资源的外部封装方案
- 通讯协议解析
- **反编译或搜索 VM 安装目录来获取 API 信息**（只有 skill 内的 `references/` 和 `examples/` 是权威来源）

如用户需要上述能力，可建议改用外部程序、上位机或其他 SDK 方案。

## 生命周期

| 方法        | 修饰                  | 触发时机              | 用途                                     |
| ----------- | --------------------- | --------------------- | ---------------------------------------- |
| `Init()`    | `public void`         | 加载方案 / 预编译时   | 初始化变量、创建句柄、加载资源           |
| `Process()` | `public bool`         | 每次流程执行          | 业务逻辑、数据处理；返回 `true` 表示成功 |
| `Dispose()` | `public virtual void` | 关闭方案 / 重新编译时 | 释放资源、关闭句柄                       |

执行顺序：编译 → `Init()` → 静默模式下首次 `Process()`（例如方案验证、无界面运行时的额外调用） → 每次执行 `Process()` → 关闭时 `Dispose()`

## 变量输入与输出（直接赋值）

VM 脚本的输入输出变量在 `UserProperty.cs` 中定义，在 `UserScript.cs` 中**直接通过变量名访问**，无需调用 Get/Set 接口。

### 类型映射规则

三条核心规则，记住即可：

| 规则                  | VM 类型示例                                                                 | 脚本 C# 类型                                 | 示例                                   |
| --------------------- | --------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------- |
| 标量 → 基础类型       | INT, FLOAT, STRING, DOUBLE, BYTE                                            | `int`, `float`, `string`, `double`, `byte[]` | `int val = in0; out0 = val;`           |
| IMAGE → ImageData     | IMAGE                                                                       | `ImageData`（特例，非数组）                  | `ImageData img = imgIn; imgOut = img;` |
| 复合 → `<Type>Data[]` | POINT, ROIBOX, CIRCLE, RECT, LINE, ELLIPSE, ANNULUS, POLYGON, CONTOUR_POINT | `PointData[]`, `RoiboxData[]` …              | `PointData[] pts = in0; out0 = pts;`   |
| 数组 → 直接用         | INT 数组, FLOAT 数组, STRING 数组, DOUBLE 数组                              | `int[]`, `float[]`, `string[]`, `double[]`   | `int[] arr = in0; out0 = arr;`         |
| 3D 专用读取 | STEREO_IMAGE, POINT3D, POSE_INFO                                           | `StereoImageData`, `Point3DData`, `PoseInfoData[]` | 见下方"3D 变量读写"               |

**特别注意**：除标量、数组和 IMAGE 外的复合类型（如 POINT, ROIBOX 等），在脚本中均映射为对应的 `<Type>Data[]` 数组类型。IMAGE 类型直接映射为 `ImageData`，不是数组。

#### 3D 变量读写

STEREO_IMAGE、POINT3D、POSE_INFO 等 3D 专用类型**不支持直接赋值读取**，须调用对应 Get 接口：

```csharp
// STEREO_IMAGE 读取
StereoImageData rangeImg = 深度图in;

// STEREO_IMAGE 输出（直接赋值）
outImage = rangeImg;
```

深度图 Buffer 为 S16（每像素 2 字节），无效值为 `-32768`，物理坐标转换公式：
`x = col * Xscale + Xoffset`，`z = raw * Zscale + Zoffset`

> 完整字段说明见 [interface-quickref.md#1c](./examples/interface-quickref.md#1c-3d-专用类型)

**约束**：变量名称必须保证唯一性，多个变量不能使用同一个名称。

#### ImageData 赋值语义

`ImageData` 的直接赋值（`imgOut = imgIn`）为**引用传递**，两个变量会指向同一内存。如需独立图像副本，必须通过 `ImageDataToMat` 获取 Mat，处理后再用 `MatToImageData` 生成新图像。

> 完整类型映射表与读写示例见 [interface-quickref.md](./examples/interface-quickref.md#1-变量类型映射)

### 常见运行时错误排查

以下为脚本运行中高频出现的错误及快速排查方向：

| 现象                      | 可能原因                                                     | 检查方式                                                                   |
| ------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------- |
| `NullReferenceException`  | 输入变量未连线或数据为空                                     | 检查对应输入是否已绑定模块输出，数据是否到达                               |
| 类型转换错误              | 变量类型定义与赋值类型不匹配（例如将 `float` 赋给 INT 变量） | 核对 `UserProperty.cs` 中的类型定义与脚本中的实际类型                      |
| 内存占用持续增长          | 未释放 Mat、每帧重复创建大对象                               | 确保所有 new 出的 Mat 用完后调用 `Dispose()`；将大数组、Mat 等缓存为类字段 |
| 输出变量值不更新          | 未对输出变量赋值，或赋值放在了条件分支中未执行               | 确认输出变量在每个 `Process()` 末尾均被赋值                                |
| 图像显示异常（黑图/错位） | 直接修改了只读的输入图像，或未克隆就修改了共享图像           | 对需要修改的图像先通过 `Mat` 克隆再处理                                    |

> 更多调试输出技巧见下文“调试输出建议”。

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
        return true;
    }

    // 仅在需要释放非托管资源时添加 Dispose()
}
```

> 完整示例见 [examples/](./examples/)（基础模板、图像处理、ROI 处理）

## 输出要求

- 用户要求“改代码”或“补功能”时，返回整理好的完整脚本
- 只需说明思路时，先给简短结论，再补关键接口和注意点
- 涉及变量、数组、图像、ROI 时，必须写清输入、输出
- 不要臆造变量名或数据结构字段；不确定时说明需要查参考文件
- **不要使用 Get/Set 遗留接口**，除非确实需要动态变量名访问（见必须遵守中的例外说明）

## 调试输出建议

- 推荐使用 `GlobalVariableModule.SetValue("调试信息", msg)` 将调试内容写入字符串类型的全局变量，通过显示模块观察
- `ShowMessageBox` 会暂停整个流程，仅用于关键断点调试，生产环境务必删除
- 善用 `processCount` 字段打印每帧执行信息（例如“Process 第 N 次执行，输入值：...”）

## 参考资料与注意事项

### 文件索引

| 文件                                                                 | 用途                              |
| -------------------------------------------------------------------- | --------------------------------- |
| [references/Script.Interface.cs](./references/Script.Interface.cs)   | 遗留接口签名原始定义              |
| [references/Script.DataStruct.cs](./references/Script.DataStruct.cs) | 数据结构字段定义                  |
| [references/Script.ExMethods.cs](./references/Script.ExMethods.cs)   | Mat / Bitmap ↔ ImageData 转换方法 |
| [examples/interface-quickref.md](./examples/interface-quickref.md)   | 变量类型映射 + 接口速查索引       |
| [examples/code-patterns.md](./examples/code-patterns.md)             | 代码模式库（12 种场景模板）       |
| [examples/](./examples/)                                             | 完整脚本示例                      |

### 注意事项

- 非托管资源（如 DLL 句柄）必须在 `Dispose()` 中释放
- 若本文与参考文件冲突，以参考文件为准

---

## 代码生成工作流

当用户请求生成、修改、补全脚本代码时，**严格按以下步骤执行**。

### Step 1：获取已有代码

1. **尝试读取**当前工作目录下的 `UserProperty.cs`（输入输出定义）和 `UserScript.cs`（脚本逻辑）
2. **如果无法访问或文件不存在**，立即要求用户粘贴这两个文件的内容或提供准确路径，禁止猜测继续
3. 从 `UserProperty.cs` 中提取已有的输入输出变量名和类型，建立变量映射表
4. 用户的请求需要第三方库时，分析 `*.csproj` 文件确认库是否存在；缺少则中断生成并提示用户

### Step 2：分析用户需求

根据用户描述，确定以下要素：

| 要素     | 说明                                                           |
| -------- | -------------------------------------------------------------- |
| 数据类型 | 涉及哪些 VM 变量类型，对应脚本中什么 C# 类型（查类型映射规则） |
| 数据流向 | 哪些是输入，哪些是输出，是否需要中间变量                       |
| 处理逻辑 | 算法/计算/变换的具体要求                                       |
| 外部依赖 | 是否需要 OpenCvSharp、通信模块等                               |
| 生命周期 | 是否需要 Init() 初始化 / Dispose() 释放资源                    |

### Step 3：确认变量映射

根据 `UserProperty.cs` 中的定义和类型映射规则，确认：

1. **每个输入变量**：变量名 → C# 类型（如 `in0` → `int`，`in1` → `PointData[]`）
2. **每个输出变量**：变量名 → C# 类型
3. **需要的数据结构字段**：查 [Script.DataStruct.cs](./references/Script.DataStruct.cs) 确认
4. **需要的转换方法**：如 `ImageDataToMat` / `MatToImageData` / `BitmapToImageData` / `ImageDataToBitmap`，见 [Script.ExMethods.cs](./references/Script.ExMethods.cs)

**关键原则**：

- 所有变量读写使用直接赋值，除非明确需要按字符串动态访问变量名，否则禁用遗留接口
- 除标量、数组和 IMAGE 外的复合 VM 类型，均映射为 `<Type>Data[]` 数组
- 变量名必须与 `UserProperty.cs` 中定义一致

### Step 4：查阅示例与模式 —— 强制查阅，禁止跳过

**在生成代码前，必须根据以下对照表打开并阅读对应参考文件。绝对禁止去 VM 安装目录搜索或反编译。**

#### 按需求查找必读文件

| 你想做什么                       | 必须先打开阅读的文件                                                      |
| -------------------------------- | ------------------------------------------------------------------------- |
| 了解变量类型映射、直接赋值写法   | `examples/interface-quickref.md`                                          |
| 把输入图像转成 Mat               | `examples/02-canny-edge-detection.cs` 和 `references/Script.ExMethods.cs` |
| 把输入图像转成 Bitmap            | `references/Script.ExMethods.cs`                                          |
| 处理 ROI（裁剪、遍历、分析）     | `examples/03-roi.cs` 和 `references/Script.DataStruct.cs`                 |
| 读取/写入多个不同类型的全局变量  | `examples/01-basic-template.cs`（查看多变量处理模式）                     |
| 不确定数据结构字段名             | `references/Script.DataStruct.cs`                                         |
| 需要遗留接口签名（仅动态名场景） | `references/Script.Interface.cs`                                          |
| 想要操作CAD图纸，完成图纸转换等  | `examples/04-trans-CAD-file.cs`                                           |
| 处理立体图像 / 深度图 / 点云提取 | `examples/05-stereo-depth-pointcloud.cs` 和 `references/Script.DataStruct.cs` |

#### 查找 API 的强制流程

当你在生成代码时遇到不确定的类型、方法或字段：

1. **立即**查阅上表中对应的文件（使用 `Read` 打开）。
2. 若表中没有完全匹配的需求，按以下顺序逐篇查阅，直到找到答案：
   `examples/interface-quickref.md` → `references/Script.ExMethods.cs` → 对应场景的示例文件。
3. 如果所有 skill 内资源都找不到答案，**中断生成并明确告知用户缺少哪部分信息**，禁止去 VM 安装目录或其它路径搜索。

#### 模式组合示例

- 用户需要”图像预处理 + ROI 内统计” → 组合模式4（图像处理管道）+ 模式5（ROI 处理）
- 用户需要”ROI 网格分割并输出子区域” → 组合模式6（ROI 网格分割）+ 模式5（ROI 处理）
- 用户需要”从全局变量获取参数、处理图像后输出” → 模式7（全局变量控制流程）+ 模式4（图像处理管道）

详细模式组合指南见 [code-patterns.md](./examples/code-patterns.md#模式组合指南)。

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
- [ ] 变量类型映射正确（复合类型 → `<Type>Data[]`，IMAGE → `ImageData`，数组和标量直接对应）
- [ ] 所有变量读写使用直接赋值，除非符合动态名例外
- [ ] 图像处理流程中 `Mat` 对象已 Dispose，或通过缓存避免泄漏
- [ ] 没有臆造变量名或数据结构字段
- [ ] 代码基于 .NET Framework 4.6.1，未使用 4.6.1 之后的 API
- [ ] 每个方法都有 XML 注释
- [ ] 结构化注释（如 `//You can add your codes here`）已删除
- [ ] 已执行或尝试执行编译校验：若 skill 安装目录下的 `assets/find_msbuild.ps1` 可运行则编译至通过；否则进行静态审查，并向用户说明”自动编译校验无法完成，请手动编译确认”

---

## 扩展范式

本 skill 采用**分层架构**，便于后续增量扩展。新增场景支持时，按以下范式操作：

### 扩展步骤

1. **references/** — 新增接口/数据结构的原始定义文件（如 `Script.3D.cs`）
2. **examples/** — 新增完整示例脚本（如 `04-3d-pointcloud.cs`）+ 更新 `interface-quickref.md` 类型映射 + 更新 `code-patterns.md` 新增模式
3. **SKILL.md** — 在本节记录扩展清单；如需修改“必须遵守”或“标准模板”，同步更新

### 扩展清单

| 场景                       | 状态        | 说明                                             |
| -------------------------- | ----------- | ------------------------------------------------ |
| 2D 脚本（标准）            | ✅ 已支持   | ScriptMethods + IProcessMethods                  |
| 3D 深度图 / 点云提取       | ✅ 已支持   | StereoImageData + GetStereoImageValue，示例 05   |
| OpenCvSharp 集成           | ✅ 已支持   | 示例 02 + 模式 4                                 |
| System.Drawing.Bitmap 集成 | ✅ 已支持   | Script.ExMethods.cs + 模式 4b                    |
| 其他第三方库               | 🔲 按需扩展 | 新增 references + examples + 校验 .csproj        |

> 扩展时注意：references/ 放原始定义，examples/ 放可运行示例和速查文档，SKILL.md 只放规则和链接，不重复详细内容。
