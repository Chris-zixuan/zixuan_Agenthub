---
name: workbuddy-auto-checkin
description: 'WorkBuddy「Buddy 加油站」每日签到自动化搭建 Skill（纯签到，不含失败通知）。当用户要求"每天自动签到 WorkBuddy"、"自动领 Buddy 加油站积分"、"自动领 100 积分"、"设置 WorkBuddy 每日签到"、"把签到做成自动化"时使用。原理是只读本机 WorkBuddy 登录态的 accessToken，直接调用官方签到接口（无需点击 GUI、无需 OCR、无需第三方 Skill），再把自带脚本落位到稳定路径并创建 WorkBuddy 自带每日 09:00 自动化。安全约束：只读登录态、绝不打印 token、不修改登录态文件、不安装 Electron、不建系统级定时任务。若需要"签到失败推微信"，请改用带通知版技能。'
version: 1.1.0
author: ChrisYang
tags:
  - WorkBuddy
  - 自动化
  - 签到
  - 积分
  - 定时任务
skill_path: "Mac: /Users/yangzixuan/个人项目/zixuan_Agenthub/skills/workbuddy-auto-checkin；Windows: D:/个人项目/zixuan_Agenthub/skills/workbuddy-auto-checkin"
---

# WorkBuddy 每日自动签到（接口直签，纯签到版）

WorkBuddy 的「Buddy 加油站」每日签到本质是一次带本地登录 Token 的 HTTP 接口请求，
**不需要**模拟点击左下角「个人信息 → Buddy 加油站 → 签到」这一套 GUI 流程（自动化代理也没有点击桌面 UI 的能力）。

本 Skill 自带脚本 `scripts/workbuddy_checkin.py`，可直接拿来用。
**本版本不含任何外部通知能力**，仅完成签到本身；若需要"签到失败推微信"，请使用 `workbuddy-checkin`（带通知版）技能。

## 关键事实（已实测验证）

### 登录态文件位置（脚本已内置多平台候选，按顺序探测）

| 平台 | 路径 |
| --- | --- |
| Windows | `%LOCALAPPDATA%\CodeBuddyExtension\Data\Public\auth\workbuddy-desktop.info`（旧版可能在 `%APPDATA%` 同路径，文件名 `state.vscdb` 的 sqlite；v5.3.8+ 为明文） |
| macOS | `~/Library/Application Support/CodeBuddyExtension/Data/Public/auth/workbuddy-desktop.info`（实测 2026-09 可用） |

> 脚本只在环境变量存在时才拼 Windows 路径，否则会退化成相对路径噪音。

- 文件内 `auth.accessToken`（JWT，`auth.tokenType=Bearer`）、`auth.domain`、`auth.expiresAt`（毫秒时间戳，可用来判断是否过期）。
- **接口域名以登录态里的 `auth.domain` 为准，不要写死**：
  - 实测 Windows 机为 `www.codebuddy.cn`；
  - 实测 macOS 机（2026-09-16）为 `copilot.tencent.com`，**该域名可用，返回 HTTP 200** —— 所以"`copilot.tencent.com` 一定 404"的说法不成立，不要据此替换域名，直接读本机 `auth.domain` 即可。
- **状态查询（只读）**：`POST https://<domain>/v2/billing/meter/checkin-activity-status`
  返回 `{"code":0,"data":{"today_checked_in":true/false,"streak_days":N,"daily_credit":100,...}}`
- **领取签到**：`POST https://<domain>/v2/billing/meter/daily-checkin`
  - 成功：HTTP 200，`code:0`，返回 `credit` / `streak_days`（领取 100 积分）。
  - 已签到：HTTP 400，`code:10001`，`msg:"今天已签到，请明天再来"` —— **幂等，不会重复发**。

## 自带脚本（`scripts/workbuddy_checkin.py`）

仅用 Python 标准库（`urllib` / `json` / `os`），零第三方依赖。逻辑：
1. 按候选列表定位 `workbuddy-desktop.info`，只读取出 `accessToken` 与 `domain`。
2. 调 `checkin-activity-status`：若 `data.today_checked_in==true` → 直接 `skip_already_signed` 退出（不发领取请求）。
3. 否则调 `daily-checkin` 领取；响应 `code==10001` 或含"已签到" → 视为已签安全跳过；HTTP 200 且 `code==0` → 领取成功。
4. 非 2xx 也解析响应体（避免把"已签到 400"误判为异常）。
5. **输出 JSON 结果，全程不打印任何真实 token**（仅脱敏 `eyJhbG...xxxx`）。
6. 退出码：成功 `0` / 失败 `1`；每次运行结果追加写入脚本同目录 `checkin.log`（不含 token）。

运行方式（按平台替换解释器路径）：

```
# Windows（用正斜杠路径，避免 Git Bash MSYS 把 /c/ 当相对路径）
"C:/Users/<user>/.workbuddy/binaries/python/versions/3.13.12/python.exe" "C:/Users/<user>/.workbuddy/scripts/workbuddy_checkin.py"

# macOS
/Users/<user>/.workbuddy/binaries/python/versions/3.13.12/bin/python3 /Users/<user>/.workbuddy/scripts/workbuddy_checkin.py

# 仅查询（只读，不领取）：追加 --check-only
# 跳过失败推送（调试）：追加 --no-notify
```
> 注意：上面的 python 路径是 WorkBuddy 托管运行时；若本机路径不同，用 `where python` / `which python3` 查实际路径替换。

