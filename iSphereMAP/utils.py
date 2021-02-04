import numpy as np 


def norm_l2(mat):
    new_mat = np.zeros(shape = (mat.shape[0],mat.shape[1]))
    for i in np.arange(mat.shape[0]):
        new_mat[i,:] = mat[i,:] / np.linalg.norm(mat[i,:])
    return new_mat

def Spars_Pi(vec,lambda_cv,method):
    """
    method 1 : make the pi corresponding to biggest value be 1 and rest be zero

    method 2 : set a lambda threshold; 
                if all pis don't exceed threshold then keep original values,
                otherwise, make the pi corresponding to biggest value be 1 and rest be zero
    """

    if method == "method_1":
        mask = np.zeros(vec.shape,dtype = bool)
        mask[np.argmax(vec)] = True
        vec[mask] = 1
        vec[~mask] = 0
    elif method == "method_2":
        vec_norm = vec / np.linalg.norm(vec)
        ind_max = np.where(vec_norm > lambda_cv)
        if len(ind_max) >= 1:
            mask = np.zeros(vec.shape,dtype=bool)
            mask[np.argmax(vec)] = True
            vec[mask] = 1
            vec[~mask] = 0
    return vec