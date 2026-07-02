// ============================================================
// <项目名> — 完整流水线脚本模板
// ============================================================
// 本文件展示从输入 → 外部通信 → 处理 → 输出的完整流程。
// ============================================================

using System;
using Script.Methods;

public partial class UserScript : ScriptMethods, IProcessMethods
{
    // ---------- 外部通信 ----------
    // TODO: 根据 project-context.md 选择通信方式，调整字段类型

    /// <summary>外部通信客户端（Init 中初始化，Dispose 中释放）</summary>
    private PipeClient _pipeClient;    // 示例：NamedPipe，按需替换为 TcpClientWrapper 等

    // ---------- 处理计数 ----------
    private int processCount;

    // ---------- 缓存对象 ----------
    // TODO: 将每帧重复创建的大对象缓存为字段，避免 GC 压力

    /// <summary>
    /// 初始化
    /// </summary>
    public void Init()
    {
        processCount = 0;

        // TODO: 初始化外部通信连接
        // _pipeClient = new PipeClient("<管道名>", 5000);
        // _pipeClient.Connect();
    }

    /// <summary>
    /// 流程执行
    /// </summary>
    public bool Process()
    {
        processCount++;

        try
        {
            // Step 1: 读取输入变量（直接赋值）
            // int trigger = <in0>;
            // string productType = <in1>;

            // Step 2: 与外部程序通信
            // if (_pipeClient == null || !_pipeClient.IsConnected)
            // {
            //     _pipeClient = new PipeClient("<管道名>", 5000);
            //     _pipeClient.Connect();
            // }
            // string response = _pipeClient.SendMessage(request);
            // var result = ParseResponse(response);

            // Step 3: 业务处理逻辑
            // ...

            // Step 4: 设置输出变量（直接赋值）
            // <out0> = result.Code;
            // <out1> = resultImage;

            return true;
        }
        catch (Exception ex)
        {
            // 异常处理：设置错误码，输出错误信息
            // <out0> = -1;
            LogError($"Process error: {ex.Message}");
            return false;
        }
    }

    // ---------- 辅助方法 ----------

    // TODO: 在此添加项目专属的辅助方法，如协议解析、数据转换等

    /// <summary>
    /// 记录错误日志（通过全局变量）
    /// </summary>
    private void LogError(string message)
    {
        // GlobalVariableModule.SetValue("<调试信息变量名>", message);
    }

    // ---------- 资源释放 ----------

    /// <summary>
    /// 释放外部通信资源
    /// </summary>
    public virtual void Dispose()
    {
        _pipeClient?.Dispose();
    }
}