## 调用本 Skill 时的搭建流程（照做即可）

当用户要求搭建/修复自动签到，或换机/重装后重建时，按以下步骤执行：

1. **定位登录态并校验 token**
   - 找到 `workbuddy-desktop.info`，确认 `auth.accessToken` 存在且未过期（`expiresAt` 字段）。
   - 若文件不存在或 token 失效：如实告知用户"请先在 WorkBuddy 客户端登录"，**不要**伪造或猜测。

2. **落位脚本到稳定路径**
   - 把本 Skill 目录里的 `scripts/workbuddy_checkin.py` 复制到：
     - Windows：`C:\Users\<user>\.workbuddy\scripts\workbuddy_checkin.py`
     - macOS：`/Users/<user>/.workbuddy/scripts/workbuddy_checkin.py`
   - 用托管 Python 跑一次 `--check-only --no-notify` 验证接口通、token 有效（应返回 `status_http:200`、`status_resp.data.today_checked_in` 字段）。

3. **验证领取分支（可选但建议）**
   - 跑一次不带参数的完整脚本：若当天已签 → 返回 `skip_already_signed`；若未签 → 返回 `clicked` 并提示用户去 Buddy 加油站界面核对 +100。

4. **创建 WorkBuddy 自带自动化**（不要用 crontab / launchd / 第三方定时器）
   - 先用 `automation_update`（mode=list）检查是否已存在同类自动化；有则复用，**不要重复创建**。
   - 用 `automation_update`（mode=create）创建 recurring 自动化：
     - name：`WorkBuddy 每日自动签到`
     - rrule：`FREQ=DAILY;BYHOUR=9;BYMINUTE=0`（每天 09:00）
     - status：`ACTIVE`
     - cwds：`<SCRIPTS>` 目录
   - 自动化提示词（让代理用 Bash 跑脚本并脱敏汇报；**解释器路径按平台替换**）：
       ```
       请使用 Bash 工具运行以下命令，完成 WorkBuddy「Buddy 加油站」每日签到（接口直签，无需点击 GUI）：

       <PYTHON> <SCRIPTS>/workbuddy_checkin.py

       执行后，根据脚本输出的 JSON 结果，用一句话向用户汇报：
       - action=clicked：签到成功，已领取积分（说明 +N 积分、连续第几天）。
       - action=skip_already_signed：今日已签到，无需重复操作。
       - status=error：如实报告 msg 中的失败原因，不得谎报成功。
       约束：
       1. 严禁在任意输出中打印 token / accessToken / refreshToken。
       2. 不要无限重试；脚本内部最多重试 1 次即可。
       3. 若命令执行失败，如实报告，并提示检查 WorkBuddy 是否已登录、电脑是否联网、是否在 09:00 前后保持开机且客户端未退出。
       4. 不要运行 --check-only，也不要重复执行脚本。
       ```
     - 占位符替换：
       - Windows：`<PYTHON>` = `C:/Users/<user>/.workbuddy/binaries/python/versions/3.13.12/python.exe`，`<SCRIPTS>` = `C:/Users/<user>/.workbuddy/scripts`
       - macOS：`<PYTHON>` = `/Users/<user>/.workbuddy/binaries/python/versions/3.13.12/bin/python3`，`<SCRIPTS>` = `/Users/<user>/.workbuddy/scripts`

5. **向用户汇报**：自动化名称、执行时间、脚本路径；并提醒"若当天已手动签到会自动跳过；首个真实自动领取通常在次日 09:00，请在 Buddy 加油站核对积分 +100"。

## 安全约束（务必遵守）
- 只读登录态文件，绝不修改、绝不删除、绝不外传 `accessToken` / `refreshToken`。
- 任何输出（终端、日志、汇报）都不得包含真实 token；脚本已脱敏，代理也不要回显凭据。
- 不安装 Electron、不创建系统级定时任务；只用 WorkBuddy 自带自动化。
- 不要在网页版尝试签到（网页版无签到入口，仅 PC 客户端专属）。

## 排错
- `HTTP 400 / code=10001`：当天已签，属正常，非错误。
- `未找到本机登录态文件`：WorkBuddy 未登录或路径变更，请先登录（macOS 注意路径在 `~/Library/Application Support/` 下，不在 `~/.workbuddy/`）。
- `HTTP 404`：多为域名不对。**先确认是否真的读到了本机 `auth.domain`**；`copilot.tencent.com` 在 macOS 上实测可用（HTTP 200），不必然 404，不要盲目替换。若确实 404，再尝试 `www.codebuddy.cn`。
- token 过期：对比登录态里的 `auth.expiresAt`（毫秒时间戳）与当前时间；过期需重启客户端刷新登录态。
- 自动化到点没跑：检查电脑是否开机、客户端是否退出、是否联网。
