# 参考 · 库规范指针 + skill 侧补充

> 本文件最后核对：2026-09-16（对照 `9_系统/协作约定.md` 逐节核实）

## 权威源：`9_系统/协作约定.md`

知识库规范的**唯一权威源**是 `9_系统/协作约定.md`（库内文件）。

`AGENTS.md` 只是它的**执行摘要** —— AGENTS.md 开篇即声明：「本文件是执行摘要。完整的模板定义、属性字段字典、标签词表与移动铁律见 [[协作约定]]。**两者若冲突，以 [[协作约定]] 为准**。」

### 已迁出本文件的内容（不再重复）

| 内容 | 现在去哪看 |
|---|---|
| 三层结构与协作边界 | 协作约定 §0、§1 |
| 模板体系（每日记录 / 知识笔记 / 项目模板） | §2 |
| 属性字段字典（`类型` / `状态` 值域） | §3 |
| Tags 双域词表（技术域 9 + 个人域 5） | §4 |
| 链接与附件规范（含附件落位命名） | §5 |
| 移动与重命名铁律 | §6 |
| AI 的三种工作流 | §7 |
| 项目与日志规范 | §8 |
| LaTeX 排版规范 | 正文规则 |
| Clippings 属性规范 | §1.1（用户私域，Agent 不主动介入） |

> ⚠️ **为什么删**：这些内容本文件曾有副本，但副本没有同步机制。到 2026-09-16 核对时，副本里的标签词表已经漂移到会**拿废弃标签往日记里写数据**（还在用 `职业/跳槽`、`英语学习`、一级 `健身`，而权威源早已将其重映射为 `求职`、`英语`、`生活/健身`）。
>
> **要改规则，改 `9_系统/协作约定.md`，不要改这里。**

---

## 本文件保留什么

只保留权威源里**没有**、但 skill 执行时需要的四块：

1. 双机部署路径
2. Project Manager 的目录与字段结构（**读用**，不写）
3. Dataview 查询模板
4. index.md 的结构与归属映射

---

## 1. 双机部署路径

| 端 | 库根目录 |
|---|---|
| Mac | `/Users/yangzixuan/Documents/Obsidian/我的知识库` |
| Windows | `C:\Users\yangz\Nutstore\1\Obsidian\我的知识库` |

运行时先判断 OS（`uname` / `$OSTYPE`），再确认默认路径是否存在；均不存在时询问用户。

---

## 2. Project Manager 项目结构（读用）

项目全部由 obsidian-pm 插件（Project Manager）管理，数据为纯 Markdown + YAML frontmatter。
**所有 pm-project / pm-task 文件由插件独占管控，skill 只读不写。**

### 项目主文件（pm-project）

位置：`4_项目/{项目名}/{项目名}.md`，frontmatter 标记 `pm-project: true`。

```yaml
---
pm-project: true
id: "zgv4l9x1mrvrgm2a"
title: "延锋座椅检测项目"
description: "项目一句话描述"
color: "#8b72be"
icon: "📋"
taskIds: ["[[软件版本定制功能|软件版本定制功能]]", "[[新版本功能开发|新版本功能开发]]"]   # wikilink 列表，插件维护
customFields: []
teamMembers: ["杨子萱", "冯方"]
savedViews: []
createdAt: "2026-07-22T07:28:29.361Z"
updatedAt: "2026-08-12T08:35:30.867Z"
---
```

正文由插件同步渲染 `## Tasks` 任务列表（checkbox + wikilink），**skill 不得写入正文**。
项目状态可从 Tasks 勾选比例推断（项目看板采用此逻辑）。

### 任务文件（pm-task）

位置：`4_项目/{项目名}/_tasks/{任务名}.md`，frontmatter 标记 `pm-task: true`。

```yaml
---
pm-task: true
projectId: "[[延锋座椅检测项目|延锋座椅检测项目]]"   # wikilink 格式（非裸 id）
parentId:
id: ga1zh8humsi9vvwc
title: 撰写SOP
type: task                    # task / subtask / milestone
status: in-progress           # todo / in-progress / blocked / review / done / cancelled
priority: medium              # critical / high / medium / low
start: 2026-08-20
due: 2026-09-11
progress: 0                   # 0-100
assignees: []
tags: []
subtaskIds: []
dependencies: []
createdAt: 2026-08-07T01:35:10.908Z
updatedAt: 2026-09-07T03:52:01.529Z
---

Project: [[延锋座椅检测项目|延锋座椅检测项目]]
```

正文首行固定为 `Project: [[项目名|项目名]]`，**skill 不得改动**。

### 任务目录约定（`_tasks/`，位于项目目录内）

- 任务文件平铺在 `4_项目/{项目名}/_tasks/` 下，**文件名即任务标题**
  （注意：位于项目目录内，不是 `4_项目/{项目名}_tasks/`）
