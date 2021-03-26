class Circle(object):
    def __init__(self, center, radius):
        assert(len(center) == 2)
        self.center = np.array(center)
        self.radius = radius