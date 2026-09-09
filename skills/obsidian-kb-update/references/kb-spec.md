# Obsidian 知识库规范参考

> 双机部署：Mac 根目录 `/Users/yangzixuan/Documents/Obsidian/我的知识库`；Windows 根目录 `C:\Users\yangz\Nutstore\1\Obsidian\我的知识库`。运行时先探测 OS 再确认路径。下文路径均相对知识库根目录。

## 目录结构

```
0_Inbox/                    收集区
  Attachments/              空（预留）
  Clippings/                网页剪藏笔记（知乎/博客/文章，用户自行收集整理，Agent 默认不介入）
    assets/                 剪藏附件
  Fleeting/                 空（闪念笔记预留）
  douyin/                   douyin-to-obsidian 项目输出（抖音内容收集）
1_日志/                     时间线
  2024/2025/2026/           按年归档的每日日志（YYYY-MM-DD.md，另有周记 YYYY-Wxx.md）
2_个人/                     个人资产（跨公司通用）
  生活/                     健身/阅读/人生思考/家庭
  经验/                     AI/开发工具/网络运维/视觉算法
  跳槽准备中/               简历/面试/英语/离职分析
3_工作/                     工作知识（与公司/项目绑定）
  工作文件/                  空（预留）
  工作知识库/                知识体系
    1_软件产品/              VM2D/VM3D/二次开发/常用脚本/框架软件/算子参考
    2_解决方案/              空（预留）
    3_经验笔记/              C++/C#/WPF/内存管理/PDF导出
    4_工作备忘/              软件打包/加密狗/系统工具
    5_理论知识/              标定理论/定位抓取/算法数学/Cpp/CSharp/Opencv/PCL/WPF/AI与LLM/设计模式/通讯电气/开发工具/Helix
  机器视觉2D定位抓取知识库/    2D 定位抓取个人知识库（主题版 + 工程模型版）
  英语学习/                  英语学习相关笔记
  项目管理/
    1_归档项目/              已归档旧 MOC 项目（每个项目一个目录，内含 xxxMOC.md 主文件 + 项目日志 + 会议记录）
4_项目/{项目名}/             Project Manager（obsidian-pm）项目管理，每项目一个目录
  {项目名}.md                项目主文件（pm-project: true，插件全权管控，禁止手动修改）
  _tasks/                    任务目录（注意：位于项目目录内，不是 4_项目/{项目名}_tasks/）
    {任务名}.md              pm-task 任务文件（插件全权管控）
    Archive/                已完成/已取消任务归档
    _others/                手动项目文档（插件不碰）
      项目总览.md            概述 + 里程碑 + 方案记录 + 重难点 + 相关文档（skill 可建议更新）
      进度记录.md            仅含 # 日志 段落 + 一段 Dataview 查询代码（自动从日记拉取，不手动写进度）
      其他笔记.md            Spoke 文档
8_附件/                     附件集中管理（按日期/主题混合命名；含 _orphan_backup_* 孤儿附件备份目录）
9_系统/                     元数据层
  Dashboard/                 知识库健康度看板（知识库健康度.md：缺总结/缺 tags/孤立笔记/最近修改）
  MOC/                      系统级内容地图（项目看板/项目管理日常指南/2026年工作情况 MOC；知识库总索引、主题索引规划中）
  模板/                     笔记模板：今日记录、知识笔记模板、项目笔记模板、理论知识、知识经验、Dataview查询模板、默认新建
  看板/                     任务清单、tasksCalendar
index.md                    知识库 MOC 精选入口（用户用，只放长期重要/高频内容，全量导航见知识库总索引）
AGENTS.md                   Agent 协作规范（目录约定、标签词表、编辑边界）
家庭宪法.md                  家庭根本大法
```

## 每日记录 Frontmatter 规范

```yaml
---
日期: YYYY-MM-DD
类型: 每日记录
tags: [开发工具]           # 1-4 个，从词表选择
项目: []        # 列表，如 [延锋座椅检测项目, 大3D项目支持]
总结:           # 一句话概括今天
---
```

### tags 标签词表

#### 工作领域标签（每日记录和项目笔记）

