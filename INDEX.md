# VisionMaster 脚本技能索引

本文档提供 VisionMaster 脚本技能的快速索引，帮助您快速找到所需内容。

## 📚 文档导航

### 核心文档

| 文档 | 用途 | 适合人群 |
|------|------|----------|
| [README.md](README.md) | 快速入门指南 | 所有用户 |
| [SKILL.md](SKILL.md) | 完整技能文档 | 开发者 |
| [skill.json](skill.json) | 技能元数据 | 系统管理员 |
| [CREATION_SUMMARY.md](CREATION_SUMMARY.md) | 创建总结 | 维护者 |

### 示例代码

| 文件 | 语言 | 用途 | 难度 |
|------|------|------|------|
| [ScriptTemplate.cs](examples/ScriptTemplate.cs) | C# | 基础脚本模板 | ⭐ |
| [OpenCVExample.cs](examples/OpenCVExample.cs) | C# | OpenCV 图像处理 | ⭐⭐⭐ |
| [GlobalScriptExample.cs](examples/GlobalScriptExample.cs) | C# | 全局脚本控制 | ⭐⭐⭐⭐ |
| [RecvEventScript.py](examples/RecvEventScript.py) | Python | 接收事件脚本 | ⭐⭐ |
| [SendEventScript.py](examples/SendEventScript.py) | Python | 发送事件脚本 | ⭐⭐ |
| [ProtocolParseScript.py](examples/ProtocolParseScript.py) | Python | 协议解析脚本 | ⭐⭐⭐ |

## 🔍 功能索引

### 按功能分类

#### 数据输入输出