- `Archive/` —— 插件归档已完成 / 已取消任务
- `_others/` —— 手动项目文档，插件不碰
  - `项目总览.md`：`# 项目概述` / `# 里程碑` / `# 方案记录` / `# 进度记录` / `# 相关文档`（skill 可**建议**更新）
  - `进度记录.md`：仅 `# 日志` 段落 + Dataview 查询代码，**不手动写进度**

---

## 3. Dataview 查询模板

> 这些模板不在权威源里，是 skill 执行时用来核对结构 / 查询用的。

### 3.1 进度记录（`_others/进度记录.md` 内嵌）

从 `1_日志` 自动拉取 `## [[项目名]]` 二级标题段落内容，**不需要 skill 写入**：

```dataviewjs
const PROJECT = "延锋座椅检测项目";

const pages = dv.pages('"1_日志"')
    .where(p =>
        p.file.outlinks.some(l => l.path.includes(PROJECT))
    )
    .sort(p => p.file.name, "desc");

for (let page of pages)
{
    let content = await dv.io.load(page.file.path);
    let regex = new RegExp(
        `## \\[\\[${PROJECT}\\]\\]\\s*([\\s\\S]*?)(?=\\n# |\\n## |$)`
    );
    let match = content.match(regex);
    if (match)
    {
        dv.header(3, page.file.name);
        dv.paragraph(match[1]);
    }
}
```

### 3.2 项目日志关联查询

查某项目在日志中的全部记录（项目活跃度判定、交叉引用发现时可用）：

```dataviewjs
const proj = "项目名";
const pages = dv.pages('"1_日志"')
  .where(p => {
    const items = Array.isArray(p.项目) ? p.项目 : [p.项目];
    if (items.some(v => v && String(v).includes(proj))) return true;
    const outNames = p.file.outlinks.map(l => l.path);
    if (outNames.some(n => n.includes(proj))) return true;
    return false;
  })
  .sort(p => p.日期, 'desc');
dv.table(["日期", "项目", "总结"], pages.map(p => [
  p.file.link,
  Array.isArray(p.项目) ? p.项目.join(", ") : (p.项目 ?? "—"),
  p.总结 ?? "—"
]));
```

---

## 4. index.md 结构与归属映射

### 4.1 板块结构

```markdown
# 知识库入口

## 快速入口            ← 总索引/主题索引/项目看板/工作情况 MOC/项目管理日常指南/知识库健康度
## 当前重点
  ### 3D视觉与定位抓取
  ### 标定与数学基础
  ### 算子、脚本与工程经验
## 工作项目
  ### 进行中           ← 4_项目/ 下 pm 项目
  ### 归档项目          ← 1_归档项目/ 下旧 MOC
  ### 工作资料
## AI 与 Agent
## 开发工具与运维
## 个人成长
  ### 规划与职业
  ### 生活与关系
  ### 思考与阅读
## 写作与维护原则      ← 只放精选、全量交给总索引、Clippings 不列入
```

### 4.2 收录门槛与归属

**门槛**：只收录长期重要、高频使用、当前推进中的内容；不追求完整。全量导航由 `知识库总索引.md` 承担（Dataview 动态生成）。**Clippings 一律不收录**。

| 来源目录 | 目标板块 |
|---|---|
| `3_工作/工作知识库/5_理论知识/标定理论/` | 当前重点 → 标定与数学基础 |
| `3_工作/工作知识库/5_理论知识/定位与抓取/` | 当前重点 → 3D视觉与定位抓取 |
| `3_工作/工作知识库/5_理论知识/算法与数学/` | 当前重点 → 标定与数学基础 |
| `3_工作/工作知识库/5_理论知识/Opencv/` | 当前重点 → 算子、脚本与工程经验 |
| `3_工作/工作知识库/5_理论知识/PCL/` | 当前重点 → 3D视觉与定位抓取 |
| `3_工作/工作知识库/1_软件产品/` | 当前重点 → 算子、脚本与工程经验 |
| `3_工作/工作知识库/3_经验笔记/` | 当前重点 → 算子、脚本与工程经验 |
| `2_个人/经验/视觉算法/` | 当前重点（按内容归入对应技术小节） |
| `4_项目/{项目名}/`（pm 项目） | 工作项目 → 进行中 |
| `3_工作/项目管理/1_归档项目/` | 工作项目 → 归档项目 |
| `3_工作/项目管理/1_归档项目/` 下的工作资料 | 工作项目 → 工作资料 |
| `2_个人/经验/AI/` | AI 与 Agent |
| `2_个人/经验/开发工具/`、`2_个人/经验/网络运维/` | 开发工具与运维 |
| `2_个人/跳槽准备中/` | 个人成长 → 规划与职业 |
| `2_个人/生活/`（思考阅读类） | 个人成长 → 思考与阅读 |
| `2_个人/生活/`（生活事务类） | 个人成长 → 生活与关系 |
| `3_工作/英语学习/` | 个人成长 → 规划与职业（按主题实际归属） |
| `0_Inbox/Clippings/` | **不收录** |
