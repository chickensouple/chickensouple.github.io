def get_intersection_area(circle1, circle2):
    D = np.linalg.norm(circle1.center - circle2.center)
    if D >= (circle1.radius + circle2.radius):
        # no overlap
        return 0
    elif D + circle1.radius <= circle2.radius:
        # circle1 is fully contained in circle2
        return np.pi * circle1.radius**2
    elif D + circle2.radius <= circle1.radius:
        return np.pi * circle2.radius**2
    
    # intersection with two intersection points
    r1_sq = circle1.radius**2
    r2_sq = circle2.radius**2
    D_sq = D**2

    invert_circle2 = False
    invert_circle1 = False

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
    area1 = (r1_sq * np.arcsin(h / circle1.radius)) - (h*d1)
    area2 = (r2_sq * np.arcsin(h / circle2.radius)) - (h*d2)
    if invert_circle2:
        area2 = np.pi * r2_sq - area2
    elif invert_circle1:
        area1 = np.pi * r1_sq - area1
    
    return area1 + area2
