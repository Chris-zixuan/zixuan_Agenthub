using System;
using System.Text;
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
    /// 流程执行一次进入Process函数
    /// </summary>
    /// <returns>执行结果</returns>
    public bool Process()
    {
        // ===== 标量类型：直接赋值 =====

        // int 输入输出
        int intVal = in0;
        out0 = intVal;

        // float 输入输出
        float floatVal = in1;
        out1 = floatVal;

        // string 输入输出
        string strVal = in2;
        out2 = strVal;

        // byte[] 输入输出（十六进制数据）
        byte[] byteVal = in8;
        out8 = byteVal;

        // ===== 数组类型：直接赋值 =====

        // int 数组
        int[] intArr = in3;
        out3 = intArr;

        // float 数组
        float[] floatArr = in4;
        out4 = floatArr;

        // string 数组
        string[] strArr = in5;
        out5 = strArr;

        // ===== 复合类型：Data[] 数组直接赋值 =====

        // 图像数据
        ImageData imageData = in6;
        out6 = imageData; // 注意：ImageData 直接赋值为引用传递，如需独立副本需通过 Mat 转换

        // ROIBOX 数据
        RoiboxData[] roiData = in7;
        out7 = roiData;

        // ===== 全局变量 =====

        // 设置全局变量
        GlobalVariableModule.SetValue("var1", "323");
        // 获取全局变量
        object paramValue = GlobalVariableModule.GetValue("var1");

        // ===== 模块控制 =====

        // 获取模块结果数据
        // GetModule传入模块的名称，如果存在group中，需要加上group的名称
        // GetValue() 传入的是模块的输出参数名称
        object result = CurrentProcess.GetModule("图像源1").GetValue("Height");
        object result1 = CurrentProcess.GetModule("组合模块1.图像源1").GetValue("Height");

        // 设置模块运行参数
        // SetValue() key值为具体的参数名称
        CurrentProcess.GetModule("BLOB分析1").SetValue("FindNum", "4");
        CurrentProcess.GetModule("组合模块1.BLOB分析1").SetValue("FindNum", "4");

        // ===== 通信发送 =====

        // TCP/UDP/串口发送
        GlobalCommunicateModule.GetDevice(1).SendData("msg");

        // PLC 发送
        GlobalCommunicateModule.GetDevice(2).GetAddress(1).SendData("100", DataType.Int);

        // Modbus 发送
        GlobalCommunicateModule.GetDevice(3).GetAddress(1).SendData("100", DataType.Int);

        return true;
    }
}
