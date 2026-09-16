# 使用示例 / Usage Examples

本文档提供每个 Skill 的实际使用示例。

---

## 🗂️ 文件夹整理助手 (Organize)

### 场景：整理混乱的项目根目录

```
用户: 文件夹好乱，帮我整理一下
助手: [自动触发文件夹整理流程]
     好的，先扫描一下当前目录...

     【扫描结果】
     根目录散落文件：11 个
     子目录：4 个（其中 2 个命名风格不统一）
     疑似可清理：.playwright-mcp/（工具缓存）、output-temp/

     我来分析归属...

     【整理方案】

     整理后结构：
     项目根/
     ├── src/（保留不动，已有结构）
     ├── docs/（新建，归入文档类散落文件）
     │   ├── 需求说明.md
     │   └── 接口文档.md
     ├── scripts/（新建，归入脚本文件）
     │   └── deploy.sh
     └── .gitignore（保留不动）

     操作清单：
     - [新建] docs/
     - [移动] 需求说明.md → docs/需求说明.md
     - [移动] 接口文档.md → docs/接口文档.md
     - [新建] scripts/
     - [移动] deploy.sh → scripts/deploy.sh
     - [重命名] Temp_output/ → output/（统一命名风格）
     - [删除] .playwright-mcp/（工具缓存，无保留价值）

     确认执行吗？

用户: 确认，但 .playwright-mcp 先不删
助手: 好的，跳过 .playwright-mcp 的删除操作。
     执行中...

     ✅ 完成！整理后目录结构如下：
     [展示整理后的树形图]
```

### 场景：整理指定目录

```
用户: /organize ./downloads
助手: 扫描 ./downloads 中...
     [同上流程，针对指定目录执行]
```

**预期输出**:
- 目标结构树形图
- 逐条操作清单（含不动的部分说明）
- 执行后验证结果

---

## 🔧 VisionMaster 脚本助手 (VM Script Helper)

### 场景 1：生成图像处理脚本

```
用户: 帮我写一个脚本，把输入图像转成灰度，然后做 Canny 边缘检测，输出边缘图
助手: [自动触发 VM 脚本开发流程]
     好的！先读取你的变量定义文件...

     读取 UserProperty.cs：
     - 输入：imgIn（IMAGE 类型）
     - 输出：imgOut（IMAGE 类型）

     类型映射确认：
     - imgIn → ImageData（直接赋值读取）
     - imgOut → ImageData（直接赋值输出）

     查阅参考资料... 读取 examples/02-canny-edge-detection.cs

     生成代码：

\`\`\`csharp
using System;
using OpenCvSharp;
using Script.Methods;

public partial class UserScript : ScriptMethods, IProcessMethods
{
    int processCount;

    public void Init()
    {
        processCount = 0;
    }

    /// <summary>
    /// 对输入图像进行灰度转换和 Canny 边缘检测，结果写入输出变量。
    /// </summary>
    public bool Process()
    {
        processCount++;
        Mat src = null;
        Mat gray = null;
        Mat edges = null;

        try
        {
            src = this.ImageDataToMat(imgIn);
            gray = new Mat();
            Cv2.CvtColor(src, gray, ColorConversionCodes.BGR2GRAY);

            edges = new Mat();
            Cv2.Canny(gray, edges, 50, 150);

            imgOut = this.MatToImageData(edges);
        }
        finally
        {
            src?.Dispose();
            gray?.Dispose();
            edges?.Dispose();
        }

        return true;
    }
}
\`\`\`

     自校验通过 ✅
     尝试调用 find_msbuild.ps1 编译校验...（若环境不支持，请手动编译确认）
```

### 场景 2：读写全局变量

```
用户: 我需要从全局变量读取一个阈值参数 threshold，用它做二值化
助手: 读取 UserProperty.cs... 确认输入输出定义。

     全局变量读取使用直接赋值方式（如 int t = threshold），
     不需要 GetIntValue 遗留接口。

     查阅 examples/01-basic-template.cs...

     [生成包含全局变量读取 + 二值化的完整脚本]
```

