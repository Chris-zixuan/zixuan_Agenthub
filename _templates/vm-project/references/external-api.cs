// ============================================================
// 外部程序通信接口 — <项目名>
// ============================================================
// 本文件定义与外部程序通信的 C# 类和方法签名。
// 根据实际通信方式保留需要的部分，删除不需要的。
// ============================================================

using System;
using System.IO;
using System.IO.Pipes;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

// ============================================================
// 方式一：NamedPipe（命名管道）
// ============================================================

/// <summary>
/// NamedPipe 客户端封装
/// </summary>
public class PipeClient : IDisposable
{
    private NamedPipeClientStream _pipe;
    private readonly string _pipeName;
    private readonly int _timeoutMs;

    public bool IsConnected => _pipe != null && _pipe.IsConnected;

    public PipeClient(string pipeName, int timeoutMs = 5000)
    {
        _pipeName = pipeName;
        _timeoutMs = timeoutMs;
    }

    /// <summary>
    /// 连接到管道服务端
    /// </summary>
    public bool Connect()
    {
        try
        {
            _pipe = new NamedPipeClientStream(".", _pipeName, PipeDirection.InOut);
            _pipe.Connect(_timeoutMs);
            return true;
        }
        catch (TimeoutException)
        {
            // 连接超时，记录日志
            return false;
        }
    }

    /// <summary>
    /// 发送消息并接收响应
    /// </summary>
    public string SendMessage(string message)
    {
        if (_pipe == null || !_pipe.IsConnected)
            throw new InvalidOperationException("Pipe not connected");

        byte[] request = Encoding.UTF8.GetBytes(message);
        _pipe.Write(request, 0, request.Length);

        byte[] buffer = new byte[4096];
        int read = _pipe.Read(buffer, 0, buffer.Length);
        return Encoding.UTF8.GetString(buffer, 0, read);
    }

    public void Dispose()
    {
        _pipe?.Close();
        _pipe?.Dispose();
    }
}

// ============================================================
// 方式二：TCP Client
// ============================================================

/// <summary>
/// TCP 客户端封装
/// </summary>
public class TcpClientWrapper : IDisposable
{
    private TcpClient _client;
    private NetworkStream _stream;
    private readonly string _ip;
    private readonly int _port;
    private readonly int _timeoutMs;

    public bool IsConnected => _client != null && _client.Connected;

    public TcpClientWrapper(string ip, int port, int timeoutMs = 5000)
    {
        _ip = ip;
        _port = port;
        _timeoutMs = timeoutMs;
    }

    /// <summary>
    /// 连接到 TCP 服务端
    /// </summary>
    public bool Connect()
    {
        try
        {
            _client = new TcpClient();
            _client.ConnectAsync(_ip, _port).Wait(_timeoutMs);
            _stream = _client.GetStream();
            _stream.ReadTimeout = _timeoutMs;
            _stream.WriteTimeout = _timeoutMs;
            return _client.Connected;
        }
        catch (Exception)
        {
            return false;
        }
    }

    /// <summary>
    /// 发送字节数组并接收响应
    /// </summary>
    public byte[] Send(byte[] data)
    {
        _stream.Write(data, 0, data.Length);
        byte[] buffer = new byte[8192];
        int read = _stream.Read(buffer, 0, buffer.Length);
        byte[] result = new byte[read];
        Array.Copy(buffer, result, read);
        return result;
    }

    public void Dispose()
    {
        _stream?.Close();
        _stream?.Dispose();
        _client?.Close();
        _client?.Dispose();
    }
}

// ============================================================
// 方式三：SerialPort（串口）
// ============================================================

/// <summary>
/// 串口通信封装
/// </summary>
public class SerialPortWrapper : IDisposable
{
    private System.IO.Ports.SerialPort _sp;

    public SerialPortWrapper(string portName, int baudRate = 9600)
    {
        _sp = new System.IO.Ports.SerialPort(portName, baudRate);
        _sp.ReadTimeout = 2000;
        _sp.WriteTimeout = 2000;
    }

    public void Open() => _sp.Open();
    public bool IsOpen => _sp.IsOpen;

    public void Write(string msg) => _sp.Write(msg);
    public string ReadLine() => _sp.ReadLine();

    public void Dispose()
    {
        _sp?.Close();
        _sp?.Dispose();
    }
}

// ============================================================
// 方式四：External Process（调用外部 exe）
// ============================================================

/// <summary>
/// 外部进程调用封装
/// </summary>
public class ExternalProcessRunner : IDisposable
{
    private System.Diagnostics.Process _process;
    private readonly string _exePath;
    private readonly string _args;

    public ExternalProcessRunner(string exePath, string args)
    {
        _exePath = exePath;
        _args = args;
    }

    public string Run()
    {
        _process = new System.Diagnostics.Process
        {
            StartInfo = new System.Diagnostics.ProcessStartInfo
            {
                FileName = _exePath,
                Arguments = _args,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                StandardOutputEncoding = Encoding.UTF8
            }
        };

        _process.Start();
        string output = _process.StandardOutput.ReadToEnd();
        _process.WaitForExit();
        return output;
    }

    public void Dispose()
    {
        _process?.Dispose();
    }
}
