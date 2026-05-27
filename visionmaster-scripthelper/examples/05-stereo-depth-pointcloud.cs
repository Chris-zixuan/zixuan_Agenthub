using System;
using System.Collections.Generic;
using Script.Methods;

/// <summary>
/// 示例：激光轮廓仪深度图逐行提取点云，并按 Z 值区间过滤无效点
///
/// UserProperty.cs 预期定义：
///   IN:  STEREO_IMAGE  深度图in
///        FLOAT         zMinIn     (Z 保留下限，物理单位)
///        FLOAT         zMaxIn     (Z 保留上限，物理单位)
///   OUT: FLOAT 数组   pXOut
///        FLOAT 数组   pZOut
///        INT           ptNumOut   (每帧有效点总数)
/// </summary>
public partial class UserScript : ScriptMethods, IProcessMethods
{
    private const short InvalidDepth = -32768;
    private int processCount;

    public void Init()
    {
        processCount = 0;
    }

    /// <summary>
    /// 逐行遍历深度图，过滤无效值和超出 Z 区间的点，输出有效点云坐标
    /// </summary>
    public bool Process()
    {

        StereoImageData rangeImg = 深度图in;

        if (rangeImg.ProfileRangeImage?.Buffer == null)
        {
            ConsoleWrite("深度图数据无效");
            return false;
        }

        float zMin = zMinIn;
        float zMax = zMaxIn;

        float xScale = rangeImg.Xscale;
        float zScale = rangeImg.Zscale;
        int xOffset = rangeImg.Xoffset;
        int zOffset = rangeImg.Zoffset;

        int width = rangeImg.ProfileRangeImage.Width;
        int height = rangeImg.ProfileRangeImage.Height;

        var px = new List<float>(width * height);
        var pz = new List<float>(width * height);

        byte[] buf = rangeImg.ProfileRangeImage.Buffer;

        for (int row = 0; row < height; row++)
        {
            int rowByte = row * width * 2;
            for (int col = 0; col < width; col++)
            {
                short raw = BitConverter.ToInt16(buf, rowByte + col * 2);
                if (raw == InvalidDepth)
                    continue;

                float z = raw * zScale + zOffset;
                if (z < zMin || z > zMax)
                    continue;

                px.Add(col * xScale + xOffset);
                pz.Add(z);
            }
        }

        pXOut = px.ToArray();
        pZOut = pz.ToArray();
        ptNumOut = px.Count;

        processCount++;
        return true;
    }
}