### 场景 3：不支持的请求

```
用户: 帮我写脚本控制 IO 输出信号
助手: 抱歉，控制器 IO 发送不在 VM 脚本的支持范围内。
     建议通过外部程序或上位机调用 VM SDK 实现。
```

**预期输出**:
- 完整可编译的 `UserScript.cs` 代码
- 每个方法带 XML 注释
- 编译校验结果（自动或静态审查）

---

## 📊 Claude Code HUD 安装

### 安装步骤

```bash
# 在 Claude Code 会话中执行（3 条命令）
/plugin marketplace add jarrodwatts/claude-hud
/plugin install claude-hud
/claude-hud:setup
```

装完立即生效，无需重启。

### 配置 HUD 显示项

```bash
/claude-hud:configure
```

### 效果预览

```
Context █████░░░░░ 45%                          # 上下文用量进度条
Usage ██░░░░░░░░ 25% (1h 30m / 5h)              # 订阅额度（Pro/Max）
◐ Edit: auth.ts | ✓ Read ×3                     # 工具活动
◐ explore [haiku]: Finding auth code (2m 15s)   # Agent 状态
▸ Fix authentication bug (2/5)                  # Todo 进度
```

> Linux 出现 `EXDEV: cross-device link not permitted` 时，先执行：
> ```bash
> mkdir -p ~/.cache/tmp && TMPDIR=~/.cache/tmp claude
> ```
> 然后在新会话中重新安装。

详细说明见 [Claude Code HUD 文档](./Claude%20Code%20HUD/)。

---

## 🎯 受众适配助手 (Audience Adapter)

### 场景 1：向 CEO 汇报技术进展

```
用户: 我需要向 CEO 汇报上周的系统优化进展，素材：
     - 完成了数据库索引优化，慢查询从 1200ms 降到 80ms
     - Redis 缓存命中率从 62% 提升到 91%
     - 修复了 3 个影响用户登录的 bug
     - 服务器成本因此减少了约 18%
     - 下周计划做 CDN 接入

助手: [自动触发受众适配流程]
     好的，目标受众是 CEO，我来做信息抽象和语言转换...

     ---

     # 系统性能优化 — 用户体验大幅提升，成本同步下降

     ## 核心结论
     本周完成了一轮系统性能优化，用户登录稳定性和页面响应速度显著改善，
     服务器运营成本同步降低 18%。

     ## 关键数据
     - 页面响应速度：↑ 93%（从 1.2 秒缩短至 0.08 秒）
     - 系统缓存效率：↑ 47%（命中率从 62% 提升到 91%）
     - 服务器成本：↓ 18%

     ## 需要您了解
     - 上周修复了 3 个影响用户登录的问题，现已全部解决
     - 下周将推进 CDN 接入，预计可进一步提升全球用户访问速度

     仅供知悉，无需回复。

     ---

     需要调整语气或转成其他受众版本吗？

用户: 再给我一个给技术负责人的版本
助手: [生成技术版本，保留完整技术指标和方案细节]
```

### 场景 2：跨部门同步上线影响

```
用户: 要给运营团队同步下周三的发布，内容是：
     把用户数据存储从 MySQL 迁移到分布式数据库，迁移期间报表数据会有 1 小时延迟，
     用户侧无感知，但后台报表刷新时间从实时变成每小时一次

助手: 目标受众是运营，我来用业务语言描述...

     # 数据库升级 业务同步

     ## 一句话概要
     下周三系统升级期间，后台报表数据刷新频率临时调整，用户使用不受影响。

     ## 具体变化

     ### 对用户的影响
     - 无影响，用户侧完全无感知

     ### 对业务流程的影响
     - 无需调整现有操作流程

     ### 对数据/报表的影响
     - 报表数据更新频率：实时 → 每小时一次（升级完成后恢复实时）

     ## 时间线
     | 时间 | 事项 |
     |---|---|
     | 下周三 上午 | 开始系统升级 |
     | 下周三 升级完成后 | 报表恢复实时更新 |

     ## 常见问题 FAQ
     - Q：报表数据跟昨天不一样怎么回复用户？
     - A：系统正在升级维护，数据将在 XX 时间恢复实时更新，请稍候刷新。
```

