/// <summary>
/// VisionMaster 图像处理脚本示例 - Canny 边缘检测
/// 使用 OpenCvSharp 库进行图像处理
/// </summary>
using System;
using System.Runtime.InteropServices;
using Script.Methods;
using OpenCvSharp;

public partial class UserScript : UserScript, IProcessMethods
{
    // 全局字段
    private Mat processingMat;
    private Mat edgeMat;
    
    /// <summary>
    /// 初始化函数
    /// </summary>
    public void Init()
    {
        // 预分配 Mat 对象，避免重复创建
        // 假设最大处理 1920x1080 的图像
        processingMat = new Mat();
        edgeMat = new Mat();
        
        Console.WriteLine("Canny 边缘检测脚本初始化完成");
    }
    
    /// <summary>
    /// 流程执行函数
    /// </summary>
    public bool Process()
    {
        try
        {
            // ========== 1. 获取输入参数 ==========
            
            // 获取阈值参数
            int threshold1 = 100;
            int threshold2 = 200;
            GetIntValue("threshold1", ref threshold1);
            GetIntValue("threshold2", ref threshold2);
            
            // 获取输入图像
            ImageData imgIn = new ImageData();
            GetIMAGEValue("input_image", ref imgIn);
            
            if (imgIn.Buffer == null || imgIn.Width <= 0 || imgIn.Height <= 0)
            {
                ShowMessageBox("输入图像无效");
                return false;
            }
            
            // ========== 2. 转换为 OpenCvSharp Mat ==========
            
            // 根据像素格式创建 Mat
            Mat srcImage = new Mat();
            
            if (imgIn.PixelFormat == ImagePixelFormate.RGB24)
            {
                // RGB24 格式
                srcImage = new Mat(imgIn.Height, imgIn.Width, MatType.CV_8UC3, imgIn.Buffer);
            }
            else if (imgIn.PixelFormat == ImagePixelFormate.MONO8)
            {
                // MONO8 格式
                srcImage = new Mat(imgIn.Height, imgIn.Width, MatType.CV_8UC1, imgIn.Buffer);
                
                // 如果是单通道，转换为三通道便于处理
                Cv2.CvtColor(srcImage, srcImage, ColorConversionCodes.GRAY2BGR);
            }
            
            // ========== 3. Canny 边缘检测 ==========
            
            // 转换为灰度图
            Mat grayMat = new Mat();
            Cv2.CvtColor(srcImage, grayMat, ColorConversionCodes.BGR2GRAY);
            
            // 执行 Canny 边缘检测
            Cv2.Canny(grayMat, edgeMat, threshold1, threshold2);
            
            // ========== 4. 可选：绘制轮廓 ==========
            
            // 查找轮廓
            Point[][] contours = new Point[0][];
            HierarchyIndex[] hierarchy = new HierarchyIndex[0];
            Cv2.FindContours(edgeMat, out contours, out hierarchy, 
                RetrievalModes.External, ContourApproximationModes.APPROX_SIMPLE);
            
            // 在原图上绘制轮廓
            Mat resultImage = srcImage.Clone();
            Cv2.DrawContours(resultImage, contours, -1, new Scalar(0, 255, 0), 2);
            
            // ========== 5. 输出结果 ==========
            
            // 输出边缘图像
            byte[] edgeBuffer = new byte[edgeMat.Rows * edgeMat.Cols];
            edgeMat.GetArray(0, 0, edgeBuffer);
            
            ImageData imgOutEdge = new ImageData
            {
                Buffer = edgeBuffer,
                Width = edgeMat.Cols,
                Height = edgeMat.Rows,
                PixelFormat = ImagePixelFormate.MONO8
            };
            SetImageValue("edge_image", imgOutEdge);
            
            // 输出绘制轮廓的结果图像
            byte[] resultBuffer = new byte[resultImage.Rows * resultImage.Cols * 3];
            resultImage.GetArray(0, 0, resultBuffer);
            
            ImageData imgOutResult = new ImageData
            {
                Buffer = resultBuffer,
                Width = resultImage.Cols,
                Height = resultImage.Rows,
                PixelFormat = ImagePixelFormate.RGB24
            };
            SetImageValue("result_image", imgOutResult);
            
            // 输出检测到的轮廓数量
            SetIntValue("contour_count", contours.Length);
            
            // ========== 6. 清理临时资源 ==========
            
            grayMat.Dispose();
            resultImage.Dispose();
            srcImage.Dispose();
            
            return true;
        }
        catch (Exception ex)
        {
            ShowMessageBox($"Canny 边缘检测失败：{ex.Message}\n{ex.StackTrace}");
            return false;
        }
    }
    
    /// <summary>
    /// 资源释放函数
    /// </summary>
    public virtual void Dispose()
    {
        // 释放 Mat 对象
        processingMat?.Dispose();
        edgeMat?.Dispose();
        
        Console.WriteLine("Canny 边缘检测脚本资源已释放");
    }
}
