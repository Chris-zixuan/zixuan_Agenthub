# VisionMaster 脚本开发技能

## 快速开始

本技能提供完整的 VisionMaster (VM) 脚本开发能力，包括 C# 脚本模块、全局脚本、通信脚本和 OpenCV 集成。

## 安装

本技能已集成到 CoPaw 工作区，无需额外安装。

**依赖要求**：
- .NET Framework 4.6.1+
- Python 3.8+（通信脚本）
- VisionMaster 3.x/4.x
- OpenCvSharp（可选，用于图像处理）

## 基本用法

### 1. 创建 C# 脚本模块

```csharp
using System;
using Script.Methods;

public partial class UserScript : ScriptMethods, IProcessMethods
{
    int processCount;
    
    public void Init()
    {
        processCount = 0;
    }
    
    public bool Process()
    {
        // 获取输入
        int inputValue = 0;
        GetIntValue("in0", ref inputValue);
        
        // 处理逻辑
        int result = inputValue * 2;
        
        // 设置输出
        SetIntValue("out0", result);
        
        return true;
    }
}
```

### 2. 使用全局变量

```csharp
// 设置全局变量
GlobalVariableModule.SetValue("counter", "100");

// 获取全局变量
object value = GlobalVariableModule.GetValue("counter");
int counter = int.Parse(value?.ToString() ?? "0");
```

### 3. 控制模块

```csharp
// 获取模块结果
object height = CurrentProcess.GetModule("图像源 1").GetValue("Height");

// 设置模块参数
CurrentProcess.GetModule("BLOB 分析 1").SetValue("FindNum", "4");
```

### 4. 图像处理（OpenCV）

```csharp
using OpenCvSharp;

public bool Process()
{
    ImageData img = new ImageData();
    GetImageValue("imgIn", ref img);
    
    // 转换为 Mat
    Mat mat = new Mat(img.Height, img.Width, MatType.CV_8UC1);
    Marshal.Copy(img.Buffer, 0, mat.Data, img.Buffer.Length);
    
    // Canny 边缘检测
    Mat edges = new Mat();
    Cv2.Canny(mat, edges, 50, 150);
    
    // 转回 ImageData
    byte[] buffer = new byte[edges.Width * edges.Height];
    edges.GetArray(0, 0, buffer);
    
    img.Buffer = buffer;
    img.Width = edges.Width;
    img.Height = edges.Height;
    
    SetImageValue("imgOut", img);
    
    mat.Dispose();
    edges.Dispose();
    
    return true;
}
```

### 5. 通信脚本（Python）

**接收事件脚本**：
```python
def getOutputParam():
    return {
        "id": int,
        "value": float,
        "name": str
    }

def handleMessage(info):
    # 解析格式："1#123.45#sensor1"
    parts = info.decode('utf-8').split('#')
    return [
        int(parts[0]),
        float(parts[1]),
        parts[2]
    ]
```

## 核心接口

### 数据输入输出

| 类型 | 获取接口 | 设置接口 |
|------|---------|---------|
| int | `GetIntValue(name, ref value)` | `SetIntValue(name, value)` |
| float | `GetFloatValue(name, ref value)` | `SetFloatValue(name, value)` |
| string | `GetStringValue(name, ref value)` | `SetStringValue(name, value)` |
| byte[] | `GetBytesValue(name, ref value)` | `SetBytesValue(name, value)` |
| ImageData | `GetImageValue(name, ref value)` | `SetImageValue(name, value)` |

### 数组操作（VM 4.2.0+）

```csharp
// 优化接口（推荐）
SetIntArrayValue("out", array, 0, array.Length);
SetFloatArrayValue("out", array, 0, array.Length);
SetStringArrayValue("out", array, 0, array.Length);

// 旧接口（需循环）
for (int i = 0; i < array.Length; i++)
{
    SetIntValueByIndex("out", array[i], i, array.Length);
}
```

### 全局变量