**预期输出**:
- 按受众策略调整后的沟通内容（邮件/汇报要点/消息等形式）
- 支持同一内容生成多个受众版本

---

## 📋 SOP 文档生成 (SOP Writer)

### 场景：梳理新员工入职流程

```
用户: /sop-writer 新员工入职流程

助手: [自动触发 SOP 文档生成流程]
     好的！让我先了解一下这个流程的基本情况。

     1. 目前入职流程大概涉及哪些环节？可以随便说，不用很结构化。

用户: HR 发 offer 之后，IT 要开账号，然后要签劳动合同，部门负责人要安排 onboarding，
     还有要做背调，有时候背调没做完就入职了然后有麻烦

助手: 了解了。再问几个问题帮我理清：
     2. 背调是谁负责发起？通常什么时候做？
     3. IT 开账号需要哪些信息，谁来提供？
     4. onboarding 有标准内容吗，还是每次不一样？

用户: 背调是 HR 发起，应该在 offer 接受后立刻做；
     IT 需要姓名、工号、入职日期，HR 统一汇总发给 IT；
     onboarding 没有标准，基本靠部门负责人自由发挥

助手: 好的，信息收集完毕，正在生成 SOP 文档...

     ---

     ## 流程文档：新员工入职流程
     **负责人：** HR 部门 | **最后更新：** 2026-05-21 | **审核周期：** 每年

     ### 目的
     规范新员工从 offer 接受到正式入职的全流程，避免背调未完成提前入职等合规风险。

     ### RACI 矩阵
     | 步骤 | 执行者（R） | 决策者（A） | 咨询方（C） | 知会方（I） |
     |---|---|---|---|---|
     | 发起背调 | HR | HR 主管 | 法务 | 用人部门 |
     | 汇总员工信息 | HR | HR | - | IT |
     | 开通系统账号 | IT | IT 负责人 | HR | 新员工 |
     | 签署劳动合同 | HR + 新员工 | HR 主管 | 法务 | - |
     | 安排 onboarding | 部门负责人 | 部门负责人 | HR | 新员工 |

     ### 详细步骤
     [完整步骤、时间节点、产出物...]

     ### 异常与边界情况
     | 场景 | 处理方式 |
     |---|---|
     | 背调未完成但入职日期已到 | 须经 HR 主管审批后方可办理入职手续，同步法务备案 |
     | IT 账号未及时开通 | HR 在入职前 3 个工作日催促，逾期上报 IT 负责人 |
```

**预期输出**:
- 完整 SOP Markdown 文档（目的、范围、RACI 矩阵、流程图、详细步骤、异常处理、指标）

---

## 🧠 Obsidian 知识库操作 (Obsidian Vault)

三层合一，按意图自动分流到工具层 / 分析层 / 运维层。下面按层各给一个示例。

### 工具层：移动笔记，全库链接自动跟着改

```
用户: 把 3_工作/工作知识库/5_理论知识/PCL/手眼标定.md 移到 标定理论/ 下，改名叫 手眼标定原理

助手: [工具层 · CLI 单次操作]

     执行:
       obsidian move path="3_工作/工作知识库/5_理论知识/PCL/手眼标定.md" \
                      to="3_工作/工作知识库/5_理论知识/标定理论/手眼标定原理.md"

     ✅ 已完成。全库指向该笔记的链接已自动更新:
          [[手眼标定]]          → [[手眼标定原理]]
          [[手眼标定|标定流程]]  → [[手眼标定原理|标定流程]]

     断链复核: obsidian unresolved | grep "手眼标定"
       → 无输出，无残留断链 ✅

     （刚改完等 1–3 秒让索引重建再查；前提是 Obsidian 正在运行）
```

### 分析层：全库体检并产出报告（只读）

