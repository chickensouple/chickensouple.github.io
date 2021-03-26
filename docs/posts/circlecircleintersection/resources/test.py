import numpy as np
from circle_pyodide import Circle
from intersection_pyodide import get_intersection_area
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Circle(object):
    def __init__(self, center, radius):
        assert(len(center) == 2)
        self.center = np.array(center)
        self.radius = radius


class CircleIntersectionType(object):
    TOO_FAR = 0
    CIRCLE1_IN_CIRCLE2 = 1
    CIRCLE2_IN_CIRCLE1 = 2
    RADIAL_AXIS_CENTERED = 3
    RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE1 = 4
    RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE2 = 5

def get_intersection_pts(circle1, circle2):
    """
    This function will return 0, 1, or 2 intersection points.
    This function will ignore the case when circles are coincident.
    """
    dist = np.linalg.norm(circle1.center - circle2.center)
    if dist >= (circle1.radius + circle2.radius):
        # circles are too far apart
        return [], CircleIntersectionType.TOO_FAR
    elif dist + circle1.radius <= circle2.radius:
        return [], CircleIntersectionType.CIRCLE1_IN_CIRCLE2
    elif dist + circle2.radius <= circle1.radius:
        return [], CircleIntersectionType.CIRCLE2_IN_CIRCLE1
    else:
        # two intersection pts
        r1_sq = circle1.radius**2
        r2_sq = circle2.radius**2
        d_sq = dist**2
        pt_base = 0.5 * (circle1.center + circle2.center) + \
            0.5 * ((r1_sq - r2_sq) / d_sq) * (circle2.center - circle1.center)
    
        delta_y = circle2.center[1] - circle1.center[1]
        delta_x = circle1.center[0] - circle2.center[0]
        plus_minus = 0.5 * np.sqrt((2 * (r1_sq + r2_sq) / d_sq) - ((r1_sq - r2_sq)/d_sq)**2 - 1) * np.array([delta_y, delta_x])
        intersect_pts = [pt_base+plus_minus, pt_base-plus_minus]


        d1 = (r2_sq - r1_sq - d_sq) / (2 * dist)
        if d1 > 0:
            return intersect_pts, CircleIntersectionType.RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE1
        d2 = (r1_sq - r2_sq - d_sq) / (2 * dist)
        if d2 > 0:
            return intersect_pts, CircleIntersectionType.RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE2
        return intersect_pts, CircleIntersectionType.RADIAL_AXIS_CENTERED


def plot_circle(ax, circle, **kwargs):
    circle = plt.Circle(circle.center, circle.radius, **kwargs)
    ax.add_patch(circle)

def get_angles_from_intersection(circle, intersection_pts, smaller_area=True):
    assert(len(intersection_pts) == 2)
    angles = []
    for pt in intersection_pts:
        centered_pt = pt - circle.center
        angles.append(np.arctan2(centered_pt[1], centered_pt[0]))


    angle_diff = (angles[1] - angles[0]) % (2*np.pi)
    if (angle_diff > np.pi and smaller_area) or \
        (angle_diff <= np.pi and not smaller_area):
        angles = angles[::-1]
    
    # we want to draw a cap counterclockwise from angles[0] to angles[1]

    # this is to check if going counterclockwise passes the +-pi break
    # if so, we need to add 2*pi to the second angle so that numpy can interpolate in the clockwise direction
    if angles[0] > 0 and angles[1] < 0:
        angles[1] = angles[1] + (2*np.pi)
    return angles

def draw_intersection(ax, circle1, circle2, **kwargs):
    def get_pts(center, radius, theta1, theta2, resolution=200):
        theta = np.linspace(theta1, theta2, resolution)
        points = np.vstack((radius*np.cos(theta) + center[0], 
                            radius*np.sin(theta) + center[1]))
        return points
    
    intersect_pts, intersect_type = get_intersection_pts(circle1, circle2)

    if intersect_type == CircleIntersectionType.TOO_FAR:
        return

    if intersect_type == CircleIntersectionType.CIRCLE1_IN_CIRCLE2:
        plot_circle(ax, circle1, **kwargs)
        return
    
    if intersect_type == CircleIntersectionType.CIRCLE2_IN_CIRCLE1:
        plot_circle(ax, circle2, **kwargs)
        return

    if intersect_type == CircleIntersectionType.RADIAL_AXIS_CENTERED:
        angles1 = get_angles_from_intersection(circle1, intersect_pts)
        angles2 = get_angles_from_intersection(circle2, intersect_pts)
        pts1 = get_pts(circle1.center, circle1.radius, angles1[0], angles1[1])
        pts2 = get_pts(circle2.center, circle2.radius, angles2[0], angles2[1])
        poly_pts = np.concatenate((pts1, pts2), axis=1)

        poly = mpatches.Polygon(poly_pts.T, closed=True, **kwargs)
        ax.add_patch(poly)
        return

    if intersect_type == CircleIntersectionType.RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE1:
        angles1 = get_angles_from_intersection(circle1, intersect_pts, smaller_area=False)
        angles2 = get_angles_from_intersection(circle2, intersect_pts)
        pts1 = get_pts(circle1.center, circle1.radius, angles1[0], angles1[1])
        pts2 = get_pts(circle2.center, circle2.radius, angles2[0], angles2[1])
        poly_pts = np.concatenate((pts1, pts2), axis=1)
        poly = mpatches.Polygon(poly_pts.T, closed=True, **kwargs)
        ax.add_patch(poly)
        return

    if intersect_type == CircleIntersectionType.RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE2:
        angles1 = get_angles_from_intersection(circle1, intersect_pts)
        angles2 = get_angles_from_intersection(circle2, intersect_pts, smaller_area=False)
        pts1 = get_pts(circle1.center, circle1.radius, angles1[0], angles1[1])
        pts2 = get_pts(circle2.center, circle2.radius, angles2[0], angles2[1])
        poly_pts = np.concatenate((pts1, pts2), axis=1)
        poly = mpatches.Polygon(poly_pts.T, closed=True, **kwargs)
        ax.add_patch(poly)
        return

if __name__ == "__main__":

    circle1_color="xkcd:grass green"
    circle2_color="xkcd:royal blue"


    fig1 = plt.figure(dpi=120)
    ax = plt.gca()
    circle1 = Circle([0, 0], 1)
    circle2 = Circle([-0.5, 0.], 0.7)

    
    # drawing circles
    plot_circle(ax, circle1, fill=False, edgecolor=circle1_color, linewidth=2)
    plot_circle(ax, circle2, fill=False, edgecolor=circle2_color, linewidth=2)
    draw_intersection(ax, circle1, circle2, color="red", alpha=0.5)


    plt.xlim([-5, 5])
    plt.ylim([-5, 5])
    ax.set_aspect('equal', 'box')
    

    plt.show()

    # circle1 = Circle([0, 0], 1)

    # x_list = np.linspace(-1.5, 1.5, 100)
    # area_list = []
    # for x in x_list:
    #     circle2 = Circle([x, 0], 0.5)
    #     area = get_intersection_area(circle1, circle2)
    #     area_list.append(area)

    # plt.plot(x_list, area_list)
    # plt.show()

