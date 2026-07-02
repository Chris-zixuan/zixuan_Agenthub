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


# 圆环（复用 RoiAnnulus 结构）
class Annulus:
    def __init__(self):
        self.center_x = None
        self.center_y = None
        self.inner_radius = None
        self.outer_radius = None
        self.start_angle = None
        self.angle_extend = None


# 3D点
class Point3D:
    def __init__(self):
        self.point_x = None
        self.point_y = None
        self.point_z = None


# 3D定向包围盒
class OrientBox3D:
    def __init__(self):
        self.center_x = None
        self.center_y = None
        self.center_z = None
        self.width = None
        self.length = None
        self.height = None
        self.angle_x = None
        self.angle_y = None
        self.angle_z = None


# 位姿信息
class PoseInfo:
    def __init__(self):
        self.pose_type = None
        self.pose_coor_type = None
        self.trans_tx = None
        self.trans_ty = None
        self.trans_tz = None
        self.trans_rx = None
        self.trans_ry = None
        self.trans_rz = None
        self.rot_type = None
        self.quat_rotate1 = None
        self.quat_rotate2 = None
        self.quat_rotate3 = None
        self.quat_rotate4 = None
        self.quat_tx = None
        self.quat_ty = None
        self.quat_tz = None
        self.pose_mat0 = None
        self.pose_mat1 = None
        self.pose_mat2 = None
        self.pose_mat3 = None
        self.pose_mat4 = None
        self.pose_mat5 = None
        self.pose_mat6 = None
        self.pose_mat7 = None
        self.pose_mat8 = None
        self.pose_mat9 = None
        self.pose_mat10 = None
        self.pose_mat11 = None
        self.pose_mat12 = None
        self.pose_mat13 = None
        self.pose_mat14 = None
        self.pose_mat15 = None
        self.pose_euler_string = None
        self.pose_matrix_string = None
