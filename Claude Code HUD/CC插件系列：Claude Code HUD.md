# Claude Code HUD 状态栏插件

## 解决的问题

Claude Code 终端无法实时显示上下文使用量，导致上下文耗尽时才发现，AI 回答质量已明显下降。

claude-hud 在终端底部增加一个实时状态栏，让关键信息一目了然。

## ![](https://pic2.zhimg.com/v2-d85d0363ea77eae4f1478857a6374917_1440w.jpg)

## 功能一览

| 功能       | 示例显示                                        | 说明                                             |
| ---------- | ----------------------------------------------- | ------------------------------------------------ |
| 上下文用量 | `Context █████░░░░░ 45%`                        | 进度条变色：绿→黄→红；超 85% 自动显示 token 明细 |
| 订阅额度   | `Usage ██░░░░░░░░ 25% (1h 30m / 5h)`            | Pro/Max 专属，显示 5 小时滑动窗口剩余时间        |
| 工具活动   | `◐ Edit: auth.ts \| ✓ Read ×3`                  | 实时显示 AI 正在调用的工具                       |
| Agent 状态 | `◐ explore [haiku]: Finding auth code (2m 15s)` | 子 Agent 名称、模型、任务内容、运行时长          |
| Todo 进度  | `▸ Fix authentication bug (2/5)`                | TodoWrite 任务的完成进度                         |

> [!note] API 用户
> 使用 API Key 登录时，订阅额度（Usage）行不会显示，该功能仅限 Pro/Max 订阅用户。

---

## 安装（3 条命令）

```bash
/plugin marketplace add jarrodwatts/claude-hud
/plugin install claude-hud
/claude-hud:setup
```

装完立即生效，无需重启。

> [!warning] Linux 报错处理
> 若出现 `EXDEV: cross-device link not permitted`，先执行：
>
> ```bash
> mkdir -p ~/.cache/tmp && TMPDIR=~/.cache/tmp claude
> ```
>
> 然后在新会话中重新安装。

---

## 配置

```bash
/claude-hud:configure
```

提供三种预设：

- **Minimal**：仅显示基础信息
- **Essential**（推荐）：上下文 + 订阅额度
- **Full**：所有功能全开

> [!tip]
> 工具追踪、Agent 追踪、Todo 追踪**默认关闭**，需在 configure 中手动开启。

配置文件路径：`~/.claude/plugins/claude-hud/config.json`

---

## 相关链接

- [GitHub: jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud)