```csharp
GlobalVariableModule.SetValue("varName", "value");
object value = GlobalVariableModule.GetValue("varName");
```

### 模块控制

```csharp
// 获取结果
object result = CurrentProcess.GetModule("ModuleName").GetValue("ParamName");

// 设置参数
CurrentProcess.GetModule("ModuleName").SetValue("ParamName", "value");

// Group 内模块
CurrentProcess.GetModule("Group1.ModuleName").SetValue("ParamName", "value");
```

### 通信

```csharp
// PLC/Modbus
GlobalCommunicateModule.GetDevice(0).GetAddress(0)
    .SendData("data", DataType.StringType);

// TCP/UDP/串口
GlobalCommunicateModule.GetDevice(0).SendData("data");
GlobalCommunicateModule.GetDevice(0).SendData(byteArray);
```

## 生命周期

```
加载方案
    ↓
编译脚本
    ↓
调用 Init() ← 仅一次
    ↓
┌───────────────┐
│  流程运行     │
│  调用 Process()│ ← 每次执行
└───────────────┘
    ↓
关闭方案/重新编译
    ↓
调用 Dispose() ← 释放资源
```

## 最佳实践

### 1. 资源管理

```csharp
public partial class UserScript : ScriptMethods, IProcessMethods
{
    private Mat cachedMat;
    
    public void Init()
    {
        // 初始化资源
        cachedMat = new Mat();
    }
    
    public bool Process()
    {
        // 使用缓存的资源
        // ...
        return true;
    }
    
    public virtual void Dispose()
    {
        // 释放资源
        cachedMat?.Dispose();
    }
}
```

### 2. 异常处理

```csharp
public bool Process()
{
    try
    {
        // 业务代码
        return true;
    }
    catch (Exception ex)
    {
        // 记录日志或弹框
        MessageBox.Show($"Error: {ex.Message}");
        return false;
    }
}
```

### 3. 性能优化

- 在 `Init()` 中创建可复用对象
- 避免在 `Process()` 中频繁分配内存
- 及时释放图像和文件资源
- 使用数组优化接口代替循环

## 典型应用

1. **图像处理**：Canny、凸包、轮廓分析
2. **数据转换**：坐标排序、字符串处理
3. **模块控制**：动态调整参数、获取结果
4. **通信集成**：PLC、Modbus、TCP/UDP
5. **多流程协调**：全局脚本控制流程切换
6. **数据存储**：保存图像、写入日志

## 注意事项

⚠️ **重要提醒**：

1. 脚本中**不支持**调用控制器管理发送 IO 数据
2. 避免在脚本中操作非托管资源（如必须，需在 Process 中释放）
3. `MessageBox.Show()` 会暂停流程，慎用
4. 获取/设置模块参数仅作用于**当前流程**
5. Group 内模块需使用 `Group 名称。模块名称` 格式

## 调试

1. 点击**导出工程**生成 VS 工程
2. 使用 Visual Studio 打开并添加断点
3. 修改后点击**导入**更新脚本
4. 使用**预编译**检查语法错误
5. 使用**执行**测试功能

## 示例路径

VM 4.2.0 示例程序位置：
- 接收事件脚本：`...\VisionMaster4.2.0\Applications\VmModuleProxy\x64\RecvEventTest.py`
- 发送事件脚本：`...\VisionMaster4.2.0\Applications\VmModuleProxy\x64\SendEventTest.py`
- 协议解析脚本：`...\VisionMaster4.2.0\Applications\Module(sp)\x64\Communication\DataAnalysisModule\Receive.py`

## 参考资料

- VM SDK 手册：`..\Development\V4.x\Documentations`
- 完整文档：参见 `SKILL.md`

## 版本历史

- **1.0.0** - 初始版本，基于 VM 文档生成
  - 支持 VM 3.x/4.x/4.2.0+
  - 完整的 C# 脚本接口
  - Python 通信脚本
  - OpenCV 集成示例
