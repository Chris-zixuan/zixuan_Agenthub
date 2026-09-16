# Zixuan 的 Agent 工具箱 / Zixuan's Agent Toolkit

[English](#english) | [中文](#中文)

---

## 中文

### 📖 简介

这是我个人收集整理的 Agent Skills 与插件集合，记录我在日常使用 Claude Code / WorkBuddy 过程中沉淀下来的好用工具。
仓库同时承担「多设备 Skill 统一收敛」的职责 —— Windows 与 macOS 上的 skill 都回收到这里，各端按需软链接安装。

### 📊 内容总览

目前共包含 **7 个 Skills** + **1 个插件文档**：

#### 💻 开发辅助

| Skill | 说明 |
|-------|------|
| [VisionMaster 脚本助手](./skills/visionmaster-scripthelper) | HiVision VisionMaster C#/Python 脚本开发辅助 |

#### 💼 效率工具

| Skill / 插件 | 说明 |
|--------------|------|
| [文件夹整理助手](./skills/organize) | 扫描分类、清理冗余，整理混乱目录 |
| [WorkBuddy 每日自动签到](./skills/workbuddy-auto-checkin) | 接口直签 Buddy 加油站每日签到，并创建 WorkBuddy 自带定时自动化 |
| [Claude Code HUD](./Claude%20Code%20HUD) | 终端实时状态栏，显示上下文用量与 Agent 状态 |

#### 🧠 知识管理

| Skill | 说明 |
|-------|------|
| [Obsidian 知识库操作](./skills/yzx-obsidian) | 三层合一：官方 CLI 操作笔记（自动更新 wikilink）/ 全库体检与整体分析 / 日志写完后的一键增量维护 |
| [周报生成 PDCA](./skills/weekly-report-pdca) | 结果导向 + PDCA 闭环的中文研发周报，先出 Markdown 再出 HTML |

#### ✍️ 写作与沟通

| Skill | 说明 |
|-------|------|
| [受众适配助手](./skills/audience-adapter) | 向上汇报/跨部门沟通，按受众角色自动调整信息粒度与语言风格 |
| [SOP 文档生成](./skills/sop-writer) | 将业务流程梳理为含 RACI 矩阵、流程图和异常处理的完整 SOP 文档 |

> 📚 每个 Skill 的详细使用示例见 [EXAMPLES.md](./EXAMPLES.md)

---

### 🚀 快速开始

```bash
cd ~/.claude/skills/
git clone https://github.com/Chris-zixuan/zixuan_Agenthub.git
# 把 skills/ 下的子目录软链接到 Claude Code skills 目录
for d in zixuan_Agenthub/skills/*/; do ln -s "$(pwd)/$d" "./$(basename $d)"; done
```

或在 CC Switch 中添加仓库（Owner: `Chris-zixuan`, Name: `zixuan_Agenthub`, Subdirectory: `skills`）一键安装。

WorkBuddy 用户可把需要的 skill 目录复制或软链接到 `~/.workbuddy/skills/`。

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

A personal collection of Agent Skills and plugins for Claude Code / WorkBuddy — tools I've accumulated through daily use.
The repo also serves as the single source of truth for skills scattered across my Windows and macOS machines.

### 📊 Overview

**7 Skills** + **1 plugin guide**:

| Skill / Plugin | Description |
|----------------|-------------|
| [VisionMaster Script Helper](./skills/visionmaster-scripthelper) | C#/Python script development for HiVision VisionMaster |
| [Organize](./skills/organize) | Scan, classify, and clean up messy folders |
| [WorkBuddy Auto Check-in](./skills/workbuddy-auto-checkin) | Direct-API daily check-in for WorkBuddy, plus a scheduled WorkBuddy automation |
| [Claude Code HUD](./Claude%20Code%20HUD) | Terminal status bar for context usage and agent state |
| [Obsidian Vault](./skills/yzx-obsidian) | Three layers: official CLI ops (auto-updates wikilinks) / full-vault audit / post-journal incremental maintenance |
| [Weekly Report PDCA](./skills/weekly-report-pdca) | Result-oriented Chinese dev weekly reports with a PDCA loop |
| [Audience Adapter](./skills/audience-adapter) | Tailor reports and updates by audience role (CEO / VP / Tech / Ops) |
| [SOP Writer](./skills/sop-writer) | Turn a process description into a full SOP with RACI and flowchart |

> 📚 See [EXAMPLES.md](./EXAMPLES.md) for usage examples.

### 🚀 Quick Start

```bash
cd ~/.claude/skills/
git clone https://github.com/Chris-zixuan/zixuan_Agenthub.git
for d in zixuan_Agenthub/skills/*/; do ln -s "$(pwd)/$d" "./$(basename $d)"; done
```

Or add in CC Switch (Owner: `Chris-zixuan`, Name: `zixuan_Agenthub`, Subdirectory: `skills`) for one-click install.

For WorkBuddy, copy or symlink the skill folders into `~/.workbuddy/skills/`.

### 📄 License

[MIT License](./LICENSE)

---

Made with ❤️ by Chris-zixuan
