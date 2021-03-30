class CircleIntersectionType(object):
    TOO_FAR = 0
    CIRCLE1_IN_CIRCLE2 = 1
    CIRCLE2_IN_CIRCLE1 = 2
    RADIAL_AXIS_CENTERED = 3
    RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE1 = 4
    RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE2 = 5

def get_intersection_pts(p1, r1, p2, r2):
    """
    This function will return 0, 1, or 2 intersection points.
    This function will ignore the case when circles are coincident.
    """
    dist = np.linalg.norm(p1 - p2)
    if dist >= (r1 + r2):
        # circles are too far apart
        return [], CircleIntersectionType.TOO_FAR
    elif dist <= abs(r1 - r2):
        if r1 < r2:
            return [], CircleIntersectionType.CIRCLE1_IN_CIRCLE2
        else:
            return [], CircleIntersectionType.CIRCLE2_IN_CIRCLE1
    else:
        # two intersection pts
        r1_sq = r1**2
        r2_sq = r2**2
        d_sq = dist**2
        pt_base = 0.5 * (p1 + p2) + \
            0.5 * ((r1_sq - r2_sq) / d_sq) * (p2 - p1)
    
        delta_y = p2[1] - p1[1]
        delta_x = p1[0] - p2[0]
        plus_minus = 0.5 * np.sqrt((2 * (r1_sq + r2_sq) / d_sq) - ((r1_sq - r2_sq)/d_sq)**2 - 1) * np.array([delta_y, delta_x])
        intersect_pts = [pt_base+plus_minus, pt_base-plus_minus]


        d1 = (r2_sq - r1_sq - d_sq) / (2 * dist)
        if d1 > 0:
            return intersect_pts, CircleIntersectionType.RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE1
        d2 = (r1_sq - r2_sq - d_sq) / (2 * dist)
        if d2 > 0:
            return intersect_pts, CircleIntersectionType.RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE2
        return intersect_pts, CircleIntersectionType.RADIAL_AXIS_CENTERED


def plot_circle(ax, p, r, **kwargs):
    circle = plt.Circle(p, r, **kwargs)
    ax.add_patch(circle)
    return circle

def get_angles_from_intersection(p, r, intersection_pts, smaller_area=True):
    assert(len(intersection_pts) == 2)
    angles = []
    for pt in intersection_pts:
        centered_pt = pt - p
        angles.append(np.arctan2(centered_pt[1], centered_pt[0]))


    angle_diff = (angles[1] - angles[0]) % (2*np.pi)
    if (angle_diff > np.pi and smaller_area) or \
        (angle_diff <= np.pi and not smaller_area):
        angles = angles[::-1]
    
    # we want to draw a cap counterclockwise from angles[0] to angles[1]
    # make sure angles[1] is always greater so interpolation will go counterclockwise
    if angles[0] > angles[1]:
        angles[1] = angles[1] + (2*np.pi)
    return angles

