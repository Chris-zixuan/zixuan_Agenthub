# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库用途

这是 Chris-zixuan 的个人 Agent Skills 集合仓库（AgentHub），服务于 Claude Code 与 WorkBuddy。仓库存放自定义 Skill 定义文件，安装到 `~/.claude/skills/` 或 `~/.workbuddy/skills/` 后即可通过斜杠命令或自然语言调用。

仓库同时是多设备（Windows / macOS）Skill 的统一收敛点：各处 skill 的真身都放在本仓库，各端只做软链接或复制，避免版本分叉。

## 仓库目录结构

```
zixuan_Agenthub/
├── skills/               # Skill 定义目录（CC Switch 识别入口）
│   └── skill-name/       # 每个 Skill 一个独立子目录
│       ├── SKILL.md      # 必须，Skill 定义主文件（YAML frontmatter + 工作流 Markdown）
│       ├── references/   # 可选，供 Skill 在执行时 Read 的参考资料
│       ├── examples/     # 可选，代码示例或输出样本
│       ├── assets/       # 可选，模板、资源文件
│       └── scripts/      # 可选，可执行脚本
└── Claude Code HUD/      # 插件/工具文档
```

> `_templates/`、`docs/` 为按需创建的可选目录（Skill 脚手架、开发资料），当前仓库中不存在，不要凭空引用。

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
| `skills/visionmaster-scripthelper/` | Skill | HiVision VisionMaster C#/Python 脚本开发辅助 |
| `skills/organize/` | Skill | 扫描分类整理混乱目录，确认后执行 |
| `skills/workbuddy-auto-checkin/` | Skill | WorkBuddy「Buddy 加油站」每日签到自动化（接口直签 + 定时任务） |
| `skills/yzx-obsidian/` | Skill | Obsidian 知识库三层合一：官方 CLI 操作 / 全库体检分析 / 日志增量维护 |
| `skills/weekly-report-pdca/` | Skill | 结果导向 + PDCA 闭环的中文研发周报（先 Markdown 后 HTML） |
| `skills/audience-adapter/` | Skill | 向上汇报/跨部门沟通，按受众角色自动调整信息粒度与语言风格 |
| `skills/sop-writer/` | Skill | 将业务流程梳理为含 RACI 矩阵和异常处理的完整 SOP 文档 |
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

### WorkBuddy 用户

WorkBuddy 读取 `~/.workbuddy/skills/`。**本仓库的 skill 一律用软链接安装**，保证单一真源 —— 改仓库即全局生效，不会产生本地副本分叉：

```bash
ln -s "/Users/<user>/个人项目/zixuan_Agenthub/skills/workbuddy-auto-checkin" ~/.workbuddy/skills/workbuddy-auto-checkin
```

## 安装方式：按来源区分（硬规则）

`~/.workbuddy/skills/` 下会同时存在不同来源的 skill，**不要一刀切**：

| 来源 | 判定依据 | 安装方式 |
|------|----------|----------|
| **本仓库** | SKILL.md frontmatter 含 `skill_path` 指向 Agenthub | **软链接**（`ln -s`） |
| **WorkBuddy 市场** | 目录内含 `_skillhub_meta.json`（`"source": "marketplace"`） | **真实目录**，不得改软链接 |
| **本机 agent 创建、尚未入库** | 有 `agent_created: true` 但无 `skill_path` | 暂保持真实目录；收编入库后改软链接 |

> 判定**必须看引用关系（`skill_path` / `_skillhub_meta.json`），不能只看目录名**。
>
> 市场安装的 skill 由市场机制维护，改成软链接会被后续更新破坏。

**收编流程**：把本机 agent 创建的 skill 移入 `skills/` → 补齐前文 frontmatter 规范（含 `skill_path`）→
同步 README / EXAMPLES / CLAUDE 三处 → 提交推送 → 把本机 `~/.workbuddy/skills/<name>` 换成指向仓库的软链接。

## 改名 / 删除 Skill 的引用点清单（务必逐项过）

改一个 Skill 的名字或删掉它，波及范围**远超出仓库** —— 只改目录名必然留下死引用。
按下面逐项核对（清单来自 2026-09-16 `obsidian` → `yzx-obsidian` 改名的实际教训）：

