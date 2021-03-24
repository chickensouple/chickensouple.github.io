import numpy as np
import matplotlib.pyplot as plt

class Circle(object):
    def __init__(self, mean, radius):
        assert(len(mean) == 2)
        self.mean = np.array(mean)
        self.radius = radius

    def get_area(self):
        return np.pi * self.radius**2
        
    def __str__(self):
        return "(({}, {}), {}, {})".format(self.mean[0], self.mean[1], self.radius)
    

    @staticmethod
    def get_intersection_pts(circle1, circle2):
        """
        This function will return 0, 1, or 2 intersection points.
        This function will ignore the case when circles are coincident.
        """
        dist = np.linalg.norm(circle1.mean - circle2.mean)
        if dist >= (circle1.radius + circle2.radius):
            # circles are too far apart
            return []
        elif dist < np.abs(circle1.radius - circle2.radius):
            # one circle is fully within the other
            return []
        elif abs(dist - np.abs(circle1.radius - circle2.radius)) < 1e-3 \
            or abs(dist - (circle1.radius + circle2.radius)) < 1e-3:
            # circle is touching at one point
            pt = circle1.mean + circle1.radius * (circle2.mean - circle1.mean) / dist
            return [pt]
        elif np.all(np.abs(circle1.mean - circle2.mean) < 1e-3) and np.abs(circle1.radius - circle2.radius) < 1e-3:
            # nearly coincident circles
            return []
        else:
            # two intersection pts
            r1_sq = circle1.radius**2
            r2_sq = circle2.radius**2
            d_sq = dist**2
            pt_base = 0.5 * (circle1.mean + circle2.mean) + \
                0.5 * ((r1_sq - r2_sq) / d_sq) * (circle2.mean - circle1.mean)
        
            delta_y = circle2.mean[1] - circle1.mean[1]
            delta_x = circle1.mean[0] - circle2.mean[0]
            plus_minus = 0.5 * np.sqrt((2 * (r1_sq + r2_sq) / d_sq) - ((r1_sq - r2_sq)/d_sq)**2 - 1) * np.array([delta_y, delta_x])
            return [pt_base+plus_minus, pt_base-plus_minus]

    @staticmethod
    def compute_intersection_area(circle1, circle2):
        dist = np.linalg.norm(circle1.mean - circle2.mean)

        if dist >= (circle1.radius + circle2.radius):
            # no overlap
            return 0
        elif dist + circle1.radius <= circle2.radius:
            # circle1 is fully contained in circle 2
            return np.pi * circle1.radius**2
        elif dist + circle2.radius <= circle1.radius:
            # circle2 is fully contained in circle 1
            return np.pi * circle2.radius**2
        elif np.all(np.abs(circle1.mean - circle2.mean) < 1e-3) and np.abs(circle1.radius - circle2.radius) < 1e-3:
            # nearly coincident circles
            return np.pi * circle1.radius**2
        else:
            # "normal" intersection with two intersection points
            r1_sq = circle1.radius**2
            r2_sq = circle2.radius**2
            dist_sq = dist**2

            invert_circle2 = False
            invert_circle1 = False

            l2 = (r1_sq - r2_sq - dist_sq) / (2 * dist)
            if l2 > 0:
                # the intersection line is over halfway across circle2
                l1 = dist + l2
                invert_circle2 = True
            else:
                l1 = (r2_sq - r1_sq - dist_sq) / (2 * dist)
                if l1 > 0:
                    # the intersection line is over halfway across circle1
                    l2 = dist + l1
                    invert_circle1 = True
                else:
                    # a "normal" intersection
                    l1 = (r1_sq - r2_sq + dist_sq) / (2*dist)
                    l2 = dist - l1
            
            h = np.sqrt(r1_sq - l1**2)
            area1 = (r1_sq * np.arcsin(h / circle1.radius)) - (h*l1)
            area2 = (r2_sq * np.arcsin(h / circle2.radius)) - (h*l2)
            if invert_circle2:
                area2 = np.pi * r2_sq - area2
            elif invert_circle1:
                area1 = np.pi * r1_sq - area1

            return area1 + area2


    def plot(self, ax, **kwargs):
        circle = plt.Circle(self.mean, self.radius, **kwargs)
        ax.add_patch(circle)

