import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from circle import Circle
from curlyBrace import curlyBrace

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 
def seg_intersect(a1, a2, b1, b2) :
    def perp(a):
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot(dap, db)
    num = np.dot(dap, dp)
    return (num / denom.astype(float))*db + b1

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


def draw_arc_area(ax, center, radius, theta1, theta2, resolution=100, **kwargs):
    # generate the points
    theta = np.linspace(theta1, theta2, resolution)
    points = np.vstack((radius*np.cos(theta) + center[0], 
                        radius*np.sin(theta) + center[1]))
    points = np.concatenate((points, np.reshape(center, (2, 1))), axis=1)

    # build the polygon and add it to the axes
    poly = mpatches.Polygon(points.T, closed=True, **kwargs)
    ax.add_patch(poly)
    return poly

def get_angles_from_intersection(circle, intersection_pts, smaller_area=True):
    assert(len(intersection_pts) == 2)
    angles = []
    for pt in intersection_pts:
        centered_pt = pt - circle.mean
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


    
    intersect_pts = Circle.get_intersection_pts(circle1, circle2)
    angles1 = get_angles_from_intersection(circle1, intersect_pts)
    angles2 = get_angles_from_intersection(circle2, intersect_pts)

    pts1 = get_pts(circle1.mean, circle1.radius, angles1[0], angles1[1])
    pts2 = get_pts(circle2.mean, circle2.radius, angles2[0], angles2[1])
    poly_pts = np.concatenate((pts1, pts2), axis=1)

    poly = mpatches.Polygon(poly_pts.T, closed=True, **kwargs)
    ax.add_patch(poly)


def draw_cap_from_intersect(ax, circle, intersection_pts, smaller_area=True, **kwargs):
    assert(len(intersection_pts) == 2)
    angles = []
    for pt in intersection_pts:
        centered_pt = pt - circle.mean
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
    
    draw_cap(ax, circle.mean, circle.radius, angles[0], angles[1], **kwargs)



################################################



def make_main_image():
    fig = plt.figure(dpi=120)
    ax = plt.gca()
    circle1 = Circle([-0.5, 0], 1)
    circle2 = Circle([0.6, 0], 0.8)

    circle1_color="xkcd:grass green"
    circle2_color="xkcd:navy blue"

    pts = Circle.get_intersection_pts(circle1, circle2)
    assert(len(pts) == 2)
        
    draw_intersection(ax, circle1, circle2, color="xkcd:blood orange", alpha=0.5)


    plt.scatter([circle1.mean[0]], [circle1.mean[1]], c=circle1_color)
    plt.scatter([circle2.mean[0]], [circle2.mean[1]], c=circle2_color)
        
    circle1.plot(ax, fill=False, edgecolor=circle1_color, linewidth=2)
    circle2.plot(ax, fill=False, edgecolor=circle2_color, linewidth=2)

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

def make_cap_images():
    fig1 = plt.figure(dpi=120)
    ax = plt.gca()

    circle1 = Circle([-0.5, 0], 1)
    circle2 = Circle([0.6, 0], 0.8)

    circle1_color="xkcd:grass green"
    circle2_color="xkcd:navy blue"

    intersect_pts = Circle.get_intersection_pts(circle1, circle2)
    assert(len(intersect_pts) == 2)

    # drawing caps
    draw_cap_from_intersect(ax, circle1, intersect_pts, color=circle1_color, hatch="/", alpha=0.4)
    draw_cap_from_intersect(ax, circle2, intersect_pts, color=circle2_color, hatch="/", alpha=0.4)

    # drawing circles
    circle1.plot(ax, fill=False, edgecolor=circle1_color, linewidth=2)
    circle2.plot(ax, fill=False, edgecolor=circle2_color, linewidth=2)

    # labels
    plt.text(0.25, 0., r"$A_1$", c=circle1_color, fontsize=17)
    plt.text(-0.1, 0., r"$A_2$", c=circle2_color, fontsize=17)


    min_x = np.minimum(circle1.mean[0]-circle1.radius, circle2.mean[0]-circle2.radius)
    max_x = np.maximum(circle1.mean[1]+circle1.radius, circle2.mean[0]+circle2.radius)
    plt.xlim(min_x - 0.1, max_x + 0.1)
    plt.ylim([-1.2, 1.2])
    ax.set_aspect('equal', 'box')
    
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis('off')

    fig1.savefig('../images/caps.png', bbox_inches='tight')



    ############ 
    # figure 2
    fig2 = plt.figure(dpi=120)
    ax = plt.gca()
    circle1 = Circle([-0.5, 0], 1)
    circle2 = Circle([0.6, 0], 0.8)


    circle1_translated1 = Circle([2.5, 0], 1)
    circle1_translated2 = Circle([5.5, 0], 1)


    intersect_pts = Circle.get_intersection_pts(circle1, circle2)
    assert(len(intersect_pts) == 2)

    # first circle
    circle1.plot(ax, fill=False, edgecolor=circle1_color, linewidth=2)
    draw_cap_from_intersect(ax, circle1, intersect_pts, color=circle1_color, hatch="/", alpha=0.4)

    # second circle
    circle1_translated1.plot(ax, fill=False, edgecolor=circle1_color, linewidth=2)
    angles = get_angles_from_intersection(circle1, intersect_pts)
    draw_arc_area(ax, circle1_translated1.mean, circle1_translated1.radius, angles[0], angles[1], color=circle1_color, hatch="/", alpha=0.4)
    
    # third circle
    circle1_translated2.plot(ax, fill=False, edgecolor=circle1_color, linewidth=2)
    
    points = np.zeros((3, 2))
    points[0, :] = circle1_translated2.mean
    points[1, :] = circle1_translated2.mean + circle1_translated2.radius * np.array([np.cos(angles[0]), np.sin(angles[0])])
    points[2, :] = circle1_translated2.mean + circle1_translated2.radius * np.array([np.cos(angles[1]), np.sin(angles[1])])
    triangle = mpatches.Polygon(points, closed=True, color=circle1_color, hatch="/", alpha=0.4)
    ax.add_patch(triangle)


    # math symbols
    plt.text(0.45, -0.2, r"$=$", c=circle1_color, fontsize=40)
    plt.text(3.6, -0.2, r"$-$", c=circle1_color, fontsize=40)

    min_x = np.minimum(circle1.mean[0]-circle1.radius, circle1_translated2.mean[0]-circle1_translated2.radius)
    max_x = np.maximum(circle1.mean[1]+circle1.radius, circle1_translated2.mean[0]+circle1_translated2.radius)
    plt.xlim(min_x - 0.1, max_x + 0.1)
    plt.ylim([-1.2, 1.2])
    ax.set_aspect('equal', 'box')
    
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis('off')


    fig2.savefig('../images/caps_subtraction.png', bbox_inches='tight')

