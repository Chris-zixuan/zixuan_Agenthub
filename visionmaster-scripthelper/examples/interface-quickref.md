# VM 脚本接口速查索引

本文件从 `references/` 中的原始 `.cs` 文件提炼，按**使用场景**分类，便于代码生成时快速定位接口签名。

> **重要**：VM 脚本的变量读写优先使用**直接赋值**方式（如 `out0 = in0`），不再使用 Get/Set 遗留接口。遗留接口仅作为动态变量名访问的后备方案保留。

---

## 1. 变量类型映射

### 标量类型（直接读写）

| VM 类型 | 脚本 C# 类型 | 读取示例                 | 写入示例        |
| ------- | ------------ | ------------------------ | --------------- |
| INT     | `int`        | `int val = in0;`         | `out0 = val;`   |
| FLOAT   | `float`      | `float val = in1;`       | `out1 = val;`   |
| STRING  | `string`     | `string val = in2;`      | `out2 = val;`   |
| DOUBLE  | `double`     | `double val = in3;`      | `out3 = val;`   |
| BYTE    | `byte[]`     | `byte[] val = in4;`      | `out4 = val;`   |
| IMAGE   | `ImageData`  | `ImageData img = imgIn;` | `imgOut = img;` |

### 数组类型（直接读写）

| VM 类型     | 脚本 C# 类型 | 读取示例              | 写入示例      |
| ----------- | ------------ | --------------------- | ------------- |
| INT 数组    | `int[]`      | `int[] arr = in0;`    | `out0 = arr;` |
| FLOAT 数组  | `float[]`    | `float[] arr = in1;`  | `out1 = arr;` |
| STRING 数组 | `string[]`   | `string[] arr = in2;` | `out2 = arr;` |
| DOUBLE 数组 | `double[]`   | `double[] arr = in3;` | `out3 = arr;` |

### 复合类型（`<Type>Data[]` 数组）

| VM 类型       | 脚本 C# 类型         | 读取示例                       | 写入示例      |
| ------------- | -------------------- | ------------------------------ | ------------- |
| POINT         | `PointData[]`        | `PointData[] pts = in0;`       | `out0 = pts;` |
| CIRCLE        | `CircleData[]`       | `CircleData[] cs = in0;`       | `out0 = cs;`  |
| ROIBOX        | `RoiboxData[]`       | `RoiboxData[] rs = in0;`       | `out0 = rs;`  |
| RECT          | `RectData[]`         | `RectData[] rs = in0;`         | `out0 = rs;`  |
| LINE          | `LineData[]`         | `LineData[] ls = in0;`         | `out0 = ls;`  |
| ELLIPSE       | `EllipseData[]`      | `EllipseData[] es = in0;`      | `out0 = es;`  |
| ANNULUS       | `AnnulusData[]`      | `AnnulusData[] ann = in0;`     | `out0 = ann;` |
| POLYGON       | `PolygonData[]`      | `PolygonData[] ps = in0;`      | `out0 = ps;`  |
| CONTOUR_POINT | `ContourPointData[]` | `ContourPointData[] cs = in0;` | `out0 = cs;`  |

---

## 2. 数据结构字段速查

### ImageData

```csharp
public class ImageData
{
    public byte[] Buffer { get; set; }
    public int Width { get; set; }
    public int Height { get; set; }
    public ImagePixelFormate PixelFormat { get; set; }
}
```

**ImagePixelFormate**：`MONO8 = 17301505`（灰度），`RGB24 = 35127316`（彩色）

### RoiboxData

```csharp
public class RoiboxData
{
    public float CenterX, CenterY, Width, Height, Angle;
}
```

### PointData

```csharp
public class PointData
{
    public float PointX, PointY;
}
```

### 其他几何结构