| 标签 | 覆盖范围 | 关键词匹配 |
|------|---------|-----------|
| 3D视觉 | 点云、3D匹配、3D定位、深度图 | 点云 / 3D匹配 / 3D定位 / 深度 |
| 定位抓取 | 机器人抓取、上下料 | 抓取 / 机器人 / 上下料 / 定位 |
| 标定 | 手眼标定、相机标定、TCP标定 | 标定 / 手眼 / 内外参 / 张正友 |
| 缺陷检测 | 焊缝、铸造、表面检测 | 焊缝 / 铸造 / 缺陷 / 检测 |
| 算法 | 优化算法、线性代数 | 算法 / 优化 / 梯度 / SVD |
| AI | Agent、Claude Code、LLM | Claude / Agent / Skill / LLM / AI / LangChain |
| 开发工具 | IDE、脚本、环境配置 | VM / 脚本 / C# / IDE / 环境 |
| 网络运维 | 远程桌面、代理、服务器 | 远程 / 代理 / 服务器 / 网络 |

#### 个人/生活标签（仅用于每日记录；知识笔记不使用）

| 标签 | 覆盖范围 | 关键词匹配 |
|------|---------|-----------|
| Obsidian | 知识管理、笔记整理 | Obsidian / 知识库 / 笔记 |
| 英语学习 | 英语、背单词、口语 | 背单词 / 墨墨 / 英语 / 口语 / English |
| 职业/跳槽 | 跳槽、面试、简历、职业规划 | 简历 / 面试 / 跳槽 / 离职 / 华睿 / offer |
| 健身 | 健身、运动记录 | 健身 / 跑步 / 深蹲 / 体重 / 有氧 |
| 生活 | 生活记录、个人事件 | 尤佳欣 / 约会 / 吵架 / 生活 |

#### 标签命名规则
- **知识笔记 tags**：使用 AGENTS.md 封闭词表（一级：3D视觉、定位抓取、标定、缺陷检测、算法、AI、开发工具、网络运维、Obsidian；至少 1 个、不超过 4 个；允许必要二级如 `标定/手眼标定`）；`类型`、`项目`、`状态` 写 frontmatter 字段，不进 tags
- **每日记录 tags**：允许上表工作领域 + 个人/生活两套词表
- 领域标签用 `/` 表示层级关系：如 `职业/跳槽`、`AI/LangGraph`
- 编程语言用具体技术名称：`cpp`、`Python`、`CSharp`

## 每日记录正文结构

```
# 工作记录
## [[笔记或项目名]]        ← 二级标题 + wikilink（AGENTS.md 规范：项目记录用此格式）
- 具体内容...
---
# 英语学习       （可选段落）
- [x] 背单词
---
# 生活记录
- 早上：/ 中午：/ 下午：/ 晚上：
---
# 健身记录       （可选段落）
---
# 所思所想
---
# 附件
```

- `# 工作记录` 下的条目用 `## [[xxx]]` 二级标题（指向项目或笔记），内容用列表项
- 非首个一级标题前必须有 `---` 分隔符
- 段落顺序不严格固定：有英语学习任务的日子为 工作 → 英语 → 生活 → 健身 → 所思 → 附件；否则省略英语段

## 分类原则

- `2_个人/`：不管在哪家公司都有用的知识（经验、AI、开发工具、生活）
- `3_工作/`：跟具体公司/项目绑定的知识（项目笔记、理论知识、工作文件）
- 两者之间靠 wikilink 桥接

## Project Manager 项目结构规范

项目全部由 obsidian-pm 插件（Project Manager）管理，数据存为纯 Markdown + YAML frontmatter。**所有 pm-project / pm-task 文件完全由插件管控，skill 只读不写。**

### 项目主文件（pm-project）

位置：`4_项目/{项目名}/{项目名}.md`（每项目一个同名目录），frontmatter 标记 `pm-project: true`。

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

正文由插件同步渲染 `## Tasks` 任务列表（checkbox + wikilink），**skill 不得写入正文**。项目状态可从 Tasks 勾选比例推断（项目看板采用此逻辑）。

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

正文首行固定为 `Project: [[项目名|项目名]]`，skill 不得改动。

### 任务目录约定（`_tasks/`，位于项目目录内）

- 任务文件平铺在 `4_项目/{项目名}/_tasks/` 下，文件名即任务标题
- `Archive/`：插件归档已完成/已取消任务
- `_others/`：手动项目文档，插件不碰
  - `项目总览.md`：概述 + 里程碑 + 方案记录 + 重难点 + 相关文档（**skill 可建议更新**）
  - `进度记录.md`：仅 `# 日志` 段落 + Dataview 自动查询代码，**不手动写进度**

