
# ROI圆环
class RoiAnnulus:
    def __init__(self):
        self.center_x = None
        self.center_y = None
        self.inner_radius = None
        self.outer_radius = None
        self.start_angle = None
        self.angle_extend = None


# 圆
class Circle:
    def __init__(self):
        self.radius = None
        self.center_x = None
        self.center_y = None

# 椭圆
class ELLIPSE:
    def __init__(self):
        self.center_x = None
        self.center_y = None
        self.major_radius = None
        self.minor_radius = None
        self.angle = None

# 位置修正信息
class Fixture:
    def __init__(self):
        self.init_point_x = None
        self.init_point_y = None
        self.init_angle = None
        self.init_scale_x = None
        self.init_scale_y = None
        self.run_point_x = None
        self.run_point_y = None
        self.run_angle = None
        self.run_scale_x = None
        self.run_scale_y = None

# 图像数据
class ImageData:
    def __init__(self):
        self.width = None
        self.height = None
        self.pixel_format = None
        self.buffer = None
        self.dataLen = None

# 直线
class Line:
    def __init__(self):
        self.start_point_x = None
        self.start_point_y = None
        self.end_point_x = None
        self.end_point_y = None

# 点
class Point:
    def __init__(self):
        self.point_x = None
        self.point_y = None

# 轮廓
class PointSet:
    def __init__(self):
        self.buffer = None
        self.dataLen = None

# 矩形
class Rect:
    def __init__(self):
        self.rect_x = None
        self.rect_y = None
        self.width = None
        self.height = None

# Box
class RoiBox:
    def __init__(self):
        self.center_x = None
        self.center_y = None
        self.width = None
        self.height = None
        self.angle = None

# 多边形
class RoiPolygon:
    def __init__(self):
        self.point_num = None
        self.point_x = None
        self.point_y = None

# 圆环
class Annulus:
    def __init__(self):
        self.center_x = None
        self.center_y = None
        self.inner_radius = None
        self.outer_radius = None
        self.start_angle = None
        self.angle_extend = None