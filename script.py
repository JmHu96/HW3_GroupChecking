"""
use this file to script the creation of plots, run experiments, print information etc.

Please put in comments and docstrings in to make your code readable
"""

# Problem 0

# Part(C)
import time
import numpy as np
from life import *

csc_time = []
csr_time = []
dia_time = []
for ndim in [100,1000]:
    m,n = ndim,ndim
    np.random.seed(0)
    S = np.random.rand(m, n) < 0.3
    s = S.flatten()
    A = grid_adjacency(m,n)
    A_csc = A.tocsc()
    A_csr = A.tocsr()
    A_dia = A.todia()

    start = time.time()
    c1 = A_csc @ s
    end = time.time()
    csc_time.append(end - start)

    start = time.time()
    c2 = A_csr @ s
    end = time.time()
    csr_time.append(end - start)

    start = time.time()
    c3 = A_dia @ s
    end = time.time()
    dia_time.append(end - start)
end

print(csc_time)
print(csr_time)
print(dia_time)


np.random.seed(1)
S = np.random.rand(1000, 1000) < 0.3
start = time.time()
count_alive_neighbors(S)
end = time.time()
f"The time for count_alive_neighbors is {{}}".format(round(end-start,5))

A = grid_adjacency(m,n)
A_dia = A.todia()
A_csc = A.tocsc()
A_csr = A.tocsr()

start = time.time()
alive = count_alive_neighbors_matmul(S, A_dia)
end = time.time()
print(f"The time for dia is {{}}".format(round(end-start,5)))

start = time.time()
alive = count_alive_neighbors_matmul(S, A_csc)
end = time.time()
print(f"The time for csc is {{}}".format(round(end-start,5)))

start = time.time()
alive = count_alive_neighbors_matmul(S, A_csr)
end = time.time()
print(f"The time for csr is {{}}".format(round(end-start,5)))


# Part(D)
start = time.time()
alive = count_alive_neighbors_slice(S)
end = time.time()
print(f"The time for slice is {{}}".format(round(end-start,5)))



# Part(E)
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

np.random.seed(1)
S = np.random.rand(50, 50) < 0.2
fig = plt.figure(figsize=(5,5))
fig.set_tight_layout(True)

# Plot an image that persists
im = plt.imshow(S, animated=True)
plt.axis('off') # turn off ticks

def update(*args):

    global S
    
    # Update image to display next step
    cts = count_alive_neighbors_slice(S)
    # Game of life update
    S = np.logical_or(
        np.logical_and(cts == 2, S),
        cts == 3
    )
    im.set_array(S)
    return im,

anim = FuncAnimation(fig, update, frames=100, interval=200, blit=True)
#anim.save('life.gif', dpi=100, writer='imagemagick')