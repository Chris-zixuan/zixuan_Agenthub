using System;
using Script.Methods;

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
    /// 流程执行函数 - ROI 网格分割
    /// </summary>
    public bool Process()
    {
        int rows = 行数;
        int cols = 列数;
        RoiboxData roi = ROI;

        if (rows <= 0 || cols <= 0)
        {
            ConsoleWrite("行数和列数必须大于0");
            return false;
        }

        if (roi == null)
        {
            ConsoleWrite("输入ROI为空");
            return false;
        }

        float cellWidth = roi.Width / cols;
        float cellHeight = roi.Height / rows;
        float angle = roi.Angle;
        float rad = angle * (float)Math.PI / 180f;
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
                cell.Angle = angle;
                result[index++] = cell;
            }
        }

        ROI数组 = result;

        processCount++;
        return true;
    }


}
