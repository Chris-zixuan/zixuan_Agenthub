#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 每日自动签到脚本（接口直签，无需 GUI 点击 / OCR）

原理：
  1. 读取本机 WorkBuddy 登录态文件中的 accessToken（只读，绝不修改登录态）
  2. 查询今日签到状态  POST {base}/billing/meter/checkin-activity-status
  3. 若今日未签到，调用 POST {base}/billing/meter/daily-checkin 领取
  4. 已签到 / 接口返回 code=10001 则安全跳过，不做重复领取

失败推送（可选）：
  若签到结果为 status!=ok，会读取本地配置文件
  ~/.workbuddy/scripts/notify_config.json（若存在），向微信通道推送失败提醒。
  支持：企业微信群机器人 webhook / PushPlus / Bark。配置缺失则静默跳过，不影响签到。

安全约定：
  - 不打印 token / accessToken / refreshToken（任何输出都不含敏感凭据）
  - 不修改本机登录态文件
  - 推送密钥只存在于本地 notify_config.json，永不进入脚本或技能目录
  - 异常只记录失败原因，最多重试 1 次，不无限重试

用法：
  python workbuddy_checkin.py            # 查询 + 必要时领取
  python workbuddy_checkin.py --check-only   # 仅查询状态（只读，不领取）
  python workbuddy_checkin.py --no-notify    # 跳过失败推送（调试用）
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

# ---- 配置 ----
_REL_AUTH = os.path.join("CodeBuddyExtension", "Data", "Public", "auth",
                         "workbuddy-desktop.info")
AUTH_CANDIDATES = [
    # Windows: 仅当环境变量存在时才拼路径（否则会产生相对路径噪音）
    (os.path.join(os.environ["LOCALAPPDATA"], _REL_AUTH)
     if os.environ.get("LOCALAPPDATA") else None),
    (os.path.join(os.environ["APPDATA"], _REL_AUTH)
     if os.environ.get("APPDATA") else None),
    # macOS: ~/Library/Application Support/...
    os.path.join(os.path.expanduser("~"), "Library", "Application Support", _REL_AUTH),
]
AUTH_CANDIDATES = [p for p in AUTH_CANDIDATES if p]
STATUS_PATH = "/billing/meter/checkin-activity-status"
CHECKIN_PATH = "/billing/meter/daily-checkin"
HTTP_TIMEOUT = 20
MAX_RETRY = 1
# 失败推送配置（含密钥，仅本地，不入库）
NOTIFY_CONFIG = os.path.join(os.path.expanduser("~"),
                             ".workbuddy", "scripts", "notify_config.json")


def find_auth_file():
    for p in AUTH_CANDIDATES:
        if p and os.path.isfile(p):
            return p
    return None


