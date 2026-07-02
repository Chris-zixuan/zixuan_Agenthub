# coding: utf-8
import sys
from ShellOperate import *
import ctypes
import gc

OutputDebugString = ctypes.windll.kernel32.OutputDebugStringW

_sop = ShOperate()

# 是否打印调试信息
debug_print = False

# 初始化（必须调用）
def InitValue(data):
    return _sop.InitValue(data)


# 一些常量定义
INT_MAX = 2147483647
INT_MIN = -2147483647 - 1

FLT_MAX = 3.402823466e38
FLT_MIN = -3.402823466e38

INIT_MODULE_VAR = 0
INIT_GLOBAL_VAR = 1
INIT_LOCAL_VAR  = 2

# 内部打印调试信息接口
def DebugMsg(data):
    if debug_print:
        print(str(data) + '\r\n')
        OutputDebugString(str(data) + '\r\n')


# 用户打印调试信息接口，到编辑代码的界面上
def PrintMsg(msg: str):
    return _sop.PrintMsg(msg)
    


# 算法平台变量类型到Python变量类型的映射
dict_type = {'int': "int", 
             'int[]': "int",
             'float': "float", 
             'float[]': "float",
             'string': "str",
             'string[]': "str", 
             'byte': "bytes",
             'IMAGE': "ImageData",
             'ROIBOX': "RoiBox",
             'ROIANNULUS': "RoiAnnulus",
             'ROIPOLYGON': "RoiPolygon",
             'POINT': "Point",
             'LINE': "Line", 
             'FIXTURE':"Fixture",
             'CIRCLE': "Circle",
             'ANNULUS': "RoiAnnulus",
             'Rect': "Rect",
             'ELLIPSE': "ELLIPSE", 
             'pointset': "PointSet"}

# 检查变量类型是否为期望的类型
def checkVarType(vars, expect_type) -> bool:
    if isinstance(vars, list):
        for item in vars:
            if False == isinstance(item, expect_type):
                return False
        return True
    else:
        if isinstance(vars, expect_type):
            return True
    return False


# 检查变量值是否有效
def CheckVarValid(vars) -> bool:
    if isinstance(vars, list):
        for item in vars:
            if isinstance(item, int):
                if item > INT_MAX or item < INT_MIN:
                    return False
            elif isinstance(item, float):
                if item > FLT_MAX or item < FLT_MIN:
                    return False
        return True
    elif isinstance(vars, int):
        if vars > INT_MAX or vars < INT_MIN:
            return False
    elif isinstance(vars, float):
        if vars > FLT_MAX or vars < FLT_MIN:
            return False
    return True


