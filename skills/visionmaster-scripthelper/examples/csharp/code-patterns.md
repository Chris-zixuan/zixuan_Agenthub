# VM 脚本代码模式库

本文件提炼常见 VM 脚本场景的代码模式。**所有模式使用直接赋值方式读写变量**，不使用 Get/Set 遗留接口。

---

## 模式 1：基础数据透传

**场景**：获取输入，简单处理，设置输出

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

    /// <summary>
    /// 流程执行函数
    /// </summary>
    public bool Process()
    {
        // 直接赋值获取输入
        int inputValue = in0;

        // 处理逻辑
        int result = inputValue * 2;

        // 直接赋值设置输出
        out0 = result;

        processCount++;
        return true;
    }
}
```

---

## 模式 2：多类型数据读写

**场景**：同时处理 int、float、string、byte[] 等多种类型

```csharp
/// <summary>
/// 流程执行函数
/// </summary>
public bool Process()
{
    // 直接赋值获取各类型输入
    int intVal = in0;
    float floatVal = in1;
    string strVal = in2;
    byte[] byteVal = in3;

    // 处理逻辑...

    // 直接赋值设置各类型输出
    out0 = intVal;
    out1 = floatVal;
    out2 = strVal;
    out3 = byteVal;

    return true;
}
```

---

## 模式 3：数组数据处理

**场景**：批量处理数组数据

```csharp
/// <summary>
/// 流程执行函数
/// </summary>
public bool Process()
{
    // 直接赋值获取数组输入
    int[] inputArr = in0;

    // 处理逻辑 — 例如：每个元素乘以系数
    int factor = factorIn;

    int[] resultArr = new int[inputArr.Length];
    for (int i = 0; i < inputArr.Length; i++)
    {
        resultArr[i] = inputArr[i] * factor;
    }

    // 直接赋值设置数组输出
    out0 = resultArr;

    return true;
}
```

---

## 模式 4：图像处理管道（含 OpenCV）

**场景**：使用 OpenCvSharp 进行图像处理

```csharp
using System;
using Script.Methods;
using OpenCvSharp;

public partial class UserScript : ScriptMethods, IProcessMethods
{
    int processCount;

    public void Init()
    {
        processCount = 0;
    }

    /// <summary>
    /// 流程执行函数
    /// </summary>
    public bool Process()
    {
        // 1. 直接赋值获取输入图像
        ImageData imgIn = inputImage;

        if (imgIn.Buffer == null || imgIn.Width <= 0 || imgIn.Height <= 0)
        {
            ConsoleWrite("图像数据无效");
            return false;
        }

        // 2. ImageData → Mat（转换方法见 references/Script.ExMethods.cs）
        Mat srcMat = ImageDataToMat(imgIn);

        // 3. 图像处理逻辑（在此替换为实际算法）
        Mat resultMat = new Mat();
        // ... 算法处理 ...

        // 4. Mat → ImageData
        ImageData imgOut = MatToImageData(resultMat);

        // 5. 直接赋值设置输出
        outputImage = imgOut;

        // 6. 释放临时资源
        srcMat.Dispose();
        resultMat.Dispose();

        processCount++;
        return true;
    }
}
```

> `ImageDataToMat` / `MatToImageData` 的完整实现见 [references/Script.ExMethods.cs](../../references/Script.ExMethods.cs) 或 [02-canny-edge-detection.cs](02-canny-edge-detection.cs)

---

## 模式 4b：图像处理管道（含 System.Drawing.Bitmap）

**场景**：使用 `System.Drawing.Bitmap` 进行图像处理（无需 OpenCvSharp）

```csharp
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using Script.Methods;

public partial class UserScript : ScriptMethods, IProcessMethods
{
    int processCount;

    public void Init()
    {
        processCount = 0;
    }

    /// <summary>
    /// 流程执行函数
    /// </summary>
    public bool Process()
    {
        // 1. 直接赋值获取输入图像
        ImageData imgIn = inputImage;

        if (imgIn.Buffer == null || imgIn.Width <= 0 || imgIn.Height <= 0)
        {
            ConsoleWrite("图像数据无效");
            return false;
        }

        // 2. ImageData → Bitmap（转换方法见 references/Script.ExMethods.cs）
        Bitmap srcBmp = ImageDataToBitmap(imgIn);

        // 3. 图像处理逻辑（在此替换为实际算法）
        // 例如：使用 Graphics 绘制、像素级操作等
        Bitmap resultBmp = ProcessWithBitmap(srcBmp);

        // 4. Bitmap → ImageData
        ImageData imgOut = BitmapToImageData(resultBmp);

        // 5. 直接赋值设置输出
        outputImage = imgOut;

        // 6. 释放临时资源
        srcBmp.Dispose();
        resultBmp.Dispose();

        processCount++;
        return true;
    }