def make_notation_image():
    fig = plt.figure(dpi=120)
    ax = plt.gca()
    circle1 = Circle([-0.5, 0], 1)
    circle2 = Circle([0.6, 0], 0.8)


    circle1_color="xkcd:grass green"
    circle2_color="xkcd:navy blue"

    intersect_pts = Circle.get_intersection_pts(circle1, circle2)
    assert(len(intersect_pts) == 2)
        
    # draw centers
    plt.scatter([circle1.mean[0]], [circle1.mean[1]], c=circle1_color, zorder=100)
    plt.scatter([circle2.mean[0]], [circle2.mean[1]], c=circle2_color, zorder=100)

    # drawing circles
    circle1.plot(ax, fill=False, edgecolor=circle1_color, linewidth=2)
    circle2.plot(ax, fill=False, edgecolor=circle2_color, linewidth=2)

    # drawing radius lines
    plt.plot([circle1.mean[0], intersect_pts[1][0]], 
        [circle1.mean[1], intersect_pts[1][1]], 
        c=circle1_color, linewidth=2)
    plt.plot([circle2.mean[0], intersect_pts[1][0]], 
        [circle2.mean[1], intersect_pts[1][1]], 
        c=circle2_color, linewidth=2)



    # draw auxilary lines
    center_pt = seg_intersect(circle1.mean, circle2.mean, intersect_pts[0], intersect_pts[1])
    
    plt.plot([circle1.mean[0], center_pt[0]], [circle1.mean[1], center_pt[1]], c=circle1_color, linewidth=2)
    plt.plot([circle2.mean[0], center_pt[0]], [circle2.mean[1], center_pt[1]], c=circle2_color, linewidth=2)





    min_x = np.minimum(circle1.mean[0]-circle1.radius, circle2.mean[0]-circle2.radius)
    max_x = np.maximum(circle1.mean[1]+circle1.radius, circle2.mean[0]+circle2.radius)
    plt.xlim(min_x - 0.1, max_x + 0.1)
    plt.ylim([-1.2, 1.2])
    plt.gca().set_aspect('equal', 'box')

    
    # radius annotations
    curlyBrace(fig, ax, circle1.mean, intersect_pts[1], c=circle1_color, k_r=0.08, linestyle="--")
    plt.text(-0.45, 0.5, r"$r_1$", c=circle1_color, fontsize=20)
    curlyBrace(fig, ax, intersect_pts[1], circle2.mean, c=circle2_color, k_r=0.08, linestyle="--")
    plt.text(0.55, 0.45, r"$r_2$", c=circle2_color, fontsize=20)


    # height annotation
    curlyBrace(fig, ax, intersect_pts[1], center_pt, c="xkcd:red", k_r=0.07, linestyle="--")
    plt.text(0.3, 0.25, r"$h$", c="xkcd:red", fontsize=17)


    # length measurements
    curlyBrace(fig, ax, circle1.mean, circle2.mean, c="xkcd:red", k_r=0.06, linestyle="--")
    plt.text(0., 0.15, r"$D$", c="xkcd:red", fontsize=17)

    curlyBrace(fig, ax, circle2.mean, center_pt, c=circle2_color, k_r=0.12, linestyle="--")
    plt.text(0.3, -0.25, r"$d_2$", c=circle2_color, fontsize=17)


    curlyBrace(fig, ax, center_pt, circle1.mean, c=circle1_color, k_r=0.07, linestyle="--")
    plt.text(-0.15, -0.25, r"$d_1$", c=circle1_color, fontsize=17)


    # center labels
    plt.text(-0.7, -0.15, r"$\vec{p}_1$", c=circle1_color, fontsize=17)
    plt.text(0.7, -0.15, r"$\vec{p}_2$", c=circle2_color, fontsize=17)

    
    
    
    # drawing radial axis
    plt.plot([intersect_pts[0][0], intersect_pts[1][0]], 
        [intersect_pts[0][1], intersect_pts[1][1]], 
        color="xkcd:red")
    plt.scatter([center_pt[0]], [center_pt[1]], c="xkcd:red", zorder=100)

    plt.annotate(r"$\vec{c}$", xy=(0.18, -0.07), 
        xycoords="data", 
        xytext=(-0.3, -0.75), 
        fontsize=17,
        color="xkcd:red",
        arrowprops={"width": 1.5, 
                    "headwidth":5, 
                    "headlength": 6, 
                    "color": "xkcd:red", 
                    "alpha": 0.5})



    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.axis('off')

    fig.savefig('../images/notation.png', bbox_inches='tight')



if __name__ == "__main__":
    # make_main_image()
    # make_cap_images()
    make_notation_image()