| # | 引用点 | 说明 |
|---|--------|------|
| 1 | 目录名 与 `frontmatter.name` | 两者必须一致；且须匹配 `^[a-z0-9-]+$`（见下） |
| 2 | `frontmatter.skill_path` | Mac 与 Windows **两条路径都要改** |
| 3 | `README.md` | **中英文两张表都要改** —— 英文表最易漏 |
| 4 | `EXAMPLES.md` | 章节标题 + 末尾斜杠命令清单 |
| 5 | `CLAUDE.md` | 上文「当前内容」表 |
| 6 | 本机软链接 | 旧链接移入回收站（`trash`，不用 `rm`），重建为新名 |
| 7 | **WorkBuddy 自动化任务** | prompt 里常写死 skill 文件绝对路径 —— **最易漏，且到点才爆** |
| 8 | `~/.workbuddy/MEMORY.md` | 长期记忆中记录的 skill 路径 |
| 9 | 其他 Skill 的交叉引用 | 在仓库内 grep 旧名（当前无此类引用，需保持） |

**验证方式**（三条都要跑，缺一不可）：

```bash
# 1. 仓库内旧名残留（0 命中才算干净）
grep -rn "skills/<old>" . --include="*.md"

# 2. 本机软链接解析正常
ls -l ~/.workbuddy/skills/<new>

# 3. 自动化任务的引用 —— 无批量检索手段，只能逐个 view 核对 prompt
```

> ⚠️ **macOS 的 `grep` 是 BSD 版，不支持 BRE 的 `\|` 或运算** —— `grep "a\|b"` 会静默返回空结果（exit 1），
> 极易据此误判「已无残留」。一律用 `grep -E "a|b"`。
>
> ⚠️ 同理，**改完文件要用 `sed -n 'Np'` 或 grep 复核落盘结果**，不要只信编辑工具的「成功」返回。

### Skill 命名规范

`name` 与目录名**必须以小写字母、数字、连字符组成**（`^[a-z0-9-]+$`），且不得以连字符开头/结尾或含连续连字符。

- 依据：`skill-creator` 插件的 `scripts/quick_validate.py` 会据此校验，驼峰（如 `YzxObsidian`）判不合格。
- 实际影响：WorkBuddy 加载期**未发现**格式校验（驼峰大概率能加载），但会破坏官方打包/市场分发流程，且与全生态（内置 26 个 + 市场 + 本机）命名风格脱节。

## 添加新内容

- **Skill**：在 `skills/` 下新建目录 `skill-name/`，编写 `SKILL.md`（frontmatter 中 `name` 和 `description` 必填，`name` 必须与目录名一致）
- **脚本**：随 Skill 使用的可执行脚本放入该 Skill 的 `scripts/` 子目录，并在 SKILL.md 中用相对路径引用
- **模板**：Skill 脚手架模板放入 `_templates/`（按需创建）
- **开发资料**：与 Skill 开发相关但非运行时需要的文档（设计稿、变更日志等）放入 `docs/<skill-name>/`（按需创建）
- **插件/工具文档**：在根目录新建目录，放入说明文档即可

排查建议：仓库根有一份 `.gitignore`，Skill 运行期产生的状态文件（如日志、本机配置）应追加进去，不要提交。

## 更新文档的工作流

当用户要求「更新」或「同步文档」时，按以下步骤执行：

1. **扫描仓库**：用 `Glob` 列出所有子目录，找到包含 `SKILL.md` 的目录以及其他有说明文档的目录
2. **对比现有 README**：检查 [README.md](./README.md) 总览表格，找出新增或已删除的条目
3. **更新 README.md**：在对应分类表格中增删条目，只写 Skill 名和一句话说明，详情不放 README
4. **更新 EXAMPLES.md**：为新增的 Skill/插件补充使用示例（参考 [EXAMPLES.md](./EXAMPLES.md) 已有格式：场景标题 + 对话示例 + 预期输出）；删除已移除内容对应的示例
5. **两个文件保持同步**：README 的总览条目与 EXAMPLES 的示例章节一一对应