| 结构               | 字段                                                                            |
| ------------------ | ------------------------------------------------------------------------------- |
| `CircleData`       | `CenterX`, `CenterY`, `Radius`                                                  |
| `RectData`         | `CenterX`, `CenterY`, `Width`, `Height`                                         |
| `LineData`         | `StartPointX`, `StartPointY`, `EndPointX`, `EndPointY`                          |
| `EllipseData`      | `CenterX`, `CenterY`, `MajorRadius`, `MinorRadius`, `Angle`                     |
| `AnnulusData`      | `CenterX`, `CenterY`, `InnerRadius`, `OuterRadius`, `StartAngle`, `AngleExtend` |
| `PolygonData`      | `PointNum`, `PointXArray`, `PointYArray`                                        |
| `ContourPointData` | `PointX`, `PointY`, `PointScore`                                                |

---

## 3. Mat ↔ ImageData 转换

见 [Script.ExMethods.cs](../references/Script.ExMethods.cs)

```csharp
// Mat → ImageData
ImageData imgOut = MatToImageData(matImage);

// ImageData → Mat
Mat matImage = ImageDataToMat(imgData);
```

---

## 3b. Bitmap ↔ ImageData 转换

见 [Script.ExMethods.cs](../references/Script.ExMethods.cs)

```csharp
// Bitmap → ImageData
ImageData imgOut = BitmapToImageData(bmpImage);

// ImageData → Bitmap
Bitmap bmpImage = ImageDataToBitmap(imgData);
```

**支持的像素格式：**

| Bitmap 像素格式 | ImageData 像素格式 | 说明 |
|---|---|---|
| `Format8bppIndexed` | `MONO8` | 灰度图，`ImageDataToBitmap` 会自动设置 256 级灰度调色板 |
| `Format24bppRgb` | `RGB24` | 彩色图，转换时自动交换 BGR↔RGB 通道顺序 |

**注意事项：**
- Bitmap 使用 BGR 通道顺序，ImageData 使用 RGB 通道顺序，转换方法内部自动处理
- `ImageDataToBitmap` 返回的 Bitmap 需要调用方在使用完毕后 `Dispose()`
- 不支持其他像素格式（如 `Format32bppArgb`），如需处理请先转换为上述两种格式

---

## 4. 全局变量

| 操作 | 接口                                                                         | 备注                                  |
| ---- | ---------------------------------------------------------------------------- | ------------------------------------- |
| 设置 | `GlobalVariableModule.SetValue(string paramName, string paramValue)` → `int` | 值统一为 string                       |
| 获取 | `GlobalVariableModule.GetValue(string paramName)` → `object`                 | 返回 object，需转 string 再转目标类型 |

**代码模式：**

```csharp
// 设置
GlobalVariableModule.SetValue("counter", "100");

// 获取并转换
object val = GlobalVariableModule.GetValue("counter");
int counter = int.Parse(val?.ToString() ?? "0");
```

---

## 5. 模块控制

| 操作     | 接口                                                                | 备注                         |
| -------- | ------------------------------------------------------------------- | ---------------------------- |
| 获取模块 | `CurrentProcess.GetModule(string moduleName)` → `Module`            | Group 内用 `"Group1.模块名"` |
| 获取结果 | `Module.GetValue(string paramValueName)` → `object`                 | 返回 null 表示异常           |
| 设置参数 | `Module.SetValue(string paramValueName, string paramValue)` → `int` | 0=成功                       |

**代码模式：**

```csharp
// 获取模块结果
object height = CurrentProcess.GetModule("图像源1").GetValue("Height");
int h = int.Parse(height?.ToString() ?? "0");

// 设置模块参数
CurrentProcess.GetModule("BLOB分析1").SetValue("FindNum", "4");

// Group 内模块
object result = CurrentProcess.GetModule("组合模块1.图像源1").GetValue("Height");
```

---

## 6. 通信发送

VM 脚本层不支持直接发送控制器 IO 或通信协议（TCP/UDP/串口等）。如需通信能力，建议改用外部程序、上位机或其他 SDK 方案，通过全局变量与 VM 脚本交换数据。

