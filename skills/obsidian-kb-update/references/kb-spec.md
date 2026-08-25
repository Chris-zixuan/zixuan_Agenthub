# Obsidian 知识库规范参考

## 目录结构

```
0_Inbox/                    收集区
  Clippings/                网页剪藏笔记（知乎/博客/文章）
    assets/                 剪藏附件
  Attachments/              空（预留）
  Fleeting/                 空（闪念笔记预留）
1_日志/                     时间线
  2024/2025/2026/           按年归档的每日日志
2_个人/                     个人资产（跨公司通用）
  生活/                     健身/阅读/人生思考/尤佳欣
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
  英语学习/                  英语学习相关笔记
  项目管理/
    1_归档项目/              已归档旧 MOC 项目（历史参考，不再参与日常维护）
4_项目/                      Project Manager（obsidian-pm）项目管理，插件自动维护
  项目名.md                  项目主文件（pm-project: true，插件全权管控，禁止手动修改）
  项目名_tasks/              任务目录
    任务文件.md              pm-task 任务文件（插件全权管控）
    Archive/                已完成/已取消任务归档
    _others/                手动项目文档（插件不碰）
      项目总览.md            概述 + 里程碑 + 方案记录 + 重难点 + 相关文档
      进度记录.md            仅含 # 日志 段落 + 一段 Dataview 查询代码（自动从日记拉取，不手动写进度）
      其他笔记.md            Spoke 文档
8_附件/                     附件集中管理（按日期/主题混合命名）
9_系统/                     元数据层
  Dashboard/                 知识库仪表盘
  MOC/                      系统级内容地图（项目看板/项目管理日常指南/工作情况汇总）
  SKILLs/                   知识库专属 skills
  模板/                      笔记模板
  看板/                      日历看板
index.md                    知识库 MOC 精选入口
```

## 每日记录 Frontmatter 规范

```yaml
---
日期: YYYY-MM-DD
类型: 每日记录
tags: []
项目: []        # 列表，如 [延锋座椅检测项目, 大3D项目支持]
总结:           # 一句话概括今天
---
```

### tags 标签词表

#### 工作领域标签（用于每日记录和项目笔记）

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

#### 个人/生活标签

| 标签 | 覆盖范围 | 关键词匹配 |
|------|---------|-----------|
| Obsidian | 知识管理、笔记整理 | Obsidian / 知识库 / 笔记 |
| 英语学习 | 英语、背单词、口语 | 背单词 / 墨墨 / 英语 / 口语 / English |
| 职业/跳槽 | 跳槽、面试、简历、职业规划 | 简历 / 面试 / 跳槽 / 离职 / 华睿 / offer |
| 健身 | 健身、运动记录 | 健身 / 跑步 / 深蹲 / 体重 / 有氧 |
| 生活 | 生活记录、个人事件 | 尤佳欣 / 约会 / 吵架 / 生活 |

#### 标签命名规则
- 领域标签用 `/` 表示层级关系：如 `职业/跳槽`、`AI/LangGraph`
- 编程语言用具体技术名称：`cpp`、`Python`、`CSharp`
- 每日记录 tags 为必填字段，从词表选择

## 每日记录正文结构

```
# 工作记录
- [[项目名]] 具体内容...
---
# 英语学习       （可选段落）
- [x] 背单词
- 口语练习
---
# 生活记录
...
---
# 健身记录       （可选段落）
...
---
# 所思所想
...
---
# 附件
...
```

段落顺序不严格固定，以下常见排列：

| 排列方式 | 适用场景 |
|---------|---------|
| 工作 → 英语 → 生活 → 健身 → 所思 → 附件 | 有英语学习任务的日子 |
| 工作 → 生活 → 健身 → 所思 → 附件 | 无英语学习任务的日子 |

非首个一级标题前必须有 `---` 分隔符。

## 分类原则

- `2_个人/`：不管在哪家公司都有用的知识（经验、AI、开发工具、生活）
- `3_工作/`：跟具体公司/项目绑定的知识（项目笔记、理论知识、工作文件）
- 两者之间靠 wikilink 桥接

## Project Manager 项目结构规范

项目全部由 obsidian-pm 插件（Project Manager v1.8.0）管理，数据存为纯 Markdown + YAML frontmatter。**所有 pm-project / pm-task 文件完全由插件管控，skill 只读不写。**

### 项目主文件（pm-project）

位置：`4_项目/{项目名}.md`，frontmatter 标记 `pm-project: true`。

```yaml
---
pm-project: true
id: "zgv4l9x1mrvrgm2a"
title: "延锋座椅检测项目"
description: "项目一句话描述"
color: "#8b72be"
icon: "📋"
taskIds: ["任务id列表"]       # 插件维护，勿手动改
customFields: []             # 自定义字段
teamMembers: ["杨子萱", "冯方"]
savedViews: []               # 已保存视图
createdAt: "2026-07-22T07:28:29.361Z"
updatedAt: "2026-08-12T08:35:30.867Z"
---
```

正文由插件同步渲染 `## Tasks` 任务列表，**skill 不得写入正文**。

### 任务文件（pm-task）

位置：`4_项目/{项目名}_tasks/{任务名}.md`，frontmatter 标记 `pm-task: true`。

