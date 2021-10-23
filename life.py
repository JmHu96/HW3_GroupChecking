"""
life.py

Put any requested function or class definitions in this file.  You can use these in your script.

Please use comments and docstrings to make the file readable.
"""

# Problem 0
import numpy as np
import scipy.linalg as la
from scipy import sparse

def neighbors(i, j, m, n):
    inbrs = [-1, 0, 1]
    if i == 0:
        inbrs = [0, 1]
    if i == m-1:
        inbrs = [-1, 0]
    jnbrs = [-1, 0, 1]
    if j == 0:
        jnbrs = [0, 1]
    if j == n-1:
        jnbrs = [-1, 0]

    for delta_i in inbrs:
        for delta_j in jnbrs:
            if delta_i == delta_j == 0:
                continue
            yield i + delta_i, j + delta_j

def count_alive_neighbors(S):
    m, n = S.shape
    cts = np.zeros(S.shape, dtype=np.int64)
    for i in range(m):
        for j in range(n):
            for i2, j2 in neighbors(i, j, m, n):
                cts[i,j] = cts[i,j] + S[i2, j2]

    return cts

# Part(A)
# We will not be using them from now on because they are slow for large matrices
def compute_k(S,i,j):
    return np.ravel_multi_index(np.array([[i],[j]]), S.shape)

def compute_ij(S,k):
    return np.unravel_index([k],S.shape)

def my_reshape(s,S):
    return np.reshape(s,S.shape)


# Part(B)
def grid_adjacency(m,n):

    # This is the m*n by m*n grid that will return as the adjacency matrix
    grid = sparse.lil_matrix((m*n,m*n),dtype=np.int8)
    # This is the index that will be used as row number for each cell we have, there are
    # total of m*n of them.
    ind = 0
    # Adpoted from lecture notes
    for i in range(m):
        for j in range(n):

            inbrs = [-1, 0, 1]
            if i == 0:
                inbrs = [0, 1]
            if i == m-1:
                inbrs = [-1, 0]
            jnbrs = [-1, 0, 1]
            if j == 0:
                jnbrs = [0, 1]
            if j == n-1:
                jnbrs = [-1, 0]

            for delta_i in inbrs:
                for delta_j in jnbrs:
                    if delta_i != 0 or delta_j != 0:
                        # We here avoid using unravel as it is extremely slow
                        # We only need to update the corresponding entry
                        grid[ind,(i+delta_i)*n+delta_j+j] = 1
            # update row number
            ind = ind + 1

    return grid


# Part(C)
def count_alive_neighbors_matmul(S, A):
    """
    return counts of alive neighbors in the state array S.

    Uses matrix-vector multiplication on a flattened version of S
    """
    return np.reshape(A @ S.flatten(),S.shape)


# Part(D)
def count_alive_neighbors_slice(S):
    cts = np.zeros(S.shape, dtype=np.int8)
    # Above
    cts[1:, :] = cts[1:, :] + S[:-1, :]
    # Down
    cts[:-1, :] = cts[:-1, :] + S[1:, :]
    # Left
    cts[:, 1:] = cts[:, 1:] + S[:, :-1]
    # Right
    cts[:, :-1] = cts[:, :-1] + S[:, 1:]
    # Upper Left
    cts[1:, 1:] = cts[1:, 1:] + S[:-1, :-1]
    # Upper Right
    cts[1:, :-1] = cts[1:, :-1] + S[:-1, 1:]
    # Bottom Left
    cts[:-1, 1:] = cts[:-1, 1:] + S[1:, :-1]
    # Bottom Right
    cts[:-1, :-1] = cts[:-1, :-1] + S[1:, 1:]

    return cts