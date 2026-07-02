---
name: vm-project-PLACEHOLDER
description: "当用户在 <项目名> 项目中开发 VM 脚本，或提到 <触发关键词> 时触发。基于 visionmaster-scripthelper 基线，叠加项目专属变量、外部程序接口和代码模板。"
version: 0.1.0
author: ChrisYang
tags:
  - VisionMaster
  - 脚本开发
  - 项目定制
---

# VM 脚本开发 — <项目名>

## 这是什么

本 Skill 是 [visionmaster-scripthelper](../visionmaster-scripthelper/SKILL.md) 的**项目定制扩展**。
基线 Skill 提供通用 VM C# 脚本开发规则和 API 参考，本 Skill 在此之上叠加项目专属的变量定义、外部通信接口和代码模板。

## 触发后立即执行

**在生成任何代码之前，必须先完成以下读取**：

1. **读取基线规则**：`~/.claude/skills/visionmaster-scripthelper/SKILL.md`
   - 所有基线「必须遵守」规则本 Skill 照单全收
   - 类型映射、变量读写规则、代码组织规则全部继承
2. **读取项目上下文**：本目录 `references/project-context.md`
   - 项目变量定义表、通信方式、外部程序接口
3. **读取外部接口**：本目录 `references/external-api.cs`
   - 外部程序通信的 C# 封装类/方法签名
4. **读取工作目录**：`UserProperty.cs` 和 `UserScript.cs`（同基线 Step 1）

## 项目专属规则

<!-- 在下方填写项目特有的约束，覆盖或补充基线规则 -->

- 外部通信方式：`<NamedPipe / TCP / 串口 / 文件监控 / 无>`
- 变量命名规范：`<如有，在此说明>`
- 其他约束：`<如有，在此说明>`

## 继承基线规则清单

以下规则**直接从基线 Skill 继承，本 Skill 不再重复定义**：

| 规则 | 来源 |
|------|------|
| 变量直接赋值（禁用 Get/Set 遗留接口） | 基线「必须遵守」 |
| 类型映射（标量→基础类型、IMAGE→ImageData、复合→TypeData[]） | 基线「类型映射规则」 |
| .NET Framework 4.6.1 约束 | 基线「必须遵守」 |
| 禁止搜索/反编译 VM 安装目录 | 基线「必须遵守」 |
| Mat Dispose / 大对象缓存 | 基线「必须遵守」 |
| 代码组织（Process 上，辅助方法下，XML 注释） | 基线「代码组织」 |
| 变量名与 UserProperty.cs 一致 | 基线 Step 3 |
| 编译校验（find_msbuild.ps1） | 基线 Step 6 |
| 生命周期（Init → Process → Dispose） | 基线「生命周期」 |

## 与基线的差异

<!-- 在此说明本项目与基线有哪些不同，例如： -->
<!-- - 始终通过 NamedPipe 与外部 C++ 程序通信 -->
<!-- - 输入变量固定为 xxx，严禁修改 -->
<!-- - 输出必须包含 result_code (INT) 和 log_message (STRING) -->

## 代码生成工作流

与基线 Skill 完全一致（Step 1 ~ Step 6），唯一差异在 **Step 2（分析用户需求）**：

- 额外检查 `references/project-context.md` 中的变量表和通信方式
- 如需求涉及外部程序交互，必须查阅 `references/external-api.cs`
- 如需求匹配 `examples/` 中的项目模板，以此为起点展开

## 文件索引

| 文件 | 用途 |
|------|------|
| [references/project-context.md](./references/project-context.md) | 项目变量定义、通信方式、外部程序说明 |
| [references/external-api.cs](./references/external-api.cs) | 外部程序通信的 C# 接口封装 |
| [examples/](./examples/) | 项目专属脚本示例 |

## 外部 Skill 引用

| Skill | 路径 | 用途 |
|-------|------|------|
| visionmaster-scripthelper | `~/.claude/skills/visionmaster-scripthelper/` | 基线 VM 脚本开发规则与 API 参考 |
