import numpy as np 


def read_mat_file(vector_file):
    with open(vector_file,'r') as f:
        embed = []
        for i,line in enumerate(f):
            elems = line.rstrip('\n').split(' ')
            embed.append(elems)
    return np.array(embed).astype(float)




# def file_write(mat,file_name):
#     txt_file = []

#     for i in np.arange(mat.shape[0]):
#         line = ' '.join(mat[i,:])
#         txt_file.append(line)
#     txt_file = '\n'.join(txt_file)
#     with open(file_name, "w") as output:
#         output.write(str(txt_file))



def norm_l2(mat):
    new_mat = np.zeros(shape = (mat.shape[0],mat.shape[1]))
    for i in np.arange(mat.shape[0]):
        new_mat[i,:] = mat[i,:] / np.linalg.norm(mat[i,:])
    return new_mat

def Sparse_Pi(vec,method,lambda_cv = None,k = None):
    """
    method 1 : make the pi corresponding to biggest value be 1 and rest be zero

    method 2 : set a lambda threshold; 
                if all pis don't exceed threshold then keep original values,
                otherwise, make the pi corresponding to biggest value be 1 and rest be zero
    """

    if method == "Top_one":
#         print("Top_one")
        mask = np.zeros(vec.shape,dtype = bool)
        mask[np.argmax(vec)] = True
        vec[mask] = 1
        vec[~mask] = 0
    elif method == "hard_threshold":
#         print("hard_threshold")
        vec_norm = vec / np.linalg.norm(vec)
        ind_max = np.where(vec_norm > lambda_cv)
        if len(ind_max) >= 1:
            mask = np.zeros(vec.shape,dtype=bool)
            mask[np.argmax(vec)] = True
            vec[mask] = 1
            vec[~mask] = 0
    elif method == "Top_k":
        mask = np.zeros(vec.shape,dtype = bool)
        mask[vec.argsort()[-k:][::-1]] = True
        vec[mask] = 1
        vec[~mask] = 0

    return vec