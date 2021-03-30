# circle 1 radius
r1 = 1.0

# circle 2 radius
r2 = 0.7

def get_intersection_area(p1, r1, p2, r2):
    """
    Computes the area of intersection between two circles.

    p1 and p2 are length 2 np.arrays that represent the circle center locations.
    r1 and r2 are their respective radiuses.
    """
    D = np.linalg.norm(p1 - p2)
    if D >= (r1 + r2):
        # no overlap
        return 0
    elif D <= abs(r1 - r2):
        # one circle is fully within the other
        rad = np.minimum(r1, r2)
        return np.pi * rad**2
    
    # intersection with two intersection points
    r1_sq = r1**2
    r2_sq = r2**2
    D_sq = D**2

    invert_circle1 = False
    invert_circle2 = False

    d1 = (r2_sq - r1_sq - D_sq) / (2 * D)
    if d1 > 0:
        # The radical axis is not between the circle centers
        # and circle1 is the smaller circle
        d2 = D + d1
        invert_circle1 = True
    else:
        d2 = (r1_sq - r2_sq - D_sq) / (2 * D)
        if d2 > 0:
            # The radical axis is not between the circle centers
            # and circle2 is the smaller circle
            d1 = D + d2
            invert_circle2 = True
        else:
            # The radical axis is between the circle centers
            d1 = (r1_sq - r2_sq + D_sq) / (2*D)
            d2 = D - d1
    
    h = np.sqrt(r1_sq - d1**2)
    area1 = (r1_sq * np.arcsin(h / r1)) - (h*d1)
    area2 = (r2_sq * np.arcsin(h / r2)) - (h*d2)
    if invert_circle2:
        area2 = np.pi * r2_sq - area2
    elif invert_circle1:
        area1 = np.pi * r1_sq - area1
    
    return area1 + area2