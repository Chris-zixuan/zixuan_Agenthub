# coding: utf-8
import sys
from ioHelper import *


def Process(data) -> int:

    moduleVar = IoHelper(data, INIT_MODULE_VAR)
    globalVar = IoHelper(data, INIT_GLOBAL_VAR)
    localVar = IoHelper(data, INIT_LOCAL_VAR)
    

    try:
        #创建空列表
        matchPointX = []
        matchPointY = []
        #输入变量赋值到列表
        matchPointX = moduleVar.in0
        matchPointY = moduleVar.in1
        #组装为字典
        matchDict = dict(zip(matchPointX,matchPointY))
        matchPointX.clear()
        matchPointY.clear()
        #按字典键（X坐标）值进行排序
        sortedList = sorted(matchDict.items())
        PrintMsg(str(sortedList))
        for item in sortedList:
            #字典拆分
            matchPointX.append(item[0])
            matchPointY.append(item[1])
        #赋值到输出变量
        moduleVar.out0 = matchPointX
        moduleVar.out1 = matchPointY
    except BaseException as e:
        PrintMsg(e)
    return 0