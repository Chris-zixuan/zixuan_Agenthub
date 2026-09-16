---
name: obsidian
description: 'Obsidian 知识库统一操作入口，按意图分三层路由。① 工具层——用官方 CLI 移动/重命名笔记（自动更新全库 wikilink）、读写 frontmatter 属性、搜索、查断链与孤立页；② 分析层——全库体检与整体分析，拆子集并行分析 + 量化扫描，产出结构化报告；③ 运维层——每日日志写完后的一键增量维护（frontmatter 补全、项目任务快照、index.md 更新、项目活跃度、交叉引用发现）。触发词：移动/重命名笔记、批量改属性、查断链/孤页、搜索笔记、命令行操作 Obsidian、分析整个知识库、知识库体检、梳理库结构与空白、找重复和陈旧内容、生成知识库分析报告、vault audit、更新知识库、同步知识库、更新我的知识库、交叉引用、知识发现、项目活跃度检查、健康看板扫描。工作空间为用户的 Obsidian 知识库。'
agent_created: true
skill_path: "Mac: /Users/yangzixuan/个人项目/zixuan_Agenthub/skills/obsidian；Windows: D:/个人项目/zixuan_Agenthub/skills/obsidian"
---

# Obsidian 知识库操作

三层合一的统一入口：一个 skill 同时覆盖「用 CLI 操作库」「分析整个库」「维护库」三类工作，按意图分流到对应 reference。

## ⚠️ 第一原则：规则以库内权威源为准

知识库的完整规范只有一份：**`9_系统/协作约定.md`**（库内唯一权威源）。

`AGENTS.md` 只是它的**执行摘要** —— AGENTS.md 开篇即声明「两者若冲突，以 [[协作约定]] 为准」。

因此：涉及**标签词表、frontmatter 字段字典、目录归属、模板体系、链接与附件规范、移动铁律**时，一律现场读 `9_系统/协作约定.md`，**不要依赖本 skill 任何文件里的转述**。

本 skill 的 references 刻意只保留「协作约定里没有、但执行时需要」的内容。历史上正是因为内嵌了一份词表副本，副本漂移后导致 skill 拿**已废弃的标签**往日记里写数据 —— 不要再复制规则。

## 意图路由

| 用户意图 / 触发词 | 层 | 读这个 reference |
|---|---|---|
| 移动、重命名笔记；批量改属性；搜笔记；查断链/孤页/标签；命令行操作 Obsidian | 工具层 | `references/cli-reference.md` |
| 分析整个知识库、**知识库体检**、vault audit、梳理库结构与空白、找重复和陈旧内容、生成分析报告 | 分析层 | `references/vault-audit.md` |
| 更新知识库、同步知识库、交叉引用、知识发现、项目活跃度检查、健康看板扫描 | 运维层 | `references/kb-maintenance.md` |
| 查目录结构、字段定义、PM 项目结构、Dataview 模板、index.md 归属 | 参考 | `references/vault-spec.md` |

**三层按写权限划分，互不重叠**：

- **工具层** = 单次操作，直接执行
- **分析层** = **只读**。只出报告与建议，绝不改文件
- **运维层** = **读写**。但只改 frontmatter 与索引文件，且改动前先报告

> **「知识库体检」vs「健康看板扫描」** —— 两个词很容易混，行为差别很大：
> - **知识库体检** → 分析层。全库深度分析，拆子集派并行子代理，产出 HTML 报告。**重**
> - **健康看板扫描** → 运维层。基于 `9_系统/Dashboard/知识库健康度.md` 的既有维度快速扫描，纯文本输出。**轻**

## 三层共通硬约束

### 1. CLI 安全红线：无参数即执行

大部分 `obsidian` 命令**没有 `--help`，无参数调用会直接执行默认行为** —— 裸调 `create` 会新建 `Untitled.md`，裸调 `delete` 会把**当前活跃文件**移入回收站。

- **永远显式传 `path=` 或 `file=`**，不要裸调命令
- 查命令名列表用 `obsidian --help`
- 有副作用的命令格外谨慎：`delete` `move` `rename` `property:set|remove` `plugin:*` `theme:*` `snippet:*` `restart` `eval` `sync` `daily:*`
- 删除是**移入系统回收站**（macOS 默认 `~/.Trash/`），不是库内 `.trash/`，可恢复

### 2. 协作边界（摘自 `9_系统/协作约定.md` §1，冲突时以该文件为准）

**AI 绝不触碰**：`4_项目/` 下 pm 插件的管控文件；`0_Inbox/Clippings/`；`.obsidian/`。

**需用户确认才执行**：批量重命名 / 移动（≥3 个文件，或涉及目录调整）；修改 `9_系统/` 下的规则文件、模板与索引；删除任何既有笔记；改字段名或标签词表。

**可直接执行**：补 frontmatter 缺失字段、修断链补 wikilink、单篇笔记的重命名与排版清理。

### 3. 备份与复核

- 批量改动或修改 `9_系统/` 前，先备份到库内 `.workbuddy/backups/{日期}/`
- 移动 / 重命名后必须复核：`obsidian unresolved | grep "旧名"` —— 无输出才算干净（刚改完可能因索引未重建而误报，等 1–3 秒再查）
- 中文名 / 含空格路径一律加引号
- **不要退化成 `mv`** —— CLI 不可用时改在 Obsidian 界面操作

## 库的关键路径

| 用途 | 路径 |
|---|---|
| 库根（Mac） | `~/Documents/Obsidian/我的知识库` |
| 库根（Windows） | `C:\Users\yangz\Nutstore\1\Obsidian\我的知识库` |
| 权威规范 | `9_系统/协作约定.md`（摘要：`AGENTS.md`） |
| 用户精选入口 | `index.md` |
| 全量导航 / 主题聚合 | `9_系统/MOC/知识库总索引.md`、`主题索引.md` |
| 健康看板 | `9_系统/Dashboard/知识库健康度.md` |
| PM 项目 | `4_项目/{项目名}/` |
| 每日日志 | `1_日志/YYYY/YYYY-MM-DD.md` |
| 分析报告留存 | `9_系统/`（历史报告在此） |

双机部署（Mac / Windows），运行时先探测 OS，再确认路径是否存在；均不存在时询问用户。

> **总索引与主题索引是 Dataview 动态生成的，免维护**。人工写入会被下次渲染覆盖 —— 不要去「维护」它们（这是本 skill 从旧版本继承下来最需要记住的一条）。

## 分层说明

**工具层** → `references/cli-reference.md`
官方 CLI 的启用前提、`key=value` 语法、六大类命令（移动 / 属性 / 体检 / 搜索 / 写入 / 其它）、常见坑速查。这是另外两层的基础能力。

**分析层** → `references/vault-audit.md`
四步法：侦察 → 拆子集派并行子代理 → 主代理跑量化扫描 → 汇总报告。产出 `知识库整体分析报告-YYYY-MM-DD.md` + 同名 HTML。含用真实代价换来的踩坑纪律（尤其 `tags` 必须按四态解析、计数必须换第二种方法复算）。

**运维层** → `references/kb-maintenance.md`
日志写完后的一键增量维护。**注意它不做总索引 / 主题索引维护** —— 见上文。

**参考** → `references/vault-spec.md`
库规范里没有、但 skill 执行需要的内容：Project Manager 的目录与字段结构、Dataview 查询模板、index.md 归属映射。
