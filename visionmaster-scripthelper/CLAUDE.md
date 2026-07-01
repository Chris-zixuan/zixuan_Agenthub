# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 这是什么

本目录是 VisionMaster (VM) C# 脚本开发辅助 Skill。当用户在 VM 中开发 `UserScript.cs` / `UserProperty.cs` 时，本 Skill 提供 API 参考、代码模板和编译校验。

## 文件结构

```
├── SKILL.md                        # Skill 主定义（规则、工作流、触发条件）
├── references/
│   ├── Script.Interface.cs         # 遗留 Get/Set 接口、全局变量、模块控制、通信模块签名
│   ├── Script.DataStruct.cs        # 所有数据结构定义（ImageData, RoiboxData, PointData 等）
│   └── Script.ExMethods.cs         # Mat/Bitmap ↔ ImageData 转换方法实现
├── examples/
│   ├── interface-quickref.md       # 变量类型映射 + 接口速查（代码生成前必查）
│   ├── code-patterns.md            # 12 种场景代码模式库
│   ├── 01-basic-template.cs        # 基础模板（标量/数组/复合类型读写 + 全局变量 + 模块控制）
│   ├── 02-canny-edge-detection.cs  # OpenCV 图像处理完整示例
│   ├── 03-roi.cs                   # ROI 网格分割示例
│   └── 04-trans-CAD-file.cs        # CAD 图纸转换示例
└── assets/
    └── find_msbuild.ps1            # MSBuild 查找脚本（编译校验用）
```

## 核心规则（生成 VM 脚本时必须遵守）

1. **变量读写用直接赋值**：`int val = in0; out0 = val;`，禁止使用 `GetIntValue`/`SetIntValue` 等遗留接口，除非需要按字符串动态访问变量名
2. **类型映射**：标量→基础类型、IMAGE→`ImageData`（非数组）、复合类型→`<Type>Data[]`（如 POINT→`PointData[]`）
3. **基于 .NET Framework 4.6.1**，不得使用 4.6.1 之后引入的 API
4. **禁止搜索/反编译 VM 安装目录**，所有 API 信息只能从 `references/` 和 `examples/` 获取
5. 先读 `UserProperty.cs` 和 `UserScript.cs`，无法访问则要求用户提供
6. `Process()` 放上方，辅助方法放下方；每个方法加 XML 注释；删除模板结构化注释
7. `Mat` 用完必须 `Dispose()`，大对象用字段缓存避免每帧 new
8. 代码生成后运行 `assets/find_msbuild.ps1` 编译校验；无法运行则做静态审查

## 修改 Skill 的约定

- `references/` 放原始 API 定义（接口签名、数据结构）
- `examples/` 放可运行示例和速查文档
- `SKILL.md` 只放规则和工作流，不重复详细 API 内容
- 新增场景按范式：references 加定义 → examples 加示例和模式 → SKILL.md 记录扩展清单
