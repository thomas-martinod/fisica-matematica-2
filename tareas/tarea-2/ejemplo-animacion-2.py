import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

MAX_FRAMES = 50

def data(i, x, y, z, line, ax):
    z = np.sin(x + y + i)
    ax.clear()
    line = ax.plot_surface(x, y, z, cmap='plasma', edgecolor='none')
    return line

n = 2. * np.pi
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = np.linspace(0, n, 100)
y = np.linspace(0, n, 100)
x, y = np.meshgrid(x, y)
z = np.sin(x + y)

line = ax.plot_surface(x, y, z, cmap='plasma', edgecolor='none')

ani = animation.FuncAnimation(fig, data, fargs=(x, y, z, line, ax), interval=30, blit=False, save_count=MAX_FRAMES)
plt.show()
