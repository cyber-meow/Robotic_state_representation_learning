
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from inter.interaction import Interaction
from environment.nav_env_ext import NavEnvExt
from bot.explore_bot import ExploreBot


nav_env = NavEnvExt()
bot = ExploreBot()
inter = Interaction(nav_env, bot)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
ax1.axis('off'); ax2.axis('off'); ax3.axis('off')

obs1 = nav_env.top_down_view(128)
obs2 = nav_env.egocentric_view(128)
obs3 = nav_env.show_observation(inter._observation)

im1 = ax1.imshow(obs1, origin='lower')
im2 = ax2.imshow(obs2, origin='lower')
im3 = ax3.imshow(obs3, interpolation='none', origin='lower')

def animate(*args):
    inter.interact()
    im1.set_array(nav_env.top_down_view(128))
    im2.set_array(nav_env.egocentric_view(128))
    im3.set_array(nav_env.show_observation(inter._observation))
    return im1, im2, im3

def run():
    ani = animation.FuncAnimation(fig, animate, 1000, interval=100, blit=True)
    ani.save("nav_env_ext.mp4", writer='ffmpeg')
    plt.show()
    return ani