```
用户: 知识库体检

助手: [分析层 · 只读，全库深度分析]

     Step 1 侦察
            一级目录 9 个，md 共 812 篇
            核对 AGENTS.md 承诺的导航文件 → 均存在 ✅

     Step 2 拆 7 个子集，一条消息内并行派发子代理…

     Step 3 主代理跑量化扫描（优先用 Obsidian CLI 口径）
            obsidian vault       → 812 文件 / 47 目录
            obsidian unresolved  → 23 处（已按目录过滤 Clippings 的图片外链）
            obsidian orphans     → 孤立页 31 篇（剔除日记后 12 篇）
            Python 脚本补：frontmatter 覆盖率、tags 四态解析…

     Step 4 汇总报告

     【执行摘要】全库整体健康，问题集中在元数据与孤立页
     · frontmatter 覆盖率 78%，缺 tags 的笔记 42 篇
     · 双链健康度 96%，悬空链接 23 处（多为指向概念的留白）
     · 疑似重复主题 3 组

     已产出:
       9_系统/知识库整体分析报告-2026-09-16.md
       9_系统/知识库整体分析报告-2026-09-16.html

     ⚠️ 全程只读，未修改任何文件。改进建议见报告 P0 / P1 / P2 分档。
```

### 运维层：日志写完后一键补齐关系

```
用户: 更新知识库

助手: [运维层 · 只读 + 限定写入]

     Step 1 目标日志 → 1_日志/2026/2026-09-16.md

     Step 2 Frontmatter 补全
            项目: [延锋座椅检测项目, 大3D项目支持]
            tags: [标定, 缺陷检测]        ← 按 协作约定 §4 词表
            总结: "完成手眼标定复测，焊缝检测方案评审通过"
            日期 / 类型已存在，跳过

     Step 3 项目关联与任务快照（只读）
            📋 延锋座椅检测项目：进行中 2 / 待开始 1 / 已完成 1
            ⚠️ 「XX新项目」不在 Project Manager 中，请确认是否新建
            进度记录：由 Dataview 自动查询，无需写入

     Step 4 链接健康检查（obsidian unresolved）
            ✅ 本篇涉及的链接全部可解析

     Step 5 index.md：新增 1 条 — [[手眼标定原理]]

     Step 6 项目活跃度检查（顺带执行）
            🔴 柔性点检框架项目（49 天前，严重停滞）

     📋 知识库更新完成 — 2026-09-16
     · 未维护总索引 / 主题索引（Dataview 动态生成，免维护）
     · 改动 2 个文件：日志 frontmatter + index.md
```

> **三层差别**：工具层做单次操作；分析层**只读**，只出报告不落笔；运维层**限定写入**，只动 frontmatter 与 index.md，且改动前先报告。

**预期输出**:
- 工具层：操作结果 + 断链复核结论
- 分析层：`9_系统/知识库整体分析报告-YYYY-MM-DD.md` + 同名 HTML（仅建议，不改任何文件）
- 运维层：被更新的 frontmatter / index.md 清单与逐步改动摘要

---

## 📝 周报生成 PDCA (Weekly Report PDCA)

### 场景：从本周 Obsidian 日志生成周报

```
用户: 生成这周周报
助手: [自动触发 weekly-report-pdca 流程]

     周范围：2026-W38（09-14 ~ 09-20）
     数据源：1_日志/2026/ 下本周 7 篇日志

     收集结果：
     - 工作记录：5 天有内容，09-20（周日）无日志，已跳过
     - wikilinks / 英语打卡 / 健身 / 生活板块均已提取

     归类并应用 PDCA，正在写入 Markdown...

     ---

     # 周报 2026-W38

     ## 本周摘要
     - 完成欣锐科技代码合并交付（09-16 客户确认）
     - 2D3D 合并 PLC 触发测试通过，节拍稳定在 1.8s
     - 桐庐螺栓抓取现场问题闭环

     ## 重点工作流：桐庐螺栓抓取
     | PDCA | 内容 |
     |---|---|
     | Plan | 解决抓取位姿偏差导致的漏抓，完成标准：连续 200 次无漏抓 |
     | Do | 重做手眼标定，调整点云分割阈值 |
     | Check | 现场连续 200 次测试，漏抓 0 次 ✅ |
     | Act | 固化参数并写入交付文档 |

     ## 下周计划
     | 优先级 | 事项 | 交付物 | 依赖 |
     |---|---|---|---|
     | P0 | 淮柴电芯方案评审 | 评审结论 | 客户排期 |

     ---

     ⏸ 已写入 1_日志/2026/2026-W38.md，请审批。
       确认内容后再生成 HTML（同目录 2026-W38.html）。

用户: 第二部分再压缩一下，其他没问题
助手: [更新 Markdown，等待确认] 已同步修改。确认后我生成 HTML。
```