- [Int 类型操作](SKILL.md#int-类型操作)
- [Float 类型操作](SKILL.md#float-类型操作)
- [String 类型操作](SKILL.md#string-类型操作)
- [Byte 类型操作](SKILL.md#byte-类型操作十六进制数据)
- [ImageData 图像数据操作](SKILL.md#imagedata-图像数据操作)
- [数组操作（VM 4.2.0+）](SKILL.md#数组操作vm-420-优化)

#### 脚本生命周期

- [Init() 初始化](SKILL.md#init-初始化函数)
- [Process() 执行](SKILL.md#process-流程执行函数)
- [Dispose() 释放](SKILL.md#dispose-资源释放函数)
- [方法执行顺序](SKILL.md#方法执行顺序)

#### 全局变量与模块控制

- [全局变量操作](SKILL.md#全局变量操作)
- [模块结果获取](SKILL.md#模块结果获取)
- [模块参数设置](SKILL.md#模块参数设置)

#### 通信接口

- [PLC/Modbus 通信](SKILL.md#plcmodbus-通信)
- [TCP/UDP/串口通信](SKILL.md#tcpudp串口通信)

#### OpenCV 集成

- [Canny 边缘检测](SKILL.md#canny-边缘检测案例)
- [凸包算法](SKILL.md#凸包算法案例)
- [图像数据转换](SKILL.md#imagedata-转-mat)

#### 全局脚本

- [多流程控制](SKILL.md#多流程控制示例)
- [条件触发](SKILL.md#条件触发示例)
- [通信触发](SKILL.md#通信触发示例)

#### 通信脚本（Python）

- [接收事件脚本](SKILL.md#接收事件---脚本)
- [发送事件脚本](SKILL.md#发送事件---脚本)
- [协议解析脚本](SKILL.md#协议解析---脚本)

## 📖 学习路径

### 初学者路径

1. **了解基础**
   - [README.md - 快速开始](README.md#快速开始)
   - [SKILL.md - 核心概念](SKILL.md#核心概念)

2. **第一个脚本**
   - [ScriptTemplate.cs - 基础模板](examples/ScriptTemplate.cs)
   - [数据输入输出](SKILL.md#数据类型与接口)

3. **进阶功能**
   - [全局变量操作](SKILL.md#全局变量操作)
   - [模块参数控制](SKILL.md#模块参数设置)

### 进阶开发者路径

1. **图像处理**
   - [OpenCV 集成](SKILL.md#opencv-集成案例)
   - [OpenCVExample.cs](examples/OpenCVExample.cs)

2. **多流程控制**
   - [全局脚本](SKILL.md#全局脚本)
   - [GlobalScriptExample.cs](examples/GlobalScriptExample.cs)

3. **通信集成**
   - [通信接口](SKILL.md#通信接口)
   - [通信脚本](SKILL.md#通信脚本python)

### 高级开发者路径

1. **复杂协议处理**
   - [协议解析脚本](examples/ProtocolParseScript.py)
   - [接收/发送事件](examples/RecvEventScript.py, examples/SendEventScript.py)

2. **性能优化**
   - [最佳实践](SKILL.md#最佳实践)
   - [资源管理](SKILL.md#使用注意事项)

3. **第三方库集成**
   - [调用非托管库](SKILL.md#调用非托管库cc-dll)
   - [调用 C# 库](SKILL.md#调用-c-库)

## 🔧 常见任务快速查找

### 我想...

- **创建新脚本** → [ScriptTemplate.cs](examples/ScriptTemplate.cs)
- **处理图像** → [OpenCVExample.cs](examples/OpenCVExample.cs)
- **控制多个流程** → [GlobalScriptExample.cs](examples/GlobalScriptExample.cs)
- **解析通信数据** → [RecvEventScript.py](examples/RecvEventScript.py)
- **组装发送数据** → [SendEventScript.py](examples/SendEventScript.py)
- **解析十六进制** → [ProtocolParseScript.py](examples/ProtocolParseScript.py)
- **使用全局变量** → [全局变量操作](SKILL.md#全局变量操作)
- **控制模块参数** → [模块参数设置](SKILL.md#模块参数设置)
- **发送通信数据** → [通信接口](SKILL.md#通信接口)

## 📊 接口速查表

### 数据输入输出

| 功能 | 接口 | 示例 |
|------|------|------|
| 获取 int | `GetIntValue(name, ref value)` | `GetIntValue("in0", ref var0)` |
| 设置 int | `SetIntValue(name, value)` | `SetIntValue("out0", var0)` |
| 获取 float | `GetFloatValue(name, ref value)` | `GetFloatValue("in1", ref var1)` |
| 设置 float | `SetFloatValue(name, value)` | `SetFloatValue("out1", var1)` |
| 获取 string | `GetStringValue(name, ref value)` | `GetStringValue("in2", ref var2)` |
| 设置 string | `SetStringValue(name, value)` | `SetStringValue("out2", var2)` |
| 获取 byte[] | `GetBytesValue(name, ref value)` | `GetBytesValue("in3", ref var3)` |
| 设置 byte[] | `SetBytesValue(name, value)` | `SetBytesValue("out3", var3)` |
| 获取图像 | `GetImageValue(name, ref value)` | `GetImageValue("imgIn", ref img)` |
| 设置图像 | `SetImageValue(name, value)` | `SetImageValue("imgOut", img)` |

### 全局变量

| 功能 | 接口 | 示例 |
|------|------|------|
| 设置全局变量 | `GlobalVariableModule.SetValue(name, value)` | `SetValue("var1", "100")` |
| 获取全局变量 | `GlobalVariableModule.GetValue(name)` | `GetValue("var1")` |

### 模块控制

| 功能 | 接口 | 示例 |
|------|------|------|
| 获取模块结果 | `GetModule(name).GetValue(param)` | `GetModule("图像源 1").GetValue("Height")` |
| 设置模块参数 | `GetModule(name).SetValue(param, value)` | `GetModule("BLOB 分析 1").SetValue("FindNum", "4")` |

## 🐛 故障排查

### 常见问题

| 问题 | 解决方案 | 参考 |
|------|----------|------|
| 脚本编译失败 | 检查语法错误，查看错误信息 | [异常处理](SKILL.md#异常处理) |
| 图像处理报错 | 检查图像格式和尺寸 | [ImageData 操作](SKILL.md#imagedata-图像数据操作) |
| 模块访问失败 | 检查模块名称和 Group 访问 | [模块控制](SKILL.md#模块参数设置) |
| 通信数据解析错误 | 验证数据格式和长度 | [协议解析](examples/ProtocolParseScript.py) |
| 内存泄漏 | 检查资源释放 | [资源管理](SKILL.md#使用注意事项) |

## 📞 获取帮助

- 完整文档：[SKILL.md](SKILL.md)
- 快速入门：[README.md](README.md)
- 示例代码：[examples/](examples/)
- 官方文档：`..\Development\V4.x\Documentations`

## 🔗 外部资源

- [VM SDK 手册](SKILL.md#参考资料)
- [OpenCvSharp 文档](https://github.com/shimat/opencvsharp)
- [Python 文档](https://docs.python.org/3/)

---

**最后更新**：2026-04-15
**版本**：1.0.0