### 进度记录（Dataview 自动拉取）

`_others/进度记录.md` 内嵌 dataviewjs，从 `1_日志` 自动拉取 `## [[项目名]]` 二级标题段落内容，**不需要 skill 写入**：

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

### 项目活跃度判定（skill Step 8 使用）

- 项目最后活动日期 = 日志中最近一次提及该项目的日期（`1_日志/` 中 `## [[项目名]]` 段落或 frontmatter `项目` 字段包含项目名的日记）
- 任务动态参考：项目下 pm-task 的 `updatedAt` 最新值
- 无任何日志提及 → 报告"无法判定活跃度"

## 项目日志关联查询模板

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

## 主题 MOC 查询模板

```dataviewjs
const tag = "标定";
const pages = dv.pages('"1_日志"')
  .where(p => {
    const items = Array.isArray(p.tags) ? p.tags : [p.tags];
    return items.some(v => v && String(v).includes(tag));
  })
  .sort(p => p.日期, 'desc');
dv.table(["日期", "项目", "总结"], pages.map(p => [
  p.file.link,
  Array.isArray(p.项目) ? p.项目.join(", ") : (p.项目 ?? "—"),
  p.总结 ?? "—"
]));
```

## index.md 结构（精选入口式）

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

### index.md 收录与归属规则

**收录门槛**：只收录长期重要、高频使用、当前推进中的内容；不追求完整，全量导航由知识库总索引承担。Clippings 一律不收录。

| 来源目录 | 目标板块 |
|---------|---------|
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
| `2_个人/经验/AI/` | AI 与 Agent |
| `2_个人/经验/开发工具/`、`2_个人/经验/网络运维/` | 开发工具与运维 |
| `2_个人/跳槽准备中/` | 个人成长 → 规划与职业 |
| `2_个人/生活/`（思考阅读类） | 个人成长 → 思考与阅读 |
| `2_个人/生活/`（生活事务类） | 个人成长 → 生活与关系 |
| `3_工作/英语学习/` | 个人成长 → 规划与职业（按主题实际归属） |

## Clippings 属性规范（位于 `0_Inbox/Clippings/` 下）

```yaml
---
类型: clippings
clipping_type: zhihu-answer/zhihu-article/zhihu-pin/blog/twitter-thread/article
title:
source:
author:
发布时间:
创建时间:
总结:         # 必填
tags: []      # 必填，从词表选
---
```

Clippings 由用户自行收集和整理，Agent 默认不主动补全或整理；仅当用户点名某篇或明确要求处理时才介入。不进 index.md。

## LaTeX 排版规范

行内公式 `$` 符号与公式内容之间不允许有空格。
- 正确：`$\mathbf{A}\mathbf{x}=\mathbf{b}$`
- 错误：`$ \mathbf{A}\mathbf{x}=\mathbf{b} $`

## 已知规则

- 附件策略：本地存储，不用图床。Custom Attachment Location 插件：`8_附件/${noteFileName}`
- 整理笔记时必须保留原始图片引用格式，不可修改
- wikilink 使用短名格式 `[[笔记名]]`，Obsidian 自动解析路径
- skills 真身托管：GitHub 私有仓库 `Chris-zixuan/zixuan_Agenthub`（`skills/` 目录），Mac 克隆于 `/Users/yangzixuan/个人项目/zixuan_Agenthub`，Windows 克隆于 `D:/个人项目/zixuan_Agenthub`，通过 npx skills 分发到各机器/各 agent
- 项目与任务管理统一由 Project Manager 插件（obsidian-pm）负责；`4_项目/` 下插件管控文件 skill 只读不写
- 项目进度记录由 Dataview 自动从日志拉取，skill 不手动写入进度
- 周报生成由独立 skill（weekly-report-pdca）负责
- AGENTS.md 是知识库协作规范权威来源；若本规范与 AGENTS.md 冲突，以 AGENTS.md 为准并反馈用户
- 批量修改前备份到知识库 `.workbuddy/backups/` 日期目录
- 知识库健康度看板位于 `9_系统/Dashboard/知识库健康度.md`；`9_系统/MOC/知识库总索引.md` 与 `主题索引.md` 规划中（AGENTS.md/index.md 已引用，尚待创建）
