using System;
using System.Text;
using System.Windows.Forms;
using Script.Methods;
public partial class UserScript : ScriptMethods, IProcessMethods
{
    //the count of process
    //执行次数计数
    int processCount;

    /// <summary>
    /// Initialize the field's value when compiling
    /// 预编译时变量初始化
    /// </summary>
    public void Init()
    {
        //You can add other global fields here
        //变量初始化，其余变量可在该函数中添加
        processCount = 0;

    }

    /// <summary>
    /// Enter the process function when running code once
    /// 流程执行一次进入Process函数
    /// </summary>
    /// <returns></returns>
    public bool Process()
    {
        //You can add your codes here, for realizing your desired function
        //每次执行将进入该函数，此处添加所需的逻辑流程处理

        //获取设置int
        int a = 0;
        GetIntValue("in0", ref a);
        SetIntValue("out0", a);

        //获取设置float
        float f = 0f;
        GetFloatValue("in1", ref f);
        SetFloatValue("out1", f);

        //获取设置string
        string s = "";
        GetStringValue("in2", ref s);
        SetStringValue("out2", s);

        //获取设置二进制数据
        byte[] by = new byte[] { };
        GetBytesValue("in8", ref by);
        SetBytesValue("out8", by);

        int count = 0;
        //获取设置int数组
        int[] narry = new int[3];
        GetIntArrayValue("in3", ref narry, out count);
        SetIntArrayValue("out3", narry, 0, narry.Length);

        //获取设置float数组
        float[] farry = new float[3];
        GetFloatArrayValue("in4", ref farry, out count);
        SetFloatArrayValue("out4", farry, 0, farry.Length);

        //获取设置strig数组
        string[] sarry = new string[3];
        GetStringArrayValue("in5", ref sarry, out count);
        SetStringArrayValue("out5", sarry, 0, sarry.Length);

        //设置/获取16进制数据
        byte[] tempBytes = new byte[] { };
        GetBytesValue("in1", ref tempBytes);
        SetBytesValue("out1", new byte[] { 0x00, 0x02 });

        //设置/获取图像数据
        ImageData imagedata = new ImageData();
        GetImageValue("in6", ref imagedata);
        SetImageValue("out6", imagedata);

        //设置/获取ROIBOX数据
        RoiboxData roidata = new RoiboxData();
        GetRoiboxValue("in7", ref roidata);
        SetRoiboxValue("out7", roidata);

        //设置全局变量
        GlobalVariableModule.SetValue("var1", "323");
        //2.获取全局变量
        object paramValue = GlobalVariableModule.GetValue("var1");

        //获取模块结果数据
        //GetModule传入模块的名称，如果存在group中，需要加上group的名称
        //GetValue() 传入的是模块的输出参数名称
        object result = CurrentProcess.GetModule("图像源1").GetValue("Height");
        object result1 = CurrentProcess.GetModule("组合模块1.图像源1").GetValue("Height");

        //设置模块运行参数
        //如果该模块在group内部，需要加上group模块的参数名称
        //SetValue(),key值为具体的参数名称，
        CurrentProcess.GetModule("BLOB分析1").SetValue("FindNum", "4");
        CurrentProcess.GetModule("组合模块1.BLOB分析1").SetValue("FindNum", "4");

        //5.通信发送数据
        //GetDevice(int index), index为通信设备的ID
        //tcp,udp,串口发送数据调用函数
        GlobalCommunicateModule.GetDevice(1).SendData("msg", DataType.StringType);

        //plc设备发送数据
        //GetAddress(int index),index为address的ID
        GlobalCommunicateModule.GetDevice(2).GetAddress(1).SendData("100", DataType.IntType);
        GlobalCommunicateModule.GetDevice(2).GetAddress(1).SendData("100", DataType.StringType);
        GlobalCommunicateModule.GetDevice(2).GetAddress(1).SendData("100", DataType.FloatType);

        //modbus发送设备数据
        GlobalCommunicateModule.GetDevice(3).GetAddress(1).SendData("100", DataType.IntType);
        GlobalCommunicateModule.GetDevice(3).GetAddress(1).SendData("100", DataType.StringType);
        GlobalCommunicateModule.GetDevice(3).GetAddress(1).SendData("100", DataType.FloatType);

        return true;
    }
}