# Zixuan 的 Claude Code 工具箱 / Zixuan's Claude Code Toolkit

[English](#english) | [中文](#中文)

---

## 中文

### 📖 简介

这是我个人收集整理的 Claude Code Skills 与插件集合，记录我在日常使用 Claude Code 过程中沉淀下来的好用工具。

### 📊 内容总览

目前共包含 **12 个 Skills** + **1 个插件文档**：

#### 💻 开发辅助

| Skill | 说明 |
|-------|------|
| [VisionMaster 脚本助手](./visionmaster-scripthelper) | HiVision VisionMaster C# 脚本开发辅助 |
| [MVB-COCO 标注生成](./mvb-coco-annotation) | 将图片目录自动转换为 MVB-COCO 格式分类数据集 |

#### 💼 效率工具

| Skill / 插件 | 说明 |
|--------------|------|
| [记忆系统初始化](./memory-init) | 在当前目录一键部署 AI 记忆系统 |
| [文件夹整理助手](./organize) | 扫描分类、清理冗余，整理混乱目录 |
| [项目地图生成](./project-map-builder) | 为指定目录生成 PROJECT_MAP.md 结构概览 |
| [支付宝流水记账](./alipay-booking) | 一键将支付宝交易流水 CSV 整理为随手记记账 Excel |
| [Claude Code HUD](./Claude%20Code%20HUD) | 终端实时状态栏，显示上下文用量与 Agent 状态 |

#### 🎓 学习与研究

| Skill | 说明 |
|-------|------|
| [系统学习材料生成](./system-study) | 给定领域/技术，自主调研并产出结构化 HTML 学习材料 |

#### ✍️ 写作与沟通

| Skill | 说明 |
|-------|------|
| [受众适配助手](./audience-adapter) | 向上汇报/跨部门沟通，按受众角色自动调整信息粒度与语言风格 |
| [SOP 文档生成](./sop-writer) | 将业务流程梳理为含 RACI 矩阵、流程图和异常处理的完整 SOP 文档 |
| [周报/月报生成](./work-report-writer) | 从零散工作记录与 git log 生成结构化周报或月报 |
| [公众号文章生成](./mp-article-writor) | 将素材整理为公众号/少数派长文，含行文自检与配图 prompt |
| [简历优化器](./resume-optimizer) | 专业简历优化与生成，支持文本/Word/PDF输入，结合JD定制，输出Word+PDF+质量报告 |

> 📚 每个 Skill 的详细使用示例见 [EXAMPLES.md](./EXAMPLES.md)

---

### 🚀 快速开始

```bash
cd ~/.claude/skills/
git clone https://github.com/Chris-zixuan/zixuan_Agenthub.git
```

安装后在 Claude Code 中通过 `/skill-name` 调用，或直接用自然语言描述需求触发。

---

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！如果你有好用的 Skill 或插件推荐，欢迎分享。

---

### 📄 许可证

[MIT License](./LICENSE)

---

## English

### 📖 Introduction

A personal collection of Claude Code Skills and plugins — tools I've accumulated through daily use.

### 📊 Overview

**12 Skills** + **1 plugin guide**:

| Skill / Plugin | Description |
|----------------|-------------|
| [VisionMaster Script Helper](./visionmaster-scripthelper) | C# script development for HiVision VisionMaster |
| [MVB-COCO Annotation](./mvb-coco-annotation) | Auto-generate MVB-COCO format dataset from an image folder |
| [Memory Init](./memory-init) | One-click AI memory system deployment |
| [Organize](./organize) | Scan, classify, and clean up messy folders |
| [Project Map Builder](./project-map-builder) | Generate PROJECT_MAP.md overview for a directory |
| [Claude Code HUD](./Claude%20Code%20HUD) | Terminal status bar for context usage and agent state |
| [Alipay Booking](./alipay-booking) | Convert Alipay CSV statements to bookkeeping Excel |
| [System Study](./system-study) | Research a topic and produce structured HTML learning materials |
| [Audience Adapter](./audience-adapter) | Tailor reports and updates by audience role (CEO / VP / Tech / Ops) |
| [SOP Writer](./sop-writer) | Turn a process description into a full SOP with RACI and flowchart |
| [Work Report Writer](./work-report-writer) | Generate weekly/monthly reports from notes and git log |
| [MP Article Writer](./mp-article-writor) | Turn notes into polished WeChat/Sspai articles with style check |
| [Resume Optimizer](./resume-optimizer) | Professional resume optimization, supports text/Word/PDF input, JD matching, outputs Word+PDF+report |

> 📚 See [EXAMPLES.md](./EXAMPLES.md) for usage examples.

### 🚀 Quick Start

```bash
cd ~/.claude/skills/
git clone https://github.com/Chris-zixuan/zixuan_Agenthub.git
```

### 📄 License

[MIT License](./LICENSE)

---

Made with ❤️ by Chris-zixuan
