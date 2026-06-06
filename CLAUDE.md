# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库用途

这是 Chris-zixuan 的个人 Claude Code Skills 集合仓库（AgentHub）。仓库存放自定义 Skill 定义文件，安装到 `~/.claude/skills/` 后可在 Claude Code 中通过斜杠命令调用。

## Skill 文件结构

每个 Skill 是一个独立目录，目录名即为 Skill 名（斜杠命令名）：

```
skill-name/
├── SKILL.md          # 必须，Skill 定义主文件（YAML frontmatter + 工作流 Markdown）
├── references/       # 可选，供 Skill 在执行时 Read 的参考资料
├── examples/         # 可选，代码示例或输出样本
└── assets/           # 可选，脚本、模板等资源文件
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
| `memory-init/` | Skill | 一键部署记忆系统（CLAUDE.md + MEMORY.md + memory/） |
| `organize/` | Skill | 扫描分类整理混乱目录，确认后执行 |
| `visionmaster-scripthelper/` | Skill | HiVision VisionMaster C# 脚本开发辅助 |
| `mvb-coco-annotation/` | Skill | 将图片目录自动转换为 MVB-COCO 格式分类数据集 |
| `audience-adapter/` | Skill | 向上汇报/跨部门沟通，按受众角色自动调整信息粒度与语言风格 |
| `sop-writer/` | Skill | 将业务流程梳理为含 RACI 矩阵和异常处理的完整 SOP 文档 |
| `work-report-writer/` | Skill | 从零散工作记录与 git log 生成结构化周报或月报 |
| `project-map-builder/` | Skill | 为指定目录生成 PROJECT_MAP.md 结构概览 |
| `system-study/` | Skill | 给定领域/技术，自主调研并产出结构化 HTML 学习材料 |
| `alipay-booking/` | Skill | 一键将支付宝交易流水 CSV 整理为随手记记账 Excel |
| `mp-article-writor/` | Skill | 将素材整理为公众号/少数派长文，含行文自检与配图 prompt |
| `Claude Code HUD/` | 文档 | HUD 状态栏插件安装与配置说明 |
| `参考README.md` | 参考 | 完整 Skills 集合（yunshu0909/yunshu_skillshub）总览，新增 Skill 时参考其结构和分类方式 |

## 安装到本地

```bash
cd ~/.claude/skills/
git clone <repo-url>
```

安装后在 Claude Code 中通过 `/skill-name` 调用，或用自然语言描述触发。

## 添加新内容

- **Skill**：新建目录 `skill-name/`，编写 `SKILL.md`（frontmatter 中 `name` 和 `description` 必填）
- **插件/工具文档**：新建目录，放入说明文档即可

## 更新文档的工作流

当用户要求「更新」或「同步文档」时，按以下步骤执行：

1. **扫描仓库**：用 `Glob` 列出所有子目录，找到包含 `SKILL.md` 的目录以及其他有说明文档的目录
2. **对比现有 README**：检查 [README.md](./README.md) 总览表格，找出新增或已删除的条目
3. **更新 README.md**：在对应分类表格中增删条目，只写 Skill 名和一句话说明，详情不放 README
4. **更新 EXAMPLES.md**：为新增的 Skill/插件补充使用示例（参考 [EXAMPLES.md](./EXAMPLES.md) 已有格式：场景标题 + 对话示例 + 预期输出）；删除已移除内容对应的示例
5. **两个文件保持同步**：README 的总览条目与 EXAMPLES 的示例章节一一对应