# 变量管理类：管理模块输入、输出参数，全局变量，局部变量
class IoHelper:
    def __init__(self, data, init_type):
        """用户代码中 IoHelper 对象会在Process开始时创建, 此时会自动调用__init__函数, 创建输入变量并从脚本模块获取初始值"""
        InitValue(data)
        DebugMsg(data)
        if init_type == INIT_MODULE_VAR:
            self.__inVar = data[4]      # 当前模块的输入变量
            self.__outVar = data[5]     # 当前模块的输出变量
            self.__globalVar = {}
            self.__localVar = {}
            self.__init_type = 'moduleVar'
        elif init_type == INIT_GLOBAL_VAR:
            self.__inVar = {}
            self.__outVar = {}
            self.__globalVar = data[6]  # 全局变量
            self.__localVar = {}
            self.__init_type = 'globalVar'
        elif init_type == INIT_LOCAL_VAR:
            self.__inVar = {}
            self.__outVar = {}
            self.__globalVar = {}
            self.__localVar = data[7]   # 当前模块所属容器的局部变量
            self.__init_type = 'localVar'
        self.initVar()

    def __del__(self):
        """用户代码中 IoHelper 对象会在Process结束后销毁, 此时会自动调用__del__函数, 将输出变量的值回传给脚本模块"""
        self.updateVar()
        self.clearVar()

    # Python脚本初始化 全局变量 或者 局部变量
    def initGLVar(self, varList):
        expr = """"""
        for key in varList:
            varName = key.strip("%")
            var_name = f"{varName}"
            var_type = varList[key]["type"]
            module_id = varList[key]["module_id"]
            if var_type == "int" or var_type == "int[]" or var_type == "float" or var_type == "float[]" or var_type == "string" or var_type == "string[]" or var_type == "byte":
                expr += f"""
self.{var_name} = _sop.GetGlobalSimpleVar({module_id}, \"{var_name}\")"""
            elif var_type == "pointset":
                expr += f"""
self.{var_name} = PointSet()
_sop.GetGlobalPointSet({module_id}, \"{var_name}\", self.{var_name})"""
            elif var_type == "IMAGE":
                expr += f"""
self.{var_name} = ImageData()
_sop.GetGlobalImageData({module_id}, \"{var_name}\", self.{var_name})"""
            elif var_type == "ROIBOX":
                expr += f"""
self.{var_name} = RoiBox()
_sop.GetGlobalRoiBox({module_id}, \"{var_name}\",  self.{var_name})"""
            elif var_type == "CIRCLE":
                expr += f"""
self.{var_name} = Circle()
_sop.GetGlobalCircle({module_id}, \"{var_name}\",  self.{var_name})"""
            elif var_type == "POINT":
                expr += f"""
self.{var_name} = Point()
_sop.GetGlobalPoint({module_id}, \"{var_name}\", self.{var_name})"""
            elif var_type == "LINE":
                expr += f"""
self.{var_name} = Line()
_sop.GetGlobalLine({module_id}, \"{var_name}\",  self.{var_name})"""
            elif var_type == "ROIANNULUS":
                expr += f"""
self.{var_name} = RoiAnnulus()
_sop.GetGlobalRoiAnnulus({module_id}, \"{var_name}\",  self.{var_name})"""
            elif var_type == "Rect":
                expr += f"""
self.{var_name} = Rect()
_sop.GetGlobalRect({module_id}, \"{var_name}\",  self.{var_name})"""
            elif var_type == "ELLIPSE":
                expr += f"""
self.{var_name} = ELLIPSE()
_sop.GetGlobalEllipse({module_id}, \"{var_name}\",  self.{var_name})"""
            elif var_type == "ROIPOLYGON":
                expr += f"""
self.{var_name} = RoiPolygon()
_sop.GetGlobalRoiPolygon({module_id}, \"{var_name}\",  self.{var_name})"""
            elif var_type == "FIXTURE":
                expr += f"""
self.{var_name} = Fixture()
_sop.GetGlobalFixture({module_id}, \"{var_name}\",  self.{var_name})"""
        return expr

    # 返回全局变量 或者 局部变量 到主程序中
    def updateGLVar(self, varList):
        expr = """"""
        for key in varList:
            varName = key.strip("%")
            var_name = f"{varName}"
            var_type = varList[key]["type"]
            var_type_name = dict_type[var_type]
            module_id = varList[key]["module_id"]
            if var_type == "int" or var_type == "int[]" or var_type == "float" or var_type == "float[]" or var_type == "string" or var_type == "string[]" or var_type == "byte":
                expr += f"""
if not self.{var_name} is None:
    if (checkVarType(self.{var_name}, {var_type_name})):
        if (CheckVarValid(self.{var_name})):
            if (isinstance(self.{var_name}, list)):
                _sop.SetGlobalSimpleVar({module_id}, \"{var_name}\", self.{var_name})
            else:
                tmp = [self.{var_name}]
                _sop.SetGlobalSimpleVar({module_id}, \"{var_name}\", tmp)
        else:
            _sop.PrintMsg('global variable \"{var_name}\" contains invalid value')
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"int\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "IMAGE":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalImageData({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"ImageData\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "ROIBOX":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalRoiBox({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"RoiBox\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "ROIANNULUS":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalRoiAnnulus({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"RoiAnnulus\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "ROIPOLYGON":
                 expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalRoiPolygon({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"RoiPolygon\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "POINT":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalPoint({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"Point\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "LINE":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalLine({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"Line\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "FIXTURE":
                 expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalFixture({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"Fixture\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "CIRCLE":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalCircle({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"Circle\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "ANNULUS":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalRoiAnnulus({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"Annulus\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "Rect":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalRect({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"Rect\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "ELLIPSE":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalEllipse({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"ELLIPSE\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "pointset":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetGlobalPointSet({module_id}, \"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('global variable \"{var_name}\" contains invalid type, should be \"pointset\"')
else:
    DebugMsg(\"{var_name} is None\")"""
        return expr
        
        
    # 从C++初始化变量
    def initVar(self):
        DebugMsg(self.__init_type + '--->init')
        """创建输入、输出变量、全局变量"""
        expr = """"""
