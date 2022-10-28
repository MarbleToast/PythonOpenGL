import numpy as np

def translate(mat, vec):
    mat[3] = mat[0] * vec[0] + mat[1] * vec[1] + mat[2] * vec[2] + mat[3];
    return mat

def rotateY(mat, theta):
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.identity(4)
    R[0,0] = c
    R[0,2] = s
    R[2,0] = -s
    R[2,2] = c
    return np.matmul(mat, R)

def rotateZ(mat, theta):
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.identity(4)
    R[0,0] = c
    R[0,2] = s
    R[2,0] = -s
    R[2,2] = c
    return np.matmul(mat, R)