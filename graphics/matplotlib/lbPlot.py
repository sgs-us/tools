# -*- coding: utf-8 -*-

'''
all-in one hack for plotting some Graphics and creating some Animations of LBM
'''

from mpl_toolkits.mplot3d import Axes3D
from math import sqrt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Rectangle, Arrow, Circle, FancyArrowPatch
import matplotlib.cm as cm
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np
from numpy import linalg as LA
from itertools import product, combinations
import subprocess
from mpl_toolkits.mplot3d import proj3d

# setup 3D figure
fig = plt.gcf()
fig.set_size_inches(10,10)
ax = fig.gca(projection='3d')
ax.set_xlim([-1.1, 2.1])
ax.set_ylim([-1.1, 2.1])
ax.set_zlim([-1.1, 2.1])
ax.set_aspect("equal")
ax.view_init(None, -45)

# setup 2D figure
fig2 = plt.figure()
ax2 = fig2.gca()
ax2.set_xlim([-1.1, 2.1])
ax2.set_ylim([-1.1, 2.1])

'''
class for drawing arrows in 3D
'''
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


'''
draw cube in 3D
@param interval list of lower left to upper right corner
@param offset   np.array that shifts the cube to a certain position
'''
def drawCube(interval, offset):
    for s, e in combinations(np.array(list(product(interval,interval,interval))), 2):
        s = s + offset
        e = e + offset
        if np.sum(np.abs(s-e)) == interval[1]-interval[0]:
            ax.plot3D(*zip(s,e), color=[0, 0, 0, 0.25])


'''
Draw streaming of D2Q9 LBM
'''
def lb2D():
    # define some colors
    colors = iter(cm.rainbow(np.linspace(0, 1, 9)))
    for offset in list(product([-1, 0, 1], repeat=2)):
        origin = [0.5, 0.5]
        rect = Rectangle ((0 + offset[0], 0 + offset[1]), # xy
                          1,                              # width
                          1,                              # height
                          ec = "black",                   # edge color
                          fc = [0, 0, 0, 0],              # face color = transparent
                          zorder=1)                       # specify stacking
        ax2.add_patch(rect)
        if offset[0] != 0 or offset[1] != 0:
            arrow = Arrow(origin[0], origin[1], offset[0], offset[1], width = 0.5, color=next(colors),zorder=0)
            ax2.add_patch(arrow)
    # draw c_0
    circ = Circle((origin[0], origin[1]), 0.125, color="black", zorder=2)
    ax2.add_patch(circ)
    fig2.savefig("d2q9.png")


'''
Draw streaming of LBM in 3D
@param q indicate which scheme is drawn
'''
def lb3D(q=19):
    assert (q == 15 or q == 19 or q == 27)
    colors = iter(cm.rainbow(np.linspace(0, 1, q)))
    if q == 15:
        allowedL = [1, sqrt(3)]
    elif q == 19:
        allowedL = [1, sqrt(2)]
    elif q == 27:
        allowedL = [1, sqrt(2), sqrt(3)]
    for offset in list(product([-1, 0, 1], repeat=3)):
        o = np.array(offset)
        l = LA.norm(o)
        if l in allowedL:
            arrow = Arrow3D([0.5, 0.5 + offset[0]],
                            [0.5, 0.5 + offset[1]],
                            [0.5, 0.5 + offset[2]],
                            mutation_scale=20, lw=7, arrowstyle="-|>",
                            color=next(colors))
            ax.add_artist(arrow)
        drawCube([0, 1], np.array(offset))
    fig.savefig("d3q19.png")


'''
Animation function by rotating view
'''
def animate(i):
    ax.view_init(elev=10., azim=i)


'''
Draw a bad idea :)
@param i edge number
'''
def lbD3Q19EdgeStream(i):
    allowedO = [[[ 0, -1,  0], [ 0,  0, -1], [ 0, -1, -1]], #e0
                [[ 0,  1,  0], [ 0,  0, -1], [ 0,  1, -1]], #e1
                [[ 0, -1,  0], [ 0,  0,  1], [ 0, -1,  1]], #e2
                [[ 0,  1,  0], [ 0,  0,  1], [ 0,  1,  1]], #e3
                [[-1,  0,  0], [ 0,  0, -1], [-1,  0, -1]], #e4
                [[ 1,  0,  0], [ 0,  0, -1], [ 1,  0, -1]], #e5
                [[-1,  0,  0], [ 0,  0,  1], [-1,  0,  1]], #e6
                [[ 1,  0,  0], [ 0,  0,  1], [ 1,  0,  1]], #e7
                [[-1,  0,  0], [ 0, -1,  0], [-1, -1,  0]], #e8
                [[ 1,  0,  0], [ 0, -1,  0], [ 1, -1,  0]], #e9
                [[-1,  0,  0], [ 0,  1,  0], [-1,  1,  0]], #e10
                [[ 1,  0,  0], [ 0,  1,  0], [ 1,  1,  0]]] #e11
    ax.cla()
    ax.view_init(elev=10.)

    colors = iter(cm.rainbow(np.linspace(i/12., (i+1)/12., 3)))
    for offset in list(product([-1, 0, 1], repeat=3)):
        drawCube([0, 1], np.array(offset))
        if list(offset) in allowedO[i]:
            arrow = Arrow3D([0.5, 0.5 + offset[0]],
                            [0.5, 0.5 + offset[1]],
                            [0.5, 0.5 + offset[2]],
                            mutation_scale=20, lw=7, arrowstyle="-|>",
                            color=next(colors))
            ax.add_artist(arrow)
    fig.savefig("d3q19Stream_"+str(i).zfill(2)+".png")


'''
animate the bad idea from above :)
'''
def animateStream(i):
    lbD3Q19EdgeStream(i % 12)


'''
main
'''
# 2D
lb2D()

# 3D
# Create a video of a rotating grid (D3Q19)
# Animate
anim = animation.FuncAnimation(fig, animate, init_func=lb3D,
                               frames=360, interval=20, blit=True)
# Save
anim.save('lbm_rotation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

# edge streaming
for i in range(13):
    animateStream(i)

# Convert externally to video:
subprocess.call(["ffmpeg",
                "-framerate",
                "1.5",
                "-i",
                "d3q19Stream_%02d.png",
                "-c:v",
                "libx264",
                "-r",
                "150",
                "-pix_fmt",
                "yuv420p",
                "lbm_edge_stream.mp4"])
