
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from inter.interfaces import Environment


# A robot is placed in a room of size 45 * 45 units
# the robot has a height and diameter of 2 units

class NavEnv(Environment):

    ground_color = np.array([0, 0.8, 0.8])  #aqua
    bot_color = np.array([0, 0, 0])  # black

    def __init__(self):
        # x,y coordinates of the robot's center
        self.pos = 2 * np.ones(2)

    @property
    def actions(self):
        x = np.arange(-6,7,3)
        return [list(a) for a in np.dstack(np.meshgrid(x,x)).reshape(-1,2)]

    @property
    def state(self):
        return self.pos.copy()

    def act(self, action):
        realxMv = (
            np.random.normal(action[0], abs(action[0]/10)) if action[0] else 0)
        realyMv = (
            np.random.normal(action[1], abs(action[1]/10)) if action[1] else 0)
        self.pos += np.array([realxMv, realyMv])
        bump = not (43 >= self.pos[0] >= 2 and 43 >= self.pos[1] >= 2)
        self.pos[0] = max(min(self.pos[0],43),2)
        self.pos[1] = max(min(self.pos[1],43),2)
        if bump:
            reward = -1
        elif np.linalg.norm(45*np.ones(2) - self.pos) < 15:
            reward = 10
        else:
            reward = 0
        return self.observation(), reward

    # an image of the entire room, 10 * 10 pixel RGB image
    def observation(self):
        img = np.tile(self.ground_color, (10,10,1))
        x,y = self.pos
        xl, xr = int((x-2)/4.5), int((x+2-1e-3)//4.5)
        yl, yr = int((y-2)//4.5), int((y+2-1e-3)//4.5)
        if xl == xr:
            occupiedxs = np.array([xl])
            intensityxs = np.ones(1)
        else:
            occupiedxs = np.array([xl, xr])
            intensityxs = np.array([xr*4.5-x+2, x+2-xr*4.5])/4
        if yl == yr:
            occupiedys = np.array([yl])
            intensityys = np.ones(1)
        else:
            occupiedys = np.array([yl, yr])
            intensityys = np.array([yr*4.5-y+2, y+2-yr*4.5])/4
        cases = np.dstack(np.meshgrid(occupiedys, occupiedxs)).reshape(-1,2)
        intensities = np.outer(intensityxs, intensityys).reshape(-1)
        for i in range(len(cases)):
            img[cases[i][0],cases[i][1]] = (
                (1 - intensities[i]) * self.ground_color 
                + intensities[i] * self.bot_color)
        return img.reshape(-1)
        
    def show_observation(self, observation=None):
        if observation is None:
            return self.observation().reshape(10,10,3)
        else:
            return observation.reshape(10,10,3)

    # needs to be modified later
    def show_img(self):
        fig, ax = plt.subplots(figsize=(6,6))
        robot = plt.Circle(self.pos, 2, color='black')
        ax.add_artist(robot)
        def animate(num):
            self.act(self.actions[np.random.randint(25)])
            return robot,
        plt.xlim(0,45)
        plt.ylim(0,45)
        ani = animation.FuncAnimation(fig, animate, interval=50)
        plt.show()

