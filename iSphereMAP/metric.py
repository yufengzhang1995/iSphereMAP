import numpy as np

def SplitData(split_size,source,target):   
    
    num_line = source.shape[0]
    arr = np.arange(num_line)
    np.random.shuffle(arr)
    list_all = arr.tolist()
    each_size = int((num_line + 1) / split_size) # size of each split sets 
    source_split = []
    source_split_all = []
    target_split = [] 
    target_split_all = [] 
    count_num = 0; 
    count_split = 0  
    for i in range(len(list_all)): 
        index = int(list_all[i])
        source_split.append(source[index,:])
        target_split.append(target[index,:])
        count_num += 1
        if count_num == each_size:
            count_split += 1 
            source_split_all.append(embed_split) 
            target_split_all.append(target_split) 
            source_split = []
            target_split = [] 
            count_num = 0
            
    return np.array(source_split_all).astype(float),np.array(target_split_all).astype(float)


def Metric(method,mat_1,mat_2):
    if method == "Frobenius":
        res = np.linalg.norm(mat_1 - mat_2)
    return res 

def cross_validation(split_size,source,target,method,seed = 4):
    source_all,target_all = SplitData(split_size,source,target,seed)
    output = []
    for i in np.arange(split_size):
        source_embed = source_all[i,:,:]
        target_embed = target_all[i,:,:]
        W = learn_transformation(source_embed,target_embed)
        Y_hat = np.matmul(source_embed, W)
        output.append(metric(method,Y_hat,target_embed))
    return sum(output)/len(output)






    