    /// <summary>
    /// 使用 Bitmap 处理图像的示例方法
    /// </summary>
    /// <param name="srcBmp">输入 Bitmap</param>
    /// <returns>处理后的 Bitmap</returns>
    private Bitmap ProcessWithBitmap(Bitmap srcBmp)
    {
        // 示例：创建副本并处理
        Bitmap result = new Bitmap(srcBmp.Width, srcBmp.Height, srcBmp.PixelFormat);
        using (Graphics g = Graphics.FromImage(result))
        {
            g.DrawImage(srcBmp, 0, 0);
            // 在此添加绘制/处理逻辑...
        }
        return result;
    }
}
```

> `BitmapToImageData` / `ImageDataToBitmap` 的完整实现见 [references/Script.ExMethods.cs](../../references/Script.ExMethods.cs)。支持 `Format8bppIndexed`（MONO8）和 `Format24bppRgb`（RGB24）两种像素格式，转换时自动处理 stride 对齐和 BGR/RGB 通道交换。

---

## 模式 5：ROI 处理

**场景**：获取 ROI，进行几何变换或分割

```csharp
/// <summary>
/// 流程执行函数
/// </summary>
public bool Process()
{
    // 直接赋值获取 ROI 输入
    RoiboxData[] rois = roiIn;

    if (rois == null || rois.Length == 0)
    {
        ConsoleWrite("ROI 数据为空");
        return false;
    }

    // 处理逻辑 — 例如：计算第一个 ROI 的四个角点
    RoiboxData roi = rois[0];
    float angle = roi.Angle;
    float rad = angle * (float)Math.PI / 180f;
    float cosA = (float)Math.Cos(rad);
    float sinA = (float)Math.Sin(rad);

    float halfW = roi.Width / 2f;
    float halfH = roi.Height / 2f;

    float[][] corners = new float[4][];
    float[][] offsets = new float[][]
    {
        new float[] { -halfW, -halfH },
        new float[] {  halfW, -halfH },
        new float[] {  halfW,  halfH },
        new float[] { -halfW,  halfH }
    };

    for (int i = 0; i < 4; i++)
    {
        float rx = offsets[i][0] * cosA - offsets[i][1] * sinA;
        float ry = offsets[i][0] * sinA + offsets[i][1] * cosA;
        corners[i] = new float[] { roi.CenterX + rx, roi.CenterY + ry };
    }

    // 直接赋值设置输出...

    return true;
}
```

---

## 模式 6：ROI 网格分割

**场景**：将一个 ROI 分割为 rows × cols 的子 ROI 数组

```csharp
/// <summary>
/// 流程执行函数
/// </summary>
public bool Process()
{
    // 直接赋值获取输入
    int rows = rowsIn;
    int cols = colsIn;
    RoiboxData[] roiArr = roiIn;

    if (rows <= 0 || cols <= 0 || roiArr == null || roiArr.Length == 0)
    {
        ConsoleWrite("输入参数无效");
        return false;
    }

    RoiboxData roi = roiArr[0];
    RoiboxData[] result = SplitRoiGrid(roi, rows, cols);

    // 直接赋值设置输出
    roiOut = result;

    processCount++;
    return true;
}

