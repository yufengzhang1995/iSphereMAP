import numpy as np
import pandas as pd
from scipy.linalg import qr

#### Using the QR decomposition, if $A^T=QR$, and the rank of $A$ is $r$, then the last $n - r$ columns of Q make up the nullspace of $A$
def QR_Null(mat):
    
    """
    Using QR factorization to get null space of a matrix 
    
    Input: matrix
    
    Output: matrix
    """
    
    q,r = np.linalg.qr(mat,mode = 'complete')
    q_rank = np.linalg.matrix_rank(mat)
    
    if q_rank == 0:
        s = np.arange(mat.shape[1])
        ans = q[:,s]
    else:
        mask = np.ones(q.shape[1], dtype=int)
        mask[np.arange(q_rank)] = 0
        mask = mask.astype(np.bool)
        ans = q[:,mask]
    return ans 

#### Ulrich‘s Theorem 1 states that the unit $m$-vector $X$ has vom Mises-Fisher distribution with modal direction$(0,...0,1)^T$ if and only if $X^T = ((1 - W^2)^{0.5}V,W)$ where $V$ is a unit $(m-1)$-vector which is uniformly distributed and $W$ is a scalar random variable with range $[-1,1]$.
def rW(n,kappa, m):
    """
    return 1D numpy array of w corresponding to every X
    
    Input: 
    n: integer; 
    kappa: scalar
    m: integer
    
    Output: 1D numpy array
    
    """
    
    w_list = np.zeros(n)
    l = kappa
    d = m - 1
    
    b = d / (np.sqrt(4.0 * l * l + d * d) + 2.0 * l )
    x0 = (1.0 - b) / (1.0 + b)
    c = l * x0 + d * np.log(1.0 - x0 * x0)
    
    for i in np.arange(n):
        done = False
        while done == False:
            z = np.random.beta(a = d / 2.0,b = d / 2.0,size = 1)
            w = (1.0 - (1.0 + b) * z) / (1.0 - (1.0 - b) * z)
            u = np.random.uniform(size = 1)
            if (l * w + d * np.log(1.0 - x0 * w) - c) >= np.log(u):
                done = True
        w_list[i] = w
    
    return w_list

def norm_l2(mat):
    """
    Normalize matrix row-wise
    
    Input: matrix
    
    Output: normalized matrix
    
    """
    new_mat = np.zeros(shape = (mat.shape[0],mat.shape[1]))
    for i in np.arange(mat.shape[0]):
        new_mat[i,:] = mat[i,:] / np.sqrt(np.sum(np.power(mat[i,:],2)))
    return new_mat

def rvMF(n,theta):
    
    """
    Random values simulation from a von Mises-Fisher distribution
    
    Input:interger
    Output: 1D numpy array
    """
    
    d = theta.size # scalar
    kappa = np.sqrt(np.sum(np.power(theta,2))) # scalar
    
    if kappa == 0:    
        y = np.random.normal(0, 1, n * d).reshape(n,d) # n* d matrix
        y = norm_l2(y) # normalized n* d matrix
        
    if d == 1:
        (-1) * np.random.binomial(1,1 / (1 + np.exp(2 * theta)),n).reshape(n,1)
    else:
        w = rW(n,kappa,d) # 1 * n
        v = np.random.normal(0, 1, n*(d - 1)).reshape(n,(d - 1)) # n * (d-1)
        v = norm_l2(v) # n * (d-1)
        mu = (theta / kappa).reshape(d,1) 
        
        part_1 = np.multiply(np.sqrt(1 - np.power(w,2)).reshape(n,1),v) # element-wise multiplication: n* (d-1)
        part_2 = np.c_[part_1,w]
        
        part_3 = QR_Null(mu)
        part_4 = np.c_[part_3,mu]        
        y = np.dot(part_2,part_4.T)
    
    return y

def rmovMF(n,theta,alpha = np.array([1])):
    
    # Random values simulation from a von Mises-Fisher distribution
    k = theta.shape[0]
    alpha = alpha / np.sum(alpha) # weight
    
    rand_sample = []
    ind = pd.cut(np.random.uniform(size = n),bins = (len(alpha)),labels=False)
    pos = dict.fromkeys(np.arange(len(alpha)))
    for key in pos.keys():
        pos[key] = np.argwhere(ind == key)
    nms = list(pos.keys())
    
    for i in np.arange(len(pos.keys())):
        j = nms[i]
        p = pos[i]
        one_sample = rvMF(len(p),theta[j,:])
        rand_sample.append(one_sample)
    rand_sample_fl = [j for i in rand_sample for j in i]
    return np.asarray(rand_sample_fl)