## SETUP

import numpy as np
import matplotlib.pyplot as plt
# from js import document
import io
import base64


class Arm(object):
    def __init__(self):
        self.lengths = np.array([1., 1., 1.])
        self.lines = None
        self.pts = None

    def fwd_kinematics(self, thetas):
        cum_thetas = np.cumsum(thetas)
        x_diffs = self.lengths * np.cos(cum_thetas)
        y_diffs = self.lengths * np.sin(cum_thetas)

        x_coords = np.cumsum(x_diffs)
        y_coords = np.cumsum(y_diffs)

        coords = np.stack((x_coords, y_coords), axis=1)
        coords = np.concatenate((np.array([[0., 0.]]), coords), axis=0)

        return coords


    def draw(self, ax, thetas):
        coords = self.fwd_kinematics(thetas)
        assert(len(coords) == 4)

        if self.lines is None:
            self.lines = []
            for i in range(3):
                self.lines.append(ax.plot([0, 1], [0, 1], c="b")[0])
            self.pts = ax.scatter([0, 0, 0, 0], [0, 0, 0, 0], c="g")


        for i in range(len(coords) - 1):
            pt1 = coords[i, :]
            pt2 = coords[i+1, :]
            self.lines[i].set_data([pt1[0], pt2[0]], [pt1[1], pt2[1]])

            # self.lines.append(ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], c="b"))

        # self.pts = ax.scatter(coords[:, 0], coords[:, 1], c="g")
        self.pts.set_offsets(coords)

        ax.set_xlim([-4, 4])
        ax.set_ylim([-4, 4])
        ax.set_aspect('equal', 'box')

arm = Arm()
f = plt.figure()
f.gca().grid()
thetas = np.array([np.pi/4, -np.pi/8, -np.pi/8])
arm.draw(f.gca(), thetas)

# print(arm.lines)
plt.show(block=False)
plt.pause(0.1)


for i in range(100):
    thetas[0] += 0.1
    arm.draw(f.gca(), thetas)
    plt.show(block=False)
    plt.pause(0.1)


# buf = io.BytesIO()
# plt.savefig(buf, format='png')
# buf.seek(0)
# img_str = "data:image/png;base64," + base64.b64encode(buf.read()).decode('UTF-8')

# img_tag = document.getElementById("figure1")
# img_tag.src = img_str
# buf.close()



