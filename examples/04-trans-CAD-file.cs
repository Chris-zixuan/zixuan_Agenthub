using System;
using Script.Methods;
using CadParser;

/// <summary>
/// VisionMaster CAD 文件转换脚本示例 - DXF 文件解析与渲染
/// </summary>
public partial class UserScript : ScriptMethods, IProcessMethods
{
    int processCount;

    /// <summary>
    /// 预编译时变量初始化
    /// </summary>
    public void Init()
    {
        processCount = 0;
    }

    /// <summary>
    /// 流程执行函数 - 加载 DXF 文件并渲染为图像输出
    /// </summary>
    public bool Process()
    {
        // 直接赋值获取输入参数
        string filePath = 文件路径;
        double scale = 缩放比例;
        double bitmapScale = 渲染比例;

        if (string.IsNullOrEmpty(filePath))
        {
            ConsoleWrite("文件路径为空");
            return false;
        }

        // 加载 DXF 文件
        CadDocument doc = CadDocument.Load(filePath);
        if (doc == null)
        {
            ConsoleWrite("加载 DXF 文件失败：" + filePath);
            return false;
        }

        // 解析实体
        doc.Parse();

        // 应用坐标缩放
        doc.ApplyScale(scale);

        // 渲染为位图
        var bitmap = doc.Render(bitmapScale: bitmapScale);

        // 输出图像（将 Bitmap 转为 ImageData 由外部模块处理）
        输出图像路径 = filePath.Replace(".dxf", ".png");
        bitmap.Save(输出图像路径, System.Drawing.Imaging.ImageFormat.Png);

        // 释放临时资源
        bitmap.Dispose();
        doc.Dispose();

        processCount++;
        return true;
    }
}