def draw_intersection(ax, p1, r1, p2, r2, **kwargs):
    def get_pts(center, radius, theta1, theta2, resolution=18):
        theta = np.linspace(theta1, theta2, resolution)
        points = np.vstack((radius*np.cos(theta) + center[0], 
                            radius*np.sin(theta) + center[1]))
        return points
    
    intersect_pts, intersect_type = get_intersection_pts(p1, r1, p2, r2)

    if intersect_type == CircleIntersectionType.TOO_FAR:
        return None

    if intersect_type == CircleIntersectionType.CIRCLE1_IN_CIRCLE2:
        circle_patch = plot_circle(ax, p1, r1, **kwargs)
        return circle_patch
    
    if intersect_type == CircleIntersectionType.CIRCLE2_IN_CIRCLE1:
        circle_patch = plot_circle(ax, p2, r2, **kwargs)
        return circle_patch

    if intersect_type == CircleIntersectionType.RADIAL_AXIS_CENTERED:
        angles1 = get_angles_from_intersection(p1, r1, intersect_pts)
        angles2 = get_angles_from_intersection(p2, r2, intersect_pts)
        pts1 = get_pts(p1, r1, angles1[0], angles1[1])
        pts2 = get_pts(p2, r2, angles2[0], angles2[1])
        poly_pts = np.concatenate((pts1, pts2), axis=1)

        poly = mpatches.Polygon(poly_pts.T, closed=True, **kwargs)
        ax.add_patch(poly)
        return poly

    if intersect_type == CircleIntersectionType.RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE1:
        angles1 = get_angles_from_intersection(p1, r1, intersect_pts, smaller_area=False)
        angles2 = get_angles_from_intersection(p2, r2, intersect_pts)
        pts1 = get_pts(p1, r1, angles1[0], angles1[1])
        pts2 = get_pts(p2, r2, angles2[0], angles2[1])
        poly_pts = np.concatenate((pts1, pts2), axis=1)
        poly = mpatches.Polygon(poly_pts.T, closed=True, **kwargs)
        ax.add_patch(poly)
        return poly

    if intersect_type == CircleIntersectionType.RADIAL_AXIS_NONCENTERED_SMALL_CIRCLE2:
        angles1 = get_angles_from_intersection(p1, r1, intersect_pts)
        angles2 = get_angles_from_intersection(p2, r2, intersect_pts, smaller_area=False)
        pts1 = get_pts(p1, r1, angles1[0], angles1[1])
        pts2 = get_pts(p2, r2, angles2[0], angles2[1])
        poly_pts = np.concatenate((pts1, pts2), axis=1)
        poly = mpatches.Polygon(poly_pts.T, closed=True, **kwargs)
        ax.add_patch(poly)
        return poly

def draw_main(ax, p1, r1, p2, r2):
    circle1_color="xkcd:grass green"
    circle2_color="xkcd:royal blue"

    # drawing circles
    circle1_patch = plot_circle(ax, p1, r1, fill=False, edgecolor=circle1_color, linewidth=2)
    circle2_patch = plot_circle(ax, p2, r2, fill=False, edgecolor=circle2_color, linewidth=2)
    intersect_patch = draw_intersection(ax, p1, r1, p2, r2, color="red", alpha=0.5)

    plt.xlim([-3, 3])
    plt.ylim([-3, 3])
    ax.set_aspect('equal', 'box')

    return circle1_patch, circle2_patch, intersect_patch

fig1 = plt.figure()
p1 = np.array([0., 0.])
r1 = 1.0
p2 = np.array([0.5, 0])
r2 = 0.7

ax = fig1.gca()
# Initial Drawing of the circle
circle1_patch, circle2_patch, intersect_patch = draw_main(ax, p1, r1, p2, r2)
ax.grid()
plt_text = ax.text(-2, -2.5, "Intersection Area: {}".format(get_intersection_area(p1, r1, p2, r2)))

# setup for webasm canvas backend
def create_root_element2(self):
    return document.getElementById('widget-output')
#override create_root_element method of canvas 
fig1.canvas.create_root_element = create_root_element2.__get__(
    create_root_element2, fig1.canvas.__class__)


def redraw(event):
    global fig1
    global p1, r1, p2, r2
    global circle1_patch, circle2_patch, intersect_patch
    global plt_text

    circle1_patch.set_radius(r1)
    circle2_patch.set_radius(r2)
    circle2_patch.center = (event.xdata, event.ydata)
    p2 = np.array([event.xdata, event.ydata])

    if intersect_patch is not None:
        intersect_patch.remove()
    intersect_patch = draw_intersection(fig1.gca(), p1, r1, p2, r2, color="red", alpha=0.5)

    plt_text.set_text("Intersection Area: {}".format(get_intersection_area(p1, r1, p2, r2)))
    fig1.canvas.draw()

def redraw_pyodide_cb():
    global fig1
    global p1, r1, p2, r2
    global circle1_patch, circle2_patch, intersect_patch
    global plt_text

    circle1_patch.set_radius(r1)
    circle2_patch.set_radius(r2)

    if intersect_patch is not None:
        intersect_patch.remove()
    intersect_patch = draw_intersection(fig1.gca(), p1, r1, p2, r2, color="red", alpha=0.5)

    plt_text.set_text("Intersection Area: {}".format(get_intersection_area(p1, r1, p2, r2)))
    fig1.canvas.draw()

fig1.canvas.mpl_connect("button_press_event", redraw)    
fig1.canvas.show()






