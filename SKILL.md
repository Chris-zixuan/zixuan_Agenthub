---
name: vm-script-skill
description: "VisionMaster（VM）脚本开发辅助。用户提到 VisionMaster、VM 脚本、UserScript、IProcessMethods、Script.Methods、Get/Set 接口、图像/ROI/数组读写时触发"
version: 1.2.0
---

# VisionMaster 脚本开发技能

## 目标

帮助用户编写、修改、排查 VisionMaster 脚本；优先输出可直接使用的 C# 代码，并严格遵守 VM 接口约束。

## 触发范围

当用户在讨论以下内容时使用本 skill：

- 脚本，输入输出
- `UserScript` / `IProcessMethods` / `Script.Methods`
- `GetXxxValue` / `SetXxxValue` / 数组接口 / 图像接口 / ROI 接口
- 模块参数、全局变量、模块间读写、调试输出

## 必须遵守

- VM 脚本模块采用标准 C# 编程，基于 .NET Framework 4.6.1，需要保证调用的方法是基于4.6.1版本
- 脚本基类必须是 `UserScript`，接口必须实现 `IProcessMethods`，命名空间使用 `Script.Methods`
- 用户脚本的输出和输出约定在 UserProperty.cs 中，用户的脚本逻辑在 UserSCript.cs 中。首先读取这两个文件，确定输出和输出与已有的逻辑。再结合用户的请求进行下一步。
- 代码组织上，`Process()` 放在上方，辅助方法放在下方,避免`Process()` 中出现过长的逻辑，需要合理的拆分不同的功能为方法，然后脚本内容调用。
- 生成代码时删除脚本结构化的注释，需要给每一个方法都添加注释。
- 获取输入输出时，应当先尝试直接赋值，只有当直接赋值出现错误时，再考虑使用接口获取值。
- 只有当需要显示释放资源的时候，才会写 `Dispose()`。
- 脚本不考虑性能优化，以逻辑简单清晰为最主要。
- 当分析用户的意图需要调用第三方库时，优先分析目录中的`*.csproj`文件，如果缺少对应的库则直接中断生成并提示用户。
- 当你发现自己需要反编译才能获取到需要的信息时，你应当首先查看references目录下的文件，如果没有相关信息则中断生成并提示用户。

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

## 变量输入与输出

使用GetIntValue、GetRoiboxValue等接口为上一代数据获取方式，出于方案兼容考虑，保留了这些接口，但不推荐使用。

实际使用中，请根据您的变量名称和变量类型修改代码片段，其中不同变量类型在脚本中对应不同的数组类型，命名规则为<变量类型>Data[]（适用变量类型为非数组类型），例如变量为POINT类型，则对应脚本中的PointData[]类型。变量为数组类型的在脚本中直接使用。

变量名称需要保证唯一性，即多个变量不要使用同一个名称。

example

```csharp
// 获取整个输入数组数据
PointData[] point1 = in0;

// 分别获取输入数组的每个数据
PointData[] point2 = new PointData[in0.Length];
for (int i=0;i<in0.Length;i++)
{
        point2[i] = in0[i];
}


// 输入直接赋值给输出
out0=in0;

// 自定义数据赋值给输出
PointData[] pt = new PointData[in0.Length];
for (int i=0;i<in0.Length;i++)
 {
        pt[i] = new PointData();
        pt[i].PointX=i;
        pt[i].PointY=i;
 }
out0 = pt;
```

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

## 输出要求

- 若用户要求“改代码”或“补功能”，优先返回整理好的完整脚本
- 若只需说明思路，先给简短结论，再补关键接口和注意点
- 涉及变量、数组、图像、ROI 时，必须写清输入、输出和返回值判断
- 若代码里会调用 `Get` / `Set` 接口，必须处理返回值，不要省略判断
- 不要臆造接口；不确定时应说明需要查参考文件

## 接口分类参考

完整接口签名见 [Script.Interface.cs](./references/Script.Interface.cs)
数据结构字段见 [Script.DataStruct.cs](./references/Script.DataStruct.cs)

## 常见案例参考

## 自定义方法参考

自定义的方法见 [Script.ExMethods.cs](./references/Script.ExMethods.cs)

## 注意事项

- 避免在 `Process()` 中频繁创建和销毁对象，优先使用字段缓存
- 非托管资源（如 DLL 句柄）必须在 `Dispose()` 中释放
- `ShowMessageBox` 会暂停流程，仅用于开发调试
- 代码模板和完整示例见 [./examples/](./examples/)

## 参考资料

- 接口定义：[./references/Script.Interface.cs](./references/Script.Interface.cs)
- 数据结构：[./references/Script.DataStruct.cs](./references/Script.DataStruct.cs)
- VM SDK 手册：`..\Development\V4.x\Documentations`
- 若本文与参考文件冲突，以参考文件为准
