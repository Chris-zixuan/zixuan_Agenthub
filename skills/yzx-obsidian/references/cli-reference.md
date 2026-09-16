# 工具层 · 官方 Obsidian CLI 参考

用 Obsidian **官方**命令行工具操作知识库。核心价值：移动 / 重命名笔记时**自动更新全库 wikilink**，这是 `mv` 做不到的。

> 本文件是命令手册。通用硬约束（安全红线、协作边界、备份与复核）见 `SKILL.md`。
> 另两层（分析层 / 运维层）都建立在本层能力之上。

## 定位与前提

| 项 | 值 |
|---|---|
| 二进制 | `/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`（随 Obsidian 内置） |
| 启用 | 设置 → 通用 → 高级 → **命令行界面**（Obsidian 1.13.7 实测） |
| PATH 入口 | 启用后 Obsidian 自动软链 `/usr/local/bin/obsidian` |
| 关键前提 | **CLI 走 IPC，Obsidian 必须处于运行状态**，否则命令失败 |

> 上表为 macOS 实测。Windows 端请先确认官方 CLI 是否可用（这是 Obsidian 的主机级功能），不可用则本层能力退化为界面操作。

**不要安装 Homebrew 上的同名第三方 `obsidian-cli`**（`yakitrak/yakitrak/obsidian-cli`）。它与官方同名但语法不同（位置参数 vs `key=value`），装了会让 `obsidian` 命令解析到错的版本。命令撞名时一律用绝对路径。

## 语法规则

- 参数一律 `key=value`：`obsidian move path="a.md" to="b.md"`
- 值含空格或中文标点需加引号：`file="我的 笔记"`
- `file=` 按**名称**解析（像 wikilink，可用简称）；`path=` 是**精确路径**（`文件夹/笔记.md`）
- 省略 `file` / `path` 时，多数命令作用于**当前活跃文件**
- 多数查询命令支持 `format=json|tsv|csv`

## ⚠️ 安全红线：无参数即执行

**大部分命令没有 `--help`。无参数调用不是打印帮助，而是直接执行默认行为。** 实测踩过的坑：

| 命令 | 无参数时的实际后果 |
|---|---|
| `obsidian create` | **直接新建** `Untitled.md` |
| `obsidian delete` | **把当前活跃文件移入回收站** |

因此：

1. **永远显式传 `path=` 或 `file=`**，不要裸调命令
2. 想查命令名列表用 `obsidian --help`；查具体参数用法看本文档
3. 有副作用的命令需格外谨慎：`delete` `move` `rename` `property:set|remove` `plugin:enable|disable|install|uninstall` `theme:*` `snippet:*` `restart` `reload` `eval` `devtools` `sync` `daily:*` `task`（更新时）

删除是**移入回收站**而非彻底删除。macOS 默认进系统回收站 `~/.Trash/`（不是库内 `.trash/`），可恢复。

## 核心命令

### 1. 移动与重命名（本层最重要的能力）

```bash
obsidian move path="旧路径/笔记.md" to="新路径/笔记.md"   # 移动/改名，可跨目录
obsidian rename path="路径/笔记.md" name="新名称"          # 只改文件名，保留所在目录
```

**实测行为**（2026-09-12 在本库验证）：两者都会自动更新全库所有指向该笔记的链接，包括带别名的写法 —— `[[旧名]]` → `[[新名]]`、`[[旧名|别名]]` → `[[新名|别名]]`。

移动后**必须复核**：

```bash
obsidian unresolved | grep "旧名"
```

无输出即无残留断链。若刚移动完立刻查可能因索引未重建而误报，等 1–3 秒再查。

### 2. 属性（frontmatter）读写

```bash
obsidian property:set path="笔记.md" name="类型" value="知识笔记" type=text
obsidian property:set path="笔记.md" name="tags" value="3D视觉,算法" type=list
obsidian property:read  path="笔记.md" name="类型"
obsidian property:remove path="笔记.md" name="废弃字段"
obsidian properties                      # 列出全库所有属性名及使用情况
```

`type` 可选 `text|list|number|checkbox|date|datetime`。`type=list` 写出的是标准 YAML 多行列表格式：

```yaml
tags:
  - 3D视觉
  - 算法
```

> **写属性前先确认值域**：`类型`、`tags`、`状态` 的合法取值以 `9_系统/协作约定.md` 为准，不要自造取值。
> `4_项目/` 下由 pm 插件管控的文件（`pm-*`、`id`、`createdAt`、`status` 等）**不要用 `property:set` 改**。

### 3. 体检（替代手写扫描脚本）

```bash
obsidian unresolved   # 全库断链（未解析链接）——一条命令替代整个断链扫描脚本
obsidian orphans      # 无入链页（孤立笔记）
obsidian deadends     # 无出链页
obsidian tags         # 全库标签（含层级，如 #标定/手眼标定）
obsidian vault        # 库信息：名称/路径/文件数/文件夹数/体积
obsidian version
```

### 4. 搜索与读取

```bash
obsidian search query="关键词" [path=文件夹] [limit=n] [total] [format=json]
obsidian search:context query="关键词"     # 带匹配行上下文
obsidian read path="笔记.md"
obsidian outline path="笔记.md"            # 标题大纲树
obsidian wordcount path="笔记.md"
obsidian files                             # 列出全部文件
obsidian folders                           # 列出全部目录
obsidian backlinks file="笔记名"            # 反向链接
obsidian links file="笔记名"                # 出链
obsidian aliases                            # 全库别名
```

### 5. 内容写入

```bash
obsidian append  path="笔记.md" content="追加到末尾"
obsidian prepend path="笔记.md" content="插入到开头"
obsidian create  path="目录/新笔记.md" content="内容"   # 必须显式给 path
obsidian daily:path / daily:read / daily:append content="..."
```

### 6. 其它

```bash
obsidian task ref="路径:行号"        # 查看或更新单个任务
obsidian tasks                       # 列出全库任务
obsidian command id=<command-id>     # 执行 Obsidian 命令（commands 可列全部）
obsidian eval code="..."             # 执行 JS（危险，慎用）
```

## 操作前须知（衔接库规范）

- **移动 / 重命名必走 CLI**（`9_系统/协作约定.md` §6 铁律）—— 不要用 `mv`
- CLI 不可用时（Obsidian 未运行）→ 在 Obsidian 界面操作，**禁止退化成 `mv`**
- 批量改动（≥3 文件或涉及目录调整）前先备份到 `.workbuddy/backups/{日期}/`，并先向用户报告影响范围
- 属性值域（`类型` 取值、`状态` 插件英文 id）、标签词表（技术域 + 个人域）**以 `9_系统/协作约定.md` 为准**，不要自造取值

## 常见坑速查

| 现象 | 原因 / 处理 |
|---|---|
| 命令无任何输出或报错 | Obsidian 未运行，CLI 依赖运行中的实例 |
| `Missing required parameter: xxx` | 该命令没有 help，按本文档补齐参数 |
| 中文文件名 / 含空格路径报错 | 加引号：`path="0_Inbox/我的 笔记.md"` |
| 移动后链接看似未更新 | 等 1–3 秒让索引重建，再用 `unresolved` 复核 |
| 删除的文件在库里找不到 | macOS 默认进系统回收站 `~/.Trash/`，不是库内 `.trash/` |
| 命令行为与文档不符 | 可能解析到了第三方同名 CLI，改用绝对路径调用 |