# 输入变量
        for key in self.__inVar:
            varName = key.strip("%")
            var_name = f"{varName}"
            var_type = self.__inVar[key]["type"]
            var_value = self.__inVar[key]["value"].split('\r')

            if var_type == "int" or var_type == "int[]":
                expr += f"""
self.{var_name} = _sop.GetIntArrayValue(\"{var_name}\")"""
            elif var_type == "float" or var_type == "float[]":
                expr += f"""
self.{var_name} = _sop.GetFloatArrayValue(\"{var_name}\")"""
            elif var_type == "string" or var_type == "string[]":
                expr += f"""
self.{var_name} = _sop.GetStringArrayValue(\"{var_name}\")"""
            elif var_type == "IMAGE":
                expr += f"""
self.{var_name} = ImageData()
_sop.GetImageDataValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "byte":
                expr += f"""
self.{var_name} = _sop.GetByteValue(\"{var_name}\")"""
            elif var_type == "ROIBOX":
                expr += f"""
self.{var_name} = RoiBox()
_sop.GetRoiBoxValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "ROIANNULUS":
                expr += f"""
self.{var_name} = RoiAnnulus()
_sop.GetRoiAnnulusValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "ROIPOLYGON":
                expr += f"""
self.{var_name} = RoiPolygon()
_sop.GetRoiPolygonValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "POINT":
                expr += f"""
self.{var_name} = Point()
_sop.GetPointValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "LINE":
                expr += f"""
self.{var_name} = Line()
_sop.GetLineValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "FIXTURE":
                expr += f"""
self.{var_name} = Fixture()
_sop.GetFixtureValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "CIRCLE":
                expr += f"""
self.{var_name} = Circle()
_sop.GetCircleValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "ANNULUS":
                expr += f"""
self.{var_name} = RoiAnnulus()
_sop.GetRoiAnnulusValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "Rect":
                expr += f"""
self.{var_name} = Rect()
_sop.GetRectValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "ELLIPSE":
                expr += f"""
self.{var_name} = ELLIPSE()
_sop.GetEllipseValue(\"{var_name}\", {var_value}, self.{var_name})"""
            elif var_type == "pointset":
                expr += f"""
self.{var_name} = PointSet()
_sop.GetPointSetValue(\"{var_name}\", self.{var_name})"""

# 输出变量
        for key in self.__outVar: 
            varName = key.strip("%")
            var_name = f"{varName}"
            expr += f"""
self.{var_name} = None"""

# 全局变量
        #expr += self.initGLVar(self.__globalVar)

# 局部变量
        #expr += self.initGLVar(self.__localVar)

        DebugMsg(expr)
        exec(expr)
        DebugMsg(self.__init_type + '--->init end')

    # 返回变量到C++
    def updateVar(self):
        DebugMsg(self.__init_type + '--->update')
        """将输出变量、全局变量的值传回脚本模块"""
        expr = """"""
        for key in self.__outVar:  # 输出变量
            varName = key.strip("%")
            var_name = f"{varName}"
            var_type = self.__outVar[key]["type"]
            var_type_name = dict_type[var_type]
            var_value = self.__outVar[key]["value"].split('\r')
            DebugMsg(var_name)
            if var_type == "int" or var_type == "int[]":
                expr += f"""
if not self.{var_name} is None:
    if (checkVarType(self.{var_name}, {var_type_name})):
        if (CheckVarValid(self.{var_name})):
            if (isinstance(self.{var_name}, list)):
                _sop.SetIntArrayValue(\"{var_name}\", self.{var_name})
            else:
                tmp = [self.{var_name}]
                _sop.SetIntArrayValue(\"{var_name}\", tmp)
        else:
            _sop.PrintMsg('output variable \"{var_name}\" contains invalid value')
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"int\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "float" or var_type == "float[]":
                expr += f"""
if not self.{var_name} is None:
    if (checkVarType(self.{var_name}, {var_type_name})):
        if (CheckVarValid(self.{var_name})):
            if (isinstance(self.{var_name}, list)):
                _sop.SetFloatArrayValue(\"{var_name}\", self.{var_name})
            else:
                tmp = [self.{var_name}]
                _sop.SetFloatArrayValue(\"{var_name}\", tmp)
        else:
            _sop.PrintMsg('output variable \"{var_name}\" contains invalid value')
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"float\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "string" or var_type == "string[]":
                expr += f"""
if not self.{var_name} is None:
    if (checkVarType(self.{var_name}, {var_type_name})):
        if (isinstance(self.{var_name}, list)):
            _sop.SetStringArrayValue(\"{var_name}\", self.{var_name})
        else:
            tmp = [self.{var_name}]
            _sop.SetStringArrayValue(\"{var_name}\", tmp)
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"string\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "IMAGE":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetImageDataValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"ImageData\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "byte":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetByteValue(\"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"bytes\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "ROIBOX":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetRoiBoxValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"RoiBox\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "ROIANNULUS":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetRoiAnnulusValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"RoiAnnulus\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "ROIPOLYGON":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetRoiPolygonValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"RoiPolygon\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "POINT":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetPointValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"Point\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "LINE":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetLineValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"Line\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "FIXTURE":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetFixtureValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"Fixture\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "CIRCLE":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetCircleValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"Circle\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "ANNULUS":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetRoiAnnulusValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"RoiAnnulus\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "Rect":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetRectValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"Rect\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "ELLIPSE":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetEllipseValue(\"{var_name}\", {var_value}, self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"ELLIPSE\"')
else:
    DebugMsg(\"{var_name} is None\")"""
            elif var_type == "pointset":
                expr += f"""
if not self.{var_name} is None:
    if (isinstance(self.{var_name}, {var_type_name})):
        _sop.SetPointSetValue(\"{var_name}\", self.{var_name})
    else:
        _sop.PrintMsg('output variable \"{var_name}\" contains invalid type, should be \"pointset\"')
else:
    DebugMsg(\"{var_name} is None\")"""

        # 全局变量
        #expr += self.updateGLVar(self.__globalVar)


        # 局部变量
        #expr += self.updateGLVar(self.__localVar)


        DebugMsg(expr)
        exec(expr)
        DebugMsg(self.__init_type + '--->update end')

    # 释放变量资源
    def clearVar(self):
        DebugMsg(self.__init_type + '--->clear')
        """销毁输入、输出变量、全局变量"""
        expr = """"""
        for key in self.__inVar:  # 输入变量
            varName = key.strip("%")
            var_name = f"{varName}"
            expr += f"""
del self.{var_name}"""

        for key in self.__outVar:  # 输出变量
            varName = key.strip("%")
            var_name = f"{varName}"
            expr += f"""
del self.{var_name}"""

#        for key in self.__globalVar:  # 全局变量
#            varName = key.strip("%")
#            var_name = f"{varName}"
#            expr += f"""
#del self.{var_name}"""

#        for key in self.__localVar:  # 局部变量
#            varName = key.strip("%")
#            var_name = f"{varName}"
#            expr += f"""
#del self.{var_name}"""

        DebugMsg(expr)
        exec(expr)
        DebugMsg(self.__init_type + '--->clear end')
        gc.collect()

    # 根据全局变量/局部变量的 变量名 获取变量的字段信息
    def getGLVar(self, keyName:str):
        if self.__init_type == 'globalVar':
            for key in self.__globalVar:
                if keyName == key.strip("%"):
                    return self.__globalVar[key]
        else:
            for key in self.__localVar:
                if keyName == key.strip("%"):
                    return self.__localVar[key]
        return None
                    
        
    # 根据全局变量/局部变量的 变量名 获取变量值
    def GetValue(self, keyName:str):
        # 获取变量的其他信息（类型，模块ID）
        varInfo = self.getGLVar(keyName)
        if varInfo == None:
            return None
        varType = varInfo["type"]
        moduleId = int(varInfo["module_id"])
        temp = None
        if varType == "int" or varType == "int[]" or varType == "float" or varType == "float[]" or varType == "string" or varType == "string[]" or varType == "byte":
            temp = _sop.GetGlobalSimpleVar(moduleId, keyName)
        elif varType == "pointset":
            temp = PointSet()
            _sop.GetGlobalPointSet(moduleId, keyName, temp)
        elif varType == "IMAGE":
            temp = ImageData()
            _sop.GetGlobalImageData(moduleId, keyName, temp)
        elif varType == "ROIBOX":
            temp = RoiBox()
            _sop.GetGlobalRoiBox(moduleId, keyName, temp)
        elif varType == "CIRCLE":
            temp = Circle()
            _sop.GetGlobalCircle(moduleId, keyName, temp)
        elif varType == "POINT":
            temp = Point()
            _sop.GetGlobalPoint(moduleId, keyName, temp)
        elif varType == "LINE":
            temp = Line()
            _sop.GetGlobalLine(moduleId, keyName, temp)
        elif varType == "ROIANNULUS":
            temp = RoiAnnulus()
            _sop.GetGlobalRoiAnnulus(moduleId, keyName, temp)
        elif varType == "Rect":
            temp = Rect()
            _sop.GetGlobalRect(moduleId, keyName, temp)
        elif varType == "ELLIPSE":
            temp = ELLIPSE()
            _sop.GetGlobalEllipse(moduleId, keyName, temp)
        elif varType == "ROIPOLYGON":
            temp = RoiPolygon()
            _sop.GetGlobalRoiPolygon(moduleId, keyName, temp)
        elif varType == "FIXTURE":
            temp = Fixture()
            _sop.GetGlobalFixture(moduleId, keyName, temp)
        
        return temp
            
        
    # 根据全局变量/局部变量的 变量名 设置变量值
    def SetValue(self, keyName:str, varValue):
        # 获取变量的其他信息（类型，模块ID）
        varInfo = self.getGLVar(keyName)
        if varInfo == None:
            return None
        varType = varInfo["type"] # string
        varTypeName = eval(dict_type[varType]) # string to type
        moduleId = int(varInfo["module_id"])
        if varType == "int" or varType == "int[]" or varType == "float" or varType == "float[]" or varType == "string" or varType == "string[]" or varType == "byte":
            if not varValue is None:
                if (checkVarType(varValue, varTypeName)):
                    if (CheckVarValid(varValue)):
                        if (isinstance(varValue, list)):
                            _sop.SetGlobalSimpleVar(moduleId, keyName, varValue)
                        else:
                            tmp = [varValue]
                            _sop.SetGlobalSimpleVar(moduleId, keyName, tmp)
                    else:
                        _sop.PrintMsg('global variable ' + keyName + ' contains invalid value')
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"int\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "IMAGE":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalImageData(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"ImageData\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "ROIBOX":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalRoiBox(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"RoiBox\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "ROIANNULUS":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalRoiAnnulus(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"RoiAnnulus\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "ROIPOLYGON":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalRoiPolygon(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"RoiPolygon\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "POINT":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalPoint(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"Point\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "LINE":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalLine(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"Line\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "FIXTURE":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalFixture(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"Fixture\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "CIRCLE":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalCircle(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"Circle\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "ANNULUS":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalRoiAnnulus(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"Annulus\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "Rect":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalRect(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"Rect\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "ELLIPSE":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalEllipse(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"ELLIPSE\"')
            else:
                DebugMsg(keyName + " is None")
        elif varType == "pointset":
            if not varValue is None:
                if (isinstance(varValue, varTypeName)):
                    _sop.SetGlobalPointSet(moduleId, keyName, varValue)
                else:
                    _sop.PrintMsg('global variable ' + keyName + ' contains invalid type, should be \"pointset\"')
            else:
                DebugMsg(keyName + " is None")