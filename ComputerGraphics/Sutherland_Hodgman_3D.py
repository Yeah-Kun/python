"""
    实现Sutherland–Hodgman算法 3D版本
    四个规则：
        1. 如果点p1和点p2都在边界线内侧，则记录点p2
        2. 如果点p1在内侧，而p2在外侧，则记录交点i
        3. 如果点p1在外侧，而p2在内侧，则记录交点i和点p2
        4. 如果点p1和点p2都在边界线外侧，则不记录

    流程：
        1. 将多边形拆解成多条线段
        2. 按照4个判断规则判断，将每一条线段的结果写进列表
        3. 在N个边界线重复流程2，直到最后一条边界线结束
        4. 输出最后一个列表

    注意：最后输出的值可能会出现两个相同或非常相近的值，需要进一步处理
"""

import numpy as np


def clip_ploygon(ploygon, v1, v2, v3):
    """
        参数：
            ploygon：多边形
            v1、v2、v3：平面的三个顶点

        返回：
            after_clip_ploygon：列表, 经过裁剪的多边形
    """
    def calc_position(p, v1, v_n):
        """
            判断点p是否在平面的内侧

            返回：
                真：表示在内侧
                假：不在内侧
        """
        v = p - v1
        if np.dot(v_n, v) >= 0:
            return True
        else:
            return False

    def calc_plane_line_intersection(p1, p2, v_n, v1):
        """
            求平面方程 与 直线的交点

            原理：https://blog.csdn.net/qq_38906523/article/details/78849691

            返回：
                交点：(x,y,z)
        """
        v_line = p2 - p1

        v_pp_lp = v1 - p1

        deno = np.dot(v_n, v_line)
        if deno != 0:
            t = np.dot(v_n, v_pp_lp) / deno
            return p1 + v_line * t
        else:
            print("存在错误: p1:", p1, " p2:", p2, " v_n:", v_n, " v1:", v1)
            return np.array((0, 0, 0))

    # 初始化clip_ploygon
    clip_ploygon = []

    # 获得平面两垂直的向量
    v_first = v2 - v1
    v_second = v3 - v1

    # 法向量
    v_n = np.cross(v_first, v_second)

    p1 = ploygon[-1]
    print("ploygon:", ploygon)
    for p2 in ploygon:
        # 判断状态
        p1_position = calc_position(p1, v1, v_n)
        p2_position = calc_position(p2, v1, v_n)

        # print("p1_position:" , p1_position, "p2_position: ", p2_position)
        # 根据规则处理
        if p1_position and p2_position:
            clip_ploygon.append(p2)
        elif p1_position and not p2_position:
            intersection_point = calc_plane_line_intersection(p1, p2, v_n, v1)
            clip_ploygon.append(intersection_point)
        elif not p1_position and p2_position:
            intersection_point = calc_plane_line_intersection(p1, p2, v_n, v1)
            clip_ploygon.append(intersection_point)
            clip_ploygon.append(p2)
        else:
            pass

        p1 = p2

    return clip_ploygon


def boundary_clip(w, ploygon):
    """
        围绕边界盒裁剪多边形

        注意：根据右手定则，需要非常注意传入点的顺序，否则向量会是错的
            如需回忆，建议先按照列表p画出边界盒


        return:
            after_clip_ploygon：经过裁剪的多边形
    """
    # 初始化
    after_clip_ploygon = ploygon
    p = [np.array((-w, w, w)),
         np.array((w, w, w)),
         np.array((w, -w, w)),
         np.array((-w, -w, w)),

         np.array((-w, w, 0)),
         np.array((w, w, 0)),
         np.array((w, -w, 0)),
         np.array((-w, -w, 0)),
        ]

    # 前
    after_clip_ploygon = clip_ploygon(after_clip_ploygon, p[3], p[0], p[2])

    # 后
    after_clip_ploygon = clip_ploygon(after_clip_ploygon, p[6], p[5], p[7])

    # 左
    after_clip_ploygon = clip_ploygon(after_clip_ploygon, p[7], p[4], p[3])

    # 右
    after_clip_ploygon = clip_ploygon(after_clip_ploygon, p[2], p[1], p[6])

    # 上
    after_clip_ploygon = clip_ploygon(after_clip_ploygon, p[1], p[0], p[5])

    # 下
    after_clip_ploygon = clip_ploygon(after_clip_ploygon, p[3], p[2], p[7])

    return after_clip_ploygon


def main():
    # 构造数据
    w = 100
    triangle = [np.array([0, 150, 50]), np.array(
        [150, 50, 50]), np.array([-150, 50, 50])]
    triangle2 = [np.array([0, 0, 0]), np.array(
        [150, 50, 50]), np.array([-150, 50, 50])]
    clip_ploygon = boundary_clip(w, triangle2)
    print("clip_ploygon:", len(clip_ploygon), clip_ploygon)

    return clip_ploygon


def test_calc_plane_line_intersection():
    def calc_plane_line_intersection(p1, p2, v_n, v1):
        """
            求平面方程 与 直线的交点

            原理：https://blog.csdn.net/qq_38906523/article/details/78849691

            返回：
                交点：(x,y,z)
        """
        v_line = p2 - p1

        v_pp_lp = v1 - p1

        deno = np.dot(v_n, v_line)
        if deno != 0:
            t = np.dot(v_n, v_pp_lp) / deno
            return p1 + v_line * t
        else:
            print("存在错误: p1:", p1, " p2:", p2, " v_n:", v_n, " v1:", v1)
            return np.array((0, 0, 0))

    w = 1
    p = [np.array((-w, w, w)),
         np.array((w, w, w)),
         np.array((w, -w, w)),
         np.array((-w, -w, w)),

         np.array((-w, w, 0)),
         np.array((w, w, 0)),
         np.array((w, -w, 0)),
         np.array((-w, -w, 0)),
        ]
    p1 = np.array((-w - 50, 0, 0))
    p2 = np.array((w + 50, 0, 0))

    v_n = np.cross((p[3] - p[0]), (p[4] - p[0]))
    point = calc_plane_line_intersection(p1, p2, v_n, p[0])
    print(point)


if __name__ == '__main__':
    clip_ploygon = main()