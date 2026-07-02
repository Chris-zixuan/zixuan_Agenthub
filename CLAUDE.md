# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库用途

这是 Chris-zixuan 的个人 Claude Code Skills 集合仓库（AgentHub）。仓库存放自定义 Skill 定义文件，安装到 `~/.claude/skills/` 后可在 Claude Code 中通过斜杠命令调用。

## 仓库目录结构

```
zixuan_Agenthub/
├── skills/               # Skill 定义目录（CC Switch 识别入口）
│   └── skill-name/       # 每个 Skill 一个独立子目录
│       ├── SKILL.md      # 必须，Skill 定义主文件（YAML frontmatter + 工作流 Markdown）
│       ├── references/   # 可选，供 Skill 在执行时 Read 的参考资料
│       ├── examples/     # 可选，代码示例或输出样本
│       ├── assets/       # 可选，脚本、模板等资源文件
│       └── scripts/      # 可选，可执行脚本
├── docs/                 # 非 Skill 资料（设计文档、变更日志、开发报告等）
└── Claude Code HUD/      # 插件/工具文档
```

### SKILL.md frontmatter 规范

```yaml
---
name: skill-name          # 必须，与目录名一致
description: "触发条件描述"  # 必须，Claude 用来判断何时自动触发
version: 1.0.0            # 可选
author: 作者名             # 可选
tags: [tag1, tag2]        # 可选
---
```

## 当前内容

| 目录 | 类型 | 说明 |
|------|------|------|
| `skills/memory-init/` | Skill | 一键部署记忆系统（CLAUDE.md + MEMORY.md + memory/） |
| `skills/organize/` | Skill | 扫描分类整理混乱目录，确认后执行 |
| `skills/visionmaster-scripthelper/` | Skill | HiVision VisionMaster C# 脚本开发辅助 |
| `skills/mvb-coco-annotation/` | Skill | 将图片目录自动转换为 MVB-COCO 格式分类数据集 |
| `skills/audience-adapter/` | Skill | 向上汇报/跨部门沟通，按受众角色自动调整信息粒度与语言风格 |
| `skills/sop-writer/` | Skill | 将业务流程梳理为含 RACI 矩阵和异常处理的完整 SOP 文档 |
| `skills/work-report-writer/` | Skill | 从零散工作记录与 git log 生成结构化周报或月报 |
| `skills/project-map-builder/` | Skill | 为指定目录生成 PROJECT_MAP.md 结构概览 |
| `skills/system-study/` | Skill | 给定领域/技术，自主调研并产出结构化 HTML 学习材料 |
| `skills/mp-article-writor/` | Skill | 将素材整理为公众号/少数派长文，含行文自检与配图 prompt |
| `skills/resume-optimizer/` | Skill | 专业简历优化与生成，支持文本/Word/PDF输入，结合JD定制，输出Word+PDF+质量报告 |
| `docs/` | 资料 | Skill 开发过程中的设计文档、变更日志、质量报告等非运行时资料 |
| `Claude Code HUD/` | 文档 | HUD 状态栏插件安装与配置说明 |

## 安装到本地

### 方式一：CC Switch 一键安装（推荐）

在 CC Switch → 扩展 → Skills 中添加仓库：
- Owner: `Chris-zixuan`
- Name: `zixuan_Agenthub`
- Branch: `main`
- Subdirectory: `skills`

### 方式二：手动安装

```bash
cd ~/.claude/skills/
git clone https://github.com/Chris-zixuan/zixuan_Agenthub.git
# 把 skills/ 下的子目录软链接到 Claude Code skills 目录
for d in zixuan_Agenthub/skills/*/; do ln -s "$(pwd)/$d" "./$(basename $d)"; done
```

安装后在 Claude Code 中通过 `/skill-name` 调用，或用自然语言描述触发。

## 添加新内容

- **Skill**：在 `skills/` 下新建目录 `skill-name/`，编写 `SKILL.md`（frontmatter 中 `name` 和 `description` 必填）
- **开发资料**：与 Skill 开发相关但非运行时需要的文档（设计稿、变更日志等）放入 `docs/<skill-name>/`
- **插件/工具文档**：在根目录新建目录，放入说明文档即可

## 更新文档的工作流

当用户要求「更新」或「同步文档」时，按以下步骤执行：

1. **扫描仓库**：用 `Glob` 列出所有子目录，找到包含 `SKILL.md` 的目录以及其他有说明文档的目录
2. **对比现有 README**：检查 [README.md](./README.md) 总览表格，找出新增或已删除的条目
3. **更新 README.md**：在对应分类表格中增删条目，只写 Skill 名和一句话说明，详情不放 README
4. **更新 EXAMPLES.md**：为新增的 Skill/插件补充使用示例（参考 [EXAMPLES.md](./EXAMPLES.md) 已有格式：场景标题 + 对话示例 + 预期输出）；删除已移除内容对应的示例
5. **两个文件保持同步**：README 的总览条目与 EXAMPLES 的示例章节一一对应