/// <summary>
/// 将 ROI 按行列分割为子 ROI 数组
/// </summary>
/// <param name="roi">原始 ROI</param>
/// <param name="rows">行数</param>
/// <param name="cols">列数</param>
/// <returns>子 ROI 数组</returns>
private RoiboxData[] SplitRoiGrid(RoiboxData roi, int rows, int cols)
{
    float cellWidth = roi.Width / cols;
    float cellHeight = roi.Height / rows;
    float rad = roi.Angle * (float)Math.PI / 180f;
    float cosA = (float)Math.Cos(rad);
    float sinA = (float)Math.Sin(rad);

    RoiboxData[] result = new RoiboxData[rows * cols];
    int index = 0;

    for (int r = 0; r < rows; r++)
    {
        for (int c = 0; c < cols; c++)
        {
            float offsetX = (c - (cols - 1) / 2f) * cellWidth;
            float offsetY = (r - (rows - 1) / 2f) * cellHeight;

            float rotatedX = offsetX * cosA - offsetY * sinA;
            float rotatedY = offsetX * sinA + offsetY * cosA;

            RoiboxData cell = new RoiboxData();
            cell.CenterX = roi.CenterX + rotatedX;
            cell.CenterY = roi.CenterY + rotatedY;
            cell.Width = cellWidth;
            cell.Height = cellHeight;
            cell.Angle = roi.Angle;
            result[index++] = cell;
        }
    }

    return result;
}
```

---

## 模式 7：全局变量控制流程

**场景**：通过全局变量在模块间传递状态或配置

```csharp
/// <summary>
/// 流程执行函数
/// </summary>
public bool Process()
{
    // 读取全局变量
    object val = GlobalVariableModule.GetValue("mode");
    int mode = int.Parse(val?.ToString() ?? "0");

    // 根据全局变量选择逻辑分支
    int result = 0;
    switch (mode)
    {
        case 0:
            result = ProcessModeA();
            break;
        case 1:
            result = ProcessModeB();
            break;
        default:
            ConsoleWrite("未知模式: " + mode);
            return false;
    }

    // 写入全局变量 + 直接赋值输出
    GlobalVariableModule.SetValue("result", result.ToString());
    out0 = result;

    return true;
}

/// <summary>
/// 模式 A 处理
/// </summary>
private int ProcessModeA()
{
    // 逻辑...
    return 0;
}

/// <summary>
/// 模式 B 处理
/// </summary>
private int ProcessModeB()
{
    // 逻辑...
    return 0;
}
```

---

## 模式 8：模块参数动态调整

**场景**：根据条件动态设置其他模块的参数

```csharp
/// <summary>
/// 流程执行函数
/// </summary>
public bool Process()
{
    // 获取某个模块的结果
    object obj = CurrentProcess.GetModule("图像源1").GetValue("Height");
    if (obj == null)
    {
        ConsoleWrite("获取模块结果失败");
        return false;
    }

    int height = int.Parse(obj.ToString());

    // 根据结果调整另一个模块的参数
    if (height > 1000)
    {
        CurrentProcess.GetModule("BLOB分析1").SetValue("FindNum", "10");
    }
    else
    {
        CurrentProcess.GetModule("BLOB分析1").SetValue("FindNum", "5");
    }

    return true;
}
```

---

## 模式 9：带状态的多次执行

**场景**：Process() 需要在多次执行间保持状态

```csharp
public partial class UserScript : ScriptMethods, IProcessMethods
{
    int processCount;
    int totalCount;
    float accumulatedValue;

    public void Init()
    {
        processCount = 0;
        totalCount = 0;
        accumulatedValue = 0f;
    }

    /// <summary>
    /// 流程执行函数
    /// </summary>
    public bool Process()
    {
        processCount++;
        totalCount++;

        // 直接赋值获取输入
        float inputVal = in0;

        // 累积计算
        accumulatedValue += inputVal;

        // 每 N 次输出平均值
        if (totalCount % 10 == 0)
        {
            float avg = accumulatedValue / totalCount;
            out0 = avg;
            countOut = totalCount;
        }

        return true;
    }

    public virtual void Dispose()
    {
    }
}
```

---

## 模式 10：通信数据发送

**场景**：通过 TCP/PLC/Modbus 发送处理结果

> **边界说明**：本模式仅限**数据发送**（将脚本计算结果通过已有通信设备发送出去）。VM 脚本层不支持协议解析、控制器 IO 发送、自定义通信协议实现。如需上述能力，建议改用外部程序或上位机方案。

```csharp
/// <summary>
/// 流程执行函数
/// </summary>
public bool Process()
{
    // 直接赋值获取处理结果
    int result = resultIn;

    // TCP/UDP/串口发送
    string msg = result.ToString();
    int ret = GlobalCommunicateModule.GetDevice(1).SendData(msg);
    if (ret != 0)
    {
        ConsoleWrite("TCP 发送失败");
    }

    // PLC 发送
    ret = GlobalCommunicateModule.GetDevice(2).GetAddress(1).SendData(result.ToString(), DataType.Int);
    if (ret != 0)
    {
        ConsoleWrite("PLC 发送失败");
    }

    return true;
}
```

---

## 模式 11：异常处理模板

**场景**：需要健壮的错误处理

```csharp
/// <summary>
/// 流程执行函数
/// </summary>
public bool Process()
{
    try
    {
        // 业务逻辑...

        return true;
    }
    catch (Exception ex)
    {
        ConsoleWrite("执行异常: " + ex.Message);
        return false;
    }
}
```

---

## 模式 12：资源管理模板

**场景**：需要使用非托管资源（Mat、文件句柄等）

```csharp
public partial class UserScript : ScriptMethods, IProcessMethods
{
    int processCount;
    private Mat cachedMat;