---

## 7. 调试与显示

| 操作           | 接口                                                          | 备注                 |
| -------------- | ------------------------------------------------------------- | -------------------- |
| DebugView 输出 | `ConsoleWrite(string content)`                                | 不会暂停流程         |
| 弹窗提示       | `ShowMessageBox(string msg)`                                  | 会暂停流程，仅调试用 |
| 显示图像       | `ShowImage(ImageData imageData)`                              | 需 6210/7120 加密狗  |
| 绘制图形       | `DrawShape(object shapeData, ShapeConfig shapeConfig = null)` | 需 6210/7120 加密狗  |

---

## 8. 生命周期方法

| 方法        | 修饰                  | 时机              | 用途                     |
| ----------- | --------------------- | ----------------- | ------------------------ |
| `Init()`    | `public void`         | 加载方案/预编译   | 初始化变量、创建句柄     |
| `Process()` | `public bool`         | 每次流程执行      | 业务逻辑；返回 true=成功 |
| `Dispose()` | `public virtual void` | 关闭方案/重新编译 | 释放资源、关闭句柄       |

---

## 9. 遗留 Get/Set 接口（不推荐，仅后备）

以下接口保留用于方案兼容，**新代码不要使用**。只有当需要按变量名字符串动态访问时才考虑。

### 标量 Get 接口

| 接口                                                        | 返回值 |
| ----------------------------------------------------------- | ------ |
| `GetIntValue(string name, ref int value)` → `int`           | 0=成功 |
| `GetFloatValue(string name, ref float value)` → `int`       | 0=成功 |
| `GetStringValue(string name, ref string value)` → `int`     | 0=成功 |
| `GetBytesValue(string name, ref byte[] value)` → `int`      | 0=成功 |
| `GetDoubleValue(string name, ref double value)` → `int`     | 0=成功 |
| `GetIMAGEValue(string name, ref Image value)` → `int`       | 0=成功 |
| `GetRoiboxValue(string name, ref RoiboxData value)` → `int` | 0=成功 |

### 标量 Set 接口

| 接口                                                    | 返回值 |
| ------------------------------------------------------- | ------ |
| `SetIntValue(string key, int value)` → `int`            | 0=成功 |
| `SetFloatValue(string key, float value)` → `int`        | 0=成功 |
| `SetStringValue(string key, string value)` → `int`      | 0=成功 |
| `SetBytesValue(string key, byte[] value)` → `int`       | 0=成功 |
| `SetImageValue(string key, ImageData value)` → `int`    | 0=成功 |
| `SetRoiboxValue(string name, RoiboxData value)` → `int` | 0=成功 |

### 数组 Get/Set 接口

| 接口                                                                       | 备注           |
| -------------------------------------------------------------------------- | -------------- |
| `GetIntArrayValue(string name, ref int[] value, out int count)`            | count 用 `out` |
| `SetIntArrayValue(string key, int[] valueArray, int index, int len)`       | index 通常为 0 |
| `GetFloatArrayValue(string name, ref float[] value, out int count)`        | 同上           |
| `SetFloatArrayValue(string key, float[] valueArray, int index, int len)`   | 同上           |
| `GetStringArrayValue(string name, ref string[] value, out int count)`      | 同上           |
| `SetStringArrayValue(string key, string[] valueArray, int index, int len)` | 同上           |

完整遗留接口签名见 [Script.Interface.cs](../references/Script.Interface.cs)

---

## 常见陷阱

1. **非数组 VM 类型 → `Data[]` 数组**：POINT 不是 `PointData`，而是 `PointData[]`
2. **IMAGE 特殊**：IMAGE 对应 `ImageData`（不是数组），其他复合类型都是 `Data[]`
3. **变量名唯一性**：多个变量不能使用同一个名称
4. **全局变量类型**：`SetValue` 和 `GetValue` 都用 `string` 传递，需手动转换
