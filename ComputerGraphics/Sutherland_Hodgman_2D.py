"""
    实现Sutherland–Hodgman算法
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
"""


def calc_intersection_point(b1, b2, p1, p2):
    """
            计算两条直线的交点

            输入：
                    b1、b2：边界线
                    p1、p2：顶点
            返回：
                    (x,y)：交点
    """
    x1, y1 = b1
    x2, y2 = b2
    x3, y3 = p1
    x4, y4 = p2

    x1y2_y1x2 = x1 * y2 - y1 * x2
    x3y4_y3x4 = x3 * y4 - y3 * x4
    x1_x2_y3_y4_y1_y2_x3_x4 = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if x1_x2_y3_y4_y1_y2_x3_x4 == 0:
        return None

    x = (x1y2_y1x2 * (x3 - x4) - (x1 - x2) * x3y4_y3x4) / \
        x1_x2_y3_y4_y1_y2_x3_x4
    y = (x1y2_y1x2 * (y3 - y4) - (y1 - y2) * x3y4_y3x4) / \
        x1_x2_y3_y4_y1_y2_x3_x4

    return (x, y)


def calc_point_inside(p, x1, y1, x2, y2):
    """
            计算点是否在边界线的内侧
            返回：
                    < 0 在内侧：True
                    = 0 在边上：False
                    > 0 在外侧：False

    """
    if((x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)) >= 0:
        return False
    else:
        return True


def boundary_clip(polygon, x1, y1, x2, y2):
    """
            单条边界线裁剪多边形
    """
    p1 = polygon[-1]
    clip_polygon = []

    # 多边形的每两个点进行判断裁剪
    for p2 in polygon:
        # 计算两个点的状态
        p1_inside = calc_point_inside(p1, x1, y1, x2, y2)
        p2_inside = calc_point_inside(p2, x1, y1, x2, y2)

        # print("p1_inside:", p1_inside, " p2_inside:", p2_inside)
        # 按照规则将点加进列表
        if p1_inside and p2_inside:  # 规则1
            clip_polygon.append(p2)
        elif p1_inside and not p2_inside:  # 规则2
            interset_point = calc_intersection_point(
                (x1, y1), (x2, y2), p1, p2)
            if(interset_point != None):
                clip_polygon.append(interset_point)
        elif not p1_inside and p2_inside:  # 规则3
            interset_point = calc_intersection_point(
                (x1, y1), (x2, y2), p1, p2)
            if(interset_point != None):
                clip_polygon.append(interset_point)
                clip_polygon.append(p2)
        else:  # 规则4
            pass

        p1 = p2

    return clip_polygon


def main(boundary, polygon):
    """
            输入：
                    boundary：边界顶点坐标
                    polygon：多边形顶点坐标

            返回：
                    clip_polygon：经过裁剪的多边形顶点坐标
    """
    b1 = boundary[-1]
    clip_polygon = polygon

    for b2 in boundary:
        clip_polygon = boundary_clip(clip_polygon, b1[0], b1[1], b2[0], b2[1])
        b1 = b2

        print("clip_polygon:", clip_polygon)

    return clip_polygon


def test_calc_point_inside():
    p = (300, 200)
    b1 = (150, 200)
    b2 = (200, 200)
    flag = calc_point_inside(p, b1[0], b1[1], b2[0], b2[1])
    print("test_calc_point_inside:", flag)


if __name__ == '__main__':
    boundary = [(150, 150), (150, 200), (200, 200), (200, 150)]
    polygon = [(100, 150), (200, 250), (300, 200)]

    boundary2 = [(100, 150), (200, 250), (300, 200)]
    polygon2 = [(100, 300), (300, 300), (200, 100)]

    boundary3 = [(150, 150), (150, 200), (200, 200), (200, 150)]
    polygon3 = [(100, 150), (175, 200), (300, 150)]

    clip = main(boundary3, polygon3)

    # test_calc_point_inside()