```yaml
---
pm-task: true
projectId: zgv4l9x1mrvrgm2a   # 所属项目 id
parentId:                     # 父任务 id（子任务时）
id: ga1zh8humsi9vvwc
title: 撰写SOP
type: task                    # task / subtask / milestone
status: in-progress           # todo / in-progress / blocked / review / done / cancelled
priority: medium              # critical / high / medium / low
start: 2026-08-12
due: 2026-08-13
progress: 0                   # 0-100
assignees: []
tags: []
subtaskIds: []
dependencies: []              # 依赖任务 id，插件自动排程
createdAt: 2026-08-07T01:35:10.908Z
updatedAt: 2026-08-07T06:42:32.745Z
---

Project: [[延锋座椅检测项目|延锋座椅检测项目]]
```

正文首行固定为 `Project: [[项目名|项目名]]`，skill 不得改动。

### 任务目录约定（`_tasks/`）

- 任务文件平铺在 `{项目名}_tasks/` 下，文件名即任务标题
- `Archive/`：插件归档已完成/已取消任务
- `_others/`：手动项目文档，插件不碰
  - `项目总览.md`：概述 + 里程碑 + 方案记录 + 重难点 + 相关文档（**skill 可写**）
  - `进度记录.md`：仅 `# 日志` 段落 + Dataview 自动查询代码，**不手动写进度**

### 进度记录（Dataview 自动拉取）

`_others/进度记录.md` 内嵌 dataviewjs，从 `1_日志` 自动拉取 `[[项目名]]` 提及内容，**不需要 skill 写入**：

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

- 项目最后活动日期 = 日志中最近一次提及该项目的日期（Dataview 查询 `1_日志/` 中 wikilink 或 frontmatter `项目` 字段包含项目名的日记）
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

## index.md 结构

```markdown
# 知识库索引

## 1. 3D视觉与机器视觉
  ### 1.1 理论基础
  ### 1.2 标定
  ### 1.3 算子参考
  ### 1.4 算法原理
  ### 1.5 3D点云
  ### 1.6 实战经验
## 2. 项目
  ### 2.1 进行中
  ### 2.2 学习中
  ### 2.3 算法复现
  ### 2.4 暂停
  ### 2.5 已归档
  ### 2.6 其他项目笔记
  ### 2.7 工作文件
## 3. AI与Agent
## 4. 开发工具
## 5. 个人生活
  ### 5.1 生活
  ### 5.2 经验与思考
  ### 5.3 职业发展
  ### 5.4 人生思考与成长
  ### 5.5 跳槽准备中
## 6. 待归档
## 7. 系统与元数据
```

### index.md 分类归属规则

- `3_工作/工作知识库/5_理论知识/标定理论/` → 第 1.2 节 标定
- `3_工作/工作知识库/5_理论知识/定位与抓取/` → 第 1.1 节 理论基础
- `3_工作/工作知识库/5_理论知识/算法与数学/` → 第 1.4 节 算法原理
- `3_工作/工作知识库/5_理论知识/Opencv/` → 第 1.3 节 算子参考
- `3_工作/工作知识库/5_理论知识/PCL/` → 第 1.5 节 3D点云
- `3_工作/工作知识库/1_软件产品/` → 第 1.3 节 算子参考 / 第 1.6 节 实战经验
- `3_工作/工作知识库/3_经验笔记/` → 第 1.6 节 实战经验
- `2_个人/经验/视觉算法/` → 第 1.6 节 实战经验
- `4_项目/`（pm-project + `_tasks/` 子文件） → 第 2 节 项目（进行中项目按状态归入 2.1/2.4）
- `3_工作/项目管理/1_归档项目/`（旧 MOC 归档） → 第 2.5 节 已归档
- `2_个人/经验/AI/` → 第 3 节 AI与Agent
- `2_个人/经验/开发工具/` → 第 4 节 开发工具
- `2_个人/生活/` → 第 5.1 节 生活 / 第 5.4 节 人生思考
- `2_个人/跳槽准备中/` → 第 5.3 节 职业发展 / 第 5.5 节 跳槽准备中
- `3_工作/英语学习/` → 第 5.1 节 生活
- `0_Inbox/Clippings/` → 第 6 节 待归档

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

## LaTeX 排版规范

行内公式 `$` 符号与公式内容之间不允许有空格。
- 正确：`$\mathbf{A}\mathbf{x}=\mathbf{b}$`
- 错误：`$ \mathbf{A}\mathbf{x}=\mathbf{b} $`

## 已知规则

- 附件策略：本地存储，不用图床。Custom Attachment Location 插件：`8_附件/${noteFileName}`
- 整理笔记时必须保留原始图片引用格式，不可修改
- wikilink 使用短名格式 `[[笔记名]]`，Obsidian 自动解析路径
- raw/ 目录只读，永不修改原始资料
- skills 真身托管：GitHub 私有仓库 `Chris-zixuan/zixuan_Agenthub`（`skills/` 目录），本机克隆于 `D:/个人项目/zixuan_Agenthub`，通过 npx skills 分发到各机器/各 agent
- 项目与任务管理统一由 Project Manager 插件（obsidian-pm）负责；`4_项目/` 下文件插件全权管控，skill 只读不写
- 项目进度记录由 Dataview 自动从日志拉取，skill 不手动写入进度
- 周报生成已移交独立 skill，本 skill 不再维护周报功能
