import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from circle import Circle

# taken from https://stackoverflow.com/questions/30642391/how-to-draw-a-filled-arc-in-matplotlib
def draw_cap(ax, center, radius, theta1, theta2, resolution=100, **kwargs):
    # generate the points
    theta = np.linspace(theta1, theta2, resolution)
    points = np.vstack((radius*np.cos(theta) + center[0], 
                        radius*np.sin(theta) + center[1]))
    # build the polygon and add it to the axes
    poly = mpatches.Polygon(points.T, closed=True, **kwargs)
    ax.add_patch(poly)
    return poly


def draw_std_intersection_area(circle1, circle2):
    pts = Circle.get_intersection_pts(circle1, circle2)
    assert(len(pts) == 2)

    angle1_list = []
    for pt in pts:
        pt1 = pt - circle1.mean
        angle1_list.append(np.arctan2(pt1[1], pt1[0]))
    
        pt2 = pt - circle2.mean
        angle2_list.append(np.arctan(pt2[1], pt2[0]))


def draw_cap_from_intersect(ax, circle, intersection_pts, smaller_area=True, **kwargs):
    assert(len(intersection_pts) == 2)
    angles = []
    for pt in intersection_pts:
        centered_pt = pt - circle.mean
        angles.append(np.arctan2(centered_pt[1], centered_pt[0]))

    angle_diff = (angles[1] - angles[0]) % (2*np.pi)
    print(angles)
    if (angle_diff > np.pi and smaller_area) or \
        (angle_diff <= np.pi and not smaller_area):
        angles = angles[::-1]
    
    # we want to draw a cap counterclockwise from angles[0] to angles[1]

    # this is to check if going counterclockwise passes the +-pi break
    # if so, we need to add 2*pi to the second angle so that numpy can interpolate in the clockwise direction
    if angles[0] > 0 and angles[1] < 0:
        angles[1] = angles[1] + (2*np.pi)
    draw_cap(ax, circle.mean, circle.radius, angles[0], angles[1], **kwargs)




def make_main_image():
    fig = plt.figure(dpi=120)
    ax = plt.gca()
    circle1 = Circle([-0.5, 0], 1)
    circle2 = Circle([0.6, 0], 0.8)

    circle1.plot(ax, fill=False)
    circle2.plot(ax, fill=False)

    pts = Circle.get_intersection_pts(circle1, circle2)
    assert(len(pts) == 2)
        
    draw_cap_from_intersect(ax, circle1, pts, color="xkcd:orange")
    draw_cap_from_intersect(ax, circle2, pts, color="xkcd:orange")
    plt.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], c="xkcd:orange")

    # for pt in pts:
    #     plt.scatter([pt[0]], [pt[1]], c="xkcd:emerald green", linewidth=5)

    plt.scatter([circle1.mean[0]], [circle1.mean[1]], c="xkcd:emerald green")
    plt.scatter([circle2.mean[0]], [circle2.mean[1]], c="xkcd:royal blue")

    min_x = np.minimum(circle1.mean[0]-circle1.radius, circle2.mean[0]-circle2.radius)
    max_x = np.maximum(circle1.mean[1]+circle1.radius, circle2.mean[0]+circle2.radius)
    plt.xlim(min_x - 0.1, max_x + 0.1)
    plt.ylim([-1.2, 1.2])
    plt.gca().set_aspect('equal', 'box')
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis('off')
    # plt.show()
    fig.savefig('../images/main.png', bbox_inches='tight')

if __name__ == "__main__":
    make_main_image()