    public void Init()
    {
        processCount = 0;
        cachedMat = new Mat();
    }

    /// <summary>
    /// 流程执行函数
    /// </summary>
    public bool Process()
    {
        // 使用缓存的资源
        // ...

        return true;
    }

    public virtual void Dispose()
    {
        cachedMat?.Dispose();
    }
}
```

---

---

## 模式 13：轮廓仪深度图转点云

**场景**：从 `StereoImageData` 逐行提取有效点，转换为物理坐标点云


```csharp
/// <summary>
/// 流程执行函数：深度图转点云
/// </summary>
public bool Process()
{
   
    StereoImageData rangeImg = 深度图in;

    float xScale  = rangeImg.Xscale;
    float zScale  = rangeImg.Zscale;
    int   xOffset = rangeImg.Xoffset;
    int   zOffset = rangeImg.Zoffset;

    int width  = rangeImg.ProfileRangeImage.Width;
    int height = rangeImg.ProfileRangeImage.Height;
    byte[] buf = rangeImg.ProfileRangeImage.Buffer;

    // 预分配（最坏情况 width * height 个有效点）
    float[] px = new float[width * height];
    float[] pz = new float[width * height];
    int ptNum = 0;

    for (int row = 0; row < height; row++)
    {
        int rowByte = row * width * 2;
        for (int col = 0; col < width; col++)
        {
            short raw = BitConverter.ToInt16(buf, rowByte + col * 2);
            if (raw == -32768)  // 无效值跳过
                continue;

            px[ptNum] = col * xScale + xOffset;
            pz[ptNum] = raw * zScale + zOffset;
            ptNum++;
        }
    }

    // 直接赋值输出（float 数组变量）
    pXOut    = px;
    pZOut    = pz;
    ptNumOut = ptNum;

    return true;
}
```

> 完整示例见 [05-stereo-depth-pointcloud.cs](05-stereo-depth-pointcloud.cs)

---

## 模式 14：深度图区间过滤并回写

**场景**：将深度图中超出 Z 阈值的像素置为无效值（-32768），输出修改后的 `StereoImageData`

```csharp
/// <summary>
/// 流程执行函数：深度图区间过滤
/// </summary>
public bool Process()
{
    StereoImageData rangeImg = 深度图in;

    int width  = rangeImg.ProfileRangeImage.Width;
    int height = rangeImg.ProfileRangeImage.Height;
    byte[] buf = rangeImg.ProfileRangeImage.Buffer;

    // Buffer 解析为 short 数组（S16）
    short[] depth = new short[width * height];
    for (int i = 0; i < depth.Length; i++)
        depth[i] = BitConverter.ToInt16(buf, i * 2);

    // 按阈值过滤
    short zUpRaw   = zUpIn;   // 保留上限（原始 S16 值）
    short zDownRaw = zDownIn; // 保留下限（原始 S16 值）
    for (int i = 0; i < depth.Length; i++)
    {
        if (depth[i] != -32768 && (depth[i] > zUpRaw || depth[i] < zDownRaw))
            depth[i] = -32768;
    }

    // 回写到 Buffer
    byte[] outBuf = new byte[depth.Length * 2];
    for (int i = 0; i < depth.Length; i++)
        BitConverter.GetBytes(depth[i]).CopyTo(outBuf, i * 2);
    rangeImg.ProfileRangeImage.Buffer = outBuf;

    // 直接赋值输出 STEREO_IMAGE
    outImage = rangeImg;

    return true;
}
```

---

## 模式组合指南

| 用户需求              | 推荐模式组合               |
| --------------------- | -------------------------- |
| 简单计算              | 模式 1 + 模式 11           |
| 多类型数据转发        | 模式 2                     |
| 批量数据处理          | 模式 3                     |
| 图像滤波/检测         | 模式 4 + 模式 12           |
| 图像处理（无需 OpenCV）| 模式 4b + 模式 12         |
| ROI 分割/变换         | 模式 5 或 模式 6           |
| 流程控制/分支         | 模式 7 + 模式 8            |
| 统计/累积计算         | 模式 9                     |
| 结果通信发送          | 任意处理模式 + 模式 10     |
| 深度图转点云          | 模式 13                    |
| 深度图区间过滤        | 模式 14                    |
| 深度图预处理 + 转点云 | 模式 14 + 模式 13          |
