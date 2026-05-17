# 使用示例 / Usage Examples

本文档提供每个 Skill 的实际使用示例。

---

## 🧠 记忆系统初始化 (Memory Init)

### 场景 1：交互式初始化

```
用户: 初始化记忆
助手: [自动触发记忆系统初始化流程]
     好的！让我先检查一下当前目录...

     当前目录下未发现 CLAUDE.md、MEMORY.md 或 memory/，可以直接初始化。

     让我了解一下你的情况：
     1. 你的角色是什么？（如：开发、产品、运营、SA）

用户: 开发
助手: 2. 你主要用 Claude 做什么？

用户: 写代码、排查 bug、做技术方案
助手: 3. 对话风格偏好？（简洁直接 / 详细展开 / 随意聊天）

用户: 简洁直接
助手: 4. 有什么特别的工作习惯要我知道的？（可选，可以跳过）

用户: 跳过
助手: 好的！正在生成...

     已生成：
     - CLAUDE.md（人设 + 记忆协议）
     - MEMORY.md（长期记忆初始模板）
     - memory/（每日记忆目录）

     使用方式：
     - 正常对话即可，我会自动读取记忆
     - 对话结束时我会问你要不要保存要点
     - 说"记住这个"可以随时存记忆
```

### 场景 2：已有文件时的处理

```
用户: /memory-init
助手: 检查当前目录... 发现已存在 CLAUDE.md。

     - CLAUDE.md ✅ 已存在
     - MEMORY.md ❌ 不存在
     - memory/ ❌ 不存在

     要覆盖 CLAUDE.md，还是只补缺少的文件？

用户: 只补缺少的
助手: 已生成：
     - MEMORY.md（长期记忆初始模板）
     - memory/（每日记忆目录）
     CLAUDE.md 保持不变。
```

**预期输出**:
- `CLAUDE.md`（人设 + 对话风格 + 记忆协议）
- `MEMORY.md`（长期记忆初始模板）
- `memory/` 目录

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

## 💡 使用提示

### 自动触发 vs 手动触发

大多数情况下直接描述需求即可，Skill 会自动触发：

```
✅ 直接说：帮我整理一下这个文件夹
❌ 不需要：先输入 /organize，再说整理文件夹
```

如果自动触发不生效，使用斜杠命令手动触发：

```bash
/memory-init          # 记忆系统初始化
/organize             # 文件夹整理（当前目录）
/organize ./path      # 文件夹整理（指定目录）
/vm-script-skill      # VisionMaster 脚本助手
```