def load_token(auth_path):
    with open(auth_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    auth = data.get("auth", {})
    token = auth.get("accessToken")
    domain = auth.get("domain") or "www.codebuddy.cn"
    if not token:
        raise RuntimeError("登录态文件中未找到 accessToken（可能未登录或登录态已失效）")
    return token, domain


def api_call(base, path, token, payload=None, method="POST"):
    url = base + path
    data = json.dumps(payload if payload is not None else {}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer %s" % token)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "WorkBuddy-Checkin-Script/1.1")
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            body = resp.read().decode("utf-8", "replace")
            try:
                return resp.status, json.loads(body)
            except json.JSONDecodeError:
                return resp.status, {"raw": body}
    except urllib.error.HTTPError as e:
        # 非 2xx 也读取响应体（如已签到返回的 HTTP 400 / code=10001）
        try:
            body = e.read().decode("utf-8", "replace")
            try:
                return e.code, json.loads(body)
            except json.JSONDecodeError:
                return e.code, {"raw": body}
        except Exception:
            return e.code, {"raw": ""}


def mask_token(t):
    if not t:
        return "<empty>"
    return t[:6] + "..." + t[-4:]


# ---------------- 失败推送（微信） ----------------

def load_notify_config():
    if not os.path.isfile(NOTIFY_CONFIG):
        return None
    try:
        with open(NOTIFY_CONFIG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        if not isinstance(cfg, dict):
            return None
        return cfg
    except Exception:
        return None


def _http_post_json(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "WorkBuddy-Checkin-Script/1.1")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


def notify_via_wecom(webhook, title, content):
    payload = {"msgtype": "markdown", "markdown": {"content": content}}
    return _http_post_json(webhook, payload)


def notify_via_pushplus(token, title, content):
    url = "https://www.pushplus.plus/send"
    payload = {"token": token, "title": title,
               "content": content, "template": "markdown"}
    return _http_post_json(url, payload)


def notify_via_bark(bark_url, title, content):
    # bark_url 形如 https://api.day.app/<key>/ ，脚本自动拼接标题与内容
    base = bark_url.rstrip("/")
    url = "%s/%s/%s" % (base,
                        urllib.parse.quote(title),
                        urllib.parse.quote(content))
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", "WorkBuddy-Checkin-Script/1.1")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


def notify_failure(res):
    """签到失败时，按本地配置推送微信提醒；配置缺失则静默跳过。"""
    cfg = load_notify_config()
    if not cfg:
        return
    if cfg.get("enabled") is False:
        return

    title = "⚠️ WorkBuddy 每日签到失败"
    now = time.strftime("%Y-%m-%d %H:%M:%S")  # 本机时区（北京时间）
    msg = res.get("msg", "未知原因")
    auth_file = res.get("detail", {}).get("auth_file", "未知")

    content = (
        "### ⚠️ WorkBuddy 每日自动签到失败\n\n"
        "> **时间**：%s\n\n"
        "> **原因**：%s\n\n"
        "> **登录态文件**：%s\n\n"
        "> **处理建议**：请检查 WorkBuddy 是否已登录、电脑是否联网、09:00 前后是否开机且客户端未退出；"
        "必要时重启客户端刷新登录态后，可手动再跑一次脚本。\n"
    ) % (now, msg, auth_file)

    results = []
    # 企业微信群机器人 webhook（优先级最高）
    webhook = cfg.get("wecom_webhook")
    if webhook:
        try:
            st, _ = notify_via_wecom(webhook, title, content)
            results.append("wecom:%s" % st)
        except Exception as e:
            results.append("wecom_err:%s" % e)
    # PushPlus（推送到个人微信）
    token = cfg.get("pushplus_token")
    if token:
        try:
            st, _ = notify_via_pushplus(token, title, content)
            results.append("pushplus:%s" % st)
        except Exception as e:
            results.append("pushplus_err:%s" % e)
    # Bark（iOS 推送）
    bark = cfg.get("bark_url")
    if bark:
        try:
            st, _ = notify_via_bark(bark, title, content)
            results.append("bark:%s" % st)
        except Exception as e:
            results.append("bark_err:%s" % e)

    # 仅记录推送动作结果（不含任何密钥 / token），便于排查
    res["detail"]["notify"] = results


# ---------------- 主流程 ----------------

def run(check_only):
    result = {"status": "unknown", "action": None, "points": None,
              "msg": "", "detail": {}}

    auth_path = find_auth_file()
    if not auth_path:
        result.update(status="error", msg="未找到本机登录态文件，请确认 WorkBuddy 已登录")
        return result

    try:
        token, domain = load_token(auth_path)
    except Exception as e:
        result.update(status="error", msg="读取登录态失败: %s" % e)
        return result

    base = "https://%s/v2" % domain
    result["detail"]["domain"] = domain
    result["detail"]["auth_file"] = auth_path
    # 仅记录 token 形态，绝不记录真实值
    result["detail"]["token_masked"] = mask_token(token)

    attempt = 0
    last_err = None
    while attempt <= MAX_RETRY:
        attempt += 1
        try:
            # 1) 查询今日状态
            st_code, st_body = api_call(base, STATUS_PATH, token)
            result["detail"]["status_http"] = st_code
            result["detail"]["status_resp"] = st_body

            # 判断是否已签到：兼容多种返回形态
            today_signed = False
            if isinstance(st_body, dict):
                if st_body.get("today_checked_in") is True:
                    today_signed = True
                elif st_body.get("data", {}).get("today_checked_in") is True:
                    today_signed = True
                elif str(st_body.get("code")) == "10001":
                    today_signed = True

            if check_only:
                result.update(
                    status="ok",
                    action="skip_check_only",
                    msg="状态查询成功（未执行领取）",
                )
                result["detail"]["today_signed"] = today_signed
                return result

            if today_signed:
                result.update(status="ok", action="skip_already_signed",
                              msg="今日已签到，无需重复领取")
                return result

            # 2) 领取签到
            ck_code, ck_body = api_call(base, CHECKIN_PATH, token)
            result["detail"]["checkin_http"] = ck_code
            result["detail"]["checkin_resp"] = ck_body

            if isinstance(ck_body, dict):
                code = str(ck_body.get("code", ""))
                msg = ck_body.get("msg") or ck_body.get("message") or ""
                if code == "10001" or "已签到" in msg or "今天已签到" in msg:
                    result.update(status="ok", action="skip_already_signed",
                                  msg="今日已签到（接口返回 code=10001）")
                    return result
                if ck_code == 200 and code in ("0", "200", ""):
                    credit = ck_body.get("credit") or ck_body.get("data", {}).get("credit")
                    streak = ck_body.get("streak_days") or ck_body.get("data", {}).get("streak_days")
                    result.update(status="ok", action="clicked",
                                  points=credit,
                                  msg="领取成功" + (("，+%s 积分" % credit) if credit else "") +
                                      (("，连续第 %s 天" % streak) if streak else ""))
                    result["detail"]["streak_days"] = streak
                    return result
                # 其它成功/失败
                result.update(status="ok" if ck_code == 200 else "error",
                              action="clicked" if ck_code == 200 else "failed",
                              msg=msg or ("HTTP %s" % ck_code))
                return result
            else:
                result.update(status="error", action="failed",
                              msg="领取接口返回非 JSON: %s" % ck_body.get("raw", "")[:200])
                return result

        except urllib.error.HTTPError as e:
            last_err = "HTTP %s: %s" % (e.code, e.reason)
        except urllib.error.URLError as e:
            last_err = "网络错误: %s" % e.reason
        except Exception as e:
            last_err = "异常: %s" % e

        # 重试前稍作等待
        if attempt <= MAX_RETRY:
            time.sleep(2)

    result.update(status="error", msg="重试 %d 次后仍失败: %s" % (MAX_RETRY, last_err))
    return result


def write_log(res):
    """把每次运行结果追加写入脚本同目录的 checkin.log（本地核查用，不含 token）。"""
    try:
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkin.log")
        line = "%s | status=%s | action=%s | msg=%s\n" % (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            res.get("status"), res.get("action"), res.get("msg"))
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass  # 写日志失败绝不影响签到


def main():
    check_only = "--check-only" in sys.argv
    no_notify = "--no-notify" in sys.argv
    try:
        res = run(check_only)
    except Exception as e:
        res = {"status": "error", "action": None, "points": None,
               "msg": "脚本未捕获异常: %s" % e, "detail": {}}
    # 输出结果（不含任何真实 token）
    print(json.dumps(res, ensure_ascii=False, indent=2))
    # 失败推送（配置缺失则跳过；--no-notify 用于调试）
    if not no_notify and res.get("status") != "ok":
        try:
            notify_failure(res)
        except Exception:
            pass  # 推送失败不影响签到结果与退出码
    # 本地运行日志（系统定时任务无对话汇报，靠它核查）
    write_log(res)
    # 退出码：成功 0，失败 1，便于自动化判断是否推送告警
    sys.exit(0 if res.get("status") == "ok" else 1)


if __name__ == "__main__":
    main()