**预期输出**:
- `1_日志/YYYY/YYYY-Www.md`（待审批，含周报 frontmatter）
- 用户同意后：同目录 `YYYY-Www.html`（响应式、可打印）

---

## 🤖 WorkBuddy 每日自动签到 (WorkBuddy Auto Check-in)

### 场景 1：首次搭建自动签到

```
用户: 帮我把 WorkBuddy 每日签到做成自动化
助手: [自动触发 workbuddy-auto-checkin 流程]

     1) 定位登录态：~/Library/Application Support/CodeBuddyExtension/
        Data/Public/auth/workbuddy-desktop.info
        - accessToken 存在 ✅（tokenType=Bearer）
        - auth.domain = copilot.tencent.com
        - expiresAt = 2026-11-15，未过期 ✅

     2) 落位脚本：~/.workbuddy/scripts/workbuddy_checkin.py
        只读校验：--check-only → status_http=200 ✅

     3) 执行签到：

        {
          "status": "ok",
          "action": "clicked",
          "points": 100,
          "msg": "领取成功，+100 积分，连续第 1 天"
        }

     4) 创建自动化：WorkBuddy 每日自动签到
        - 频率：每天 09:00
        - 状态：ACTIVE
        - 下次执行：2026-09-17 09:00

     完成。今天这一份已经领到了，可以打开 Buddy 加油站核对 +100。
```

### 场景 2：当日重复触发（幂等）

```
用户: 再签到一次
助手: [运行同一脚本]

     {
       "status": "ok",
       "action": "skip_already_signed",
       "msg": "今日已签到，无需重复领取"
     }

     今天已经领过了，接口是幂等的，不会重复发放。
```

### 场景 3：失败排查

```
用户: 今天签到好像没成功
助手: 运行脚本 → status=error，msg="未找到本机登录态文件"

     大概率是 WorkBuddy 客户端已退出登录。请：
     1. 确认客户端处于已登录状态（不是登出/游客）
     2. 确认电脑联网
     3. 确认 09:00 前后电脑开机且客户端未退出
     重新登录后我可以再跑一次。
```

**预期输出**:
- 签到结果 JSON（status / action / points / msg，不含任何 token）
- 运行日志 `~/.workbuddy/scripts/checkin.log`
- 一个 WorkBuddy 自带每日 09:00 自动化
- **不会**创建 crontab / launchd 等系统级定时任务

---

## 💡 使用提示

### 自动触发 vs 手动触发

大多数情况下直接描述需求即可，Skill 会自动触发：

```
✅ 直接说：帮我整理一下这个文件夹
❌ 不需要：先输入 /organize，再说整理文件夹
```

如果自动触发不生效，使用斜杠命令手动触发：

```bash
/organize                   # 文件夹整理（当前目录）
/organize ./path            # 文件夹整理（指定目录）
/visionmaster-scripthelper  # VisionMaster 脚本助手
/audience-adapter           # 受众适配助手
/sop-writer                 # SOP 文档生成
/obsidian                   # Obsidian 知识库（三层合一）
/weekly-report-pdca         # 周报生成 PDCA
/workbuddy-auto-checkin     # WorkBuddy 每日自动签到
```
