import numpy as np 
from scipy.linalg import block_diag
import pandas as pd
from .utils import *



################ Estimate W ################
############################################
def gradient_update_nogrp(X,Y,alpha = 1,convergence = 1e-4):
    """
    Actually converges after one-step update
    """ 
    
    # Normalize to make sure it is on the sphere
    X_norm = norm_l2(X)
    Y_norm = norm_l2(Y)
    
    
    # Gradient update with stepsize alpha
    oldW = np.zeros(shape=(X_norm.shape[1],X_norm.shape[1]))
    W = np.zeros(shape=(X_norm.shape[1],X_norm.shape[1]))

    
    """
    Procrustes analysis:
    
    Find an orthogonal matrix Q in R that makes two other matrices B and A as similar as possible
    
    Obejctive functionL f(Q)= ||B-QA||(frobenius norm) 
    Q = argmin f(Q)
    
    Here: perform SVD on (X.T %*% Y) and use UV' to estimate the rotation matrix W
    
    """
    gradient = np.dot(X_norm.T,Y_norm)

    error = 10000
    while (error >= convergence):
        
        # Gradient update
        W = W + alpha * gradient

        # Perform SVD approximation
        W_u,W_s,W_v = np.linalg.svd(W)
        W = np.dot(W_u,W_v)
        
        error = np.sqrt(np.sum(np.power((oldW - W),2)))
        oldW = W

    return W


################ Estimate Pi ################
############################################

def fitpi_CV(estPi,sparse_method,Ytrgt,Yhat,lambda_cv,grp_info):

    """
    Input:
    estPi: string; option: OLS / cosine / spherical; methods to evaluate the rotation matrix
    Ytrgt: numpy matrix; Y in original space 
    Yhat: numpy matrix; X projected onto Y space
    lambda_cv: scalar; threshold 
    grp_info: numpy array; indicating the groups data points belong to
    
    Output: estimated rotation matrix
    """

    # normalization just in case
    Yhat = norm_l2(Yhat) 
    Ytrgt = norm_l2(Ytrgt) 
    
    # gather group information 
    ugrp = np.unique(grp_info) # the array consisting group indexes
    n = len(ugrp) # number of groups
    Pi_all = []

    for i in np.arange(n):
        # extract the data point in the same group
        ind = np.asarray(np.where(grp_info == ugrp[i])).flatten()
        if len(ind) > 1:
            X_pi = Yhat[ind,:].T
            Y_pi = Ytrgt[ind,:].T
            if estPi == 'OLS':
                Pi_ols = np.dot(np.dot(np.linalg.inv(np.dot(X_pi.T,X_pi) + 
                                         np.diag(np.repeat(1e-10, len(ind)))),X_pi.T),Y_pi).T
            elif estPi == 'cosine':
                Pi_ols = np.dot(norm_l2(X_pi.T),norm_l2(Y_pi.T).T).T
                
            elif estPi == 'spherical':
                Pi_ols = gradient_update_nogrp(X_pi,Y_pi,alpha = 1,convergence = 1e-10)
            
            Pi_perm = np.zeros(shape = (Pi_ols.shape[0],Pi_ols.shape[1]))
            
            for i in np.arange(Pi_perm.shape[0]):
                Pi_perm[i,:] = Sparse_Pi(Pi_ols[i,:],lambda_cv,sparse_method).T        
        else:
            Pi_perm  = np.reshape([1],(1,1)) 
        if (Pi_perm.shape[0] * Pi_perm.shape[1]) != len(ind)**2:
            print("error")
            break
        Pi_all.append(Pi_perm)
    Pi = block_diag(*Pi_all) 
    return Pi

def find_lambda_cv(estPi,sparse_method,p,N,Y,Yhat,nlambda,grp_info):

    """
    Cross-validation to find lambda

    Input:
    estPi: string; option: OLS / cosine / spherical; methods to evaluate the rotation matrix
    p: dimensions
    N: number of data points
    Y: numpy matrix; Y in original space
    Yhat: numpy matrix; X projected onto Y space
    nlambda：scalar
    grp_info：


    estPi: string; option: OLS / cosine / spherical; methods to evaluate the rotation matrix
    Ytrgt: numpy matrix; X projected onto Y space
    Yhat: numpy matrix; Y in original space
    lambda_cv: scalar; 
    grp_info: numpyu array; indicating the groups data points belong to
    
    Output: 

    """

    
    #Create n.folds equally size folds: save and use for each lambda
    nfolds = 2 
    randomorder = np.random.choice(np.arange(p),size = p,replace = False)
    folds = pd.cut(randomorder,bins = nfolds,labels = False)
    
    # Perform cross validation
    # possible lambda values 
    lambda_all = np.linspace(start = 1e-5, stop = 1-1e-5, num = nlambda)
    count = 0  
    
    cv_err_all = np.zeros(shape=(len(lambda_all),nfolds))
    cv_perm_rows_all = np.zeros(shape=(len(lambda_all),nfolds))
    cv_match_rows_all = np.zeros(shape=(len(lambda_all),nfolds))
    cv_err_Yfit_all = np.zeros(shape=(len(lambda_all),nfolds))
    cv_err_Y_all = np.zeros(shape=(len(lambda_all),nfolds))
    
    for lambda_cv in lambda_all:
        for i in np.arange(nfolds):
            testIndexes = np.asarray(np.where(folds == i)).flatten()
            Pi_i = fitpi_CV(estPi = "OLS", # estPi,sparse_method = "Top_one",Ytrgt,Yhat,lambda_cv,grp_info
                            sparse_method = "Top_one",
                            Ytrgt = Y[:,testIndexes],
                            Yhat = Yhat[:,testIndexes],
                            lambda_cv = lambda_cv,
                            grp_info = grp_info)
            Yfit = np.dot(Pi_i,Yhat)
            Yfit = norm_l2(Yfit)
        
            ### compute prediction error (F norm)
            cv_err_i = np.linalg.norm(Y[:,~testIndexes]-Yfit[:,~testIndexes])
            cv_err_all[count,i] = cv_err_i
            cv_err_Yfit_all[count,i] = np.linalg.norm(Yfit[:,~testIndexes])
            cv_err_Y_all[count,i] = np.linalg.norm(Y[:,~testIndexes])
    
            ### compute number of permutation rows
            ind_onehot = np.where(np.amax(Pi_i,axis = 0) == 1)
            ind_perm = np.where(np.amax(Pi_i - np.diag(np.repeat(1,N)),axis = 0) == 1)
            cv_perm_rows_all[count,i] = len(ind_perm)
            cv_match_rows_all[count,i] = len(ind_onehot)
        count = count + 1      
    
    cv_err = np.sum(cv_err_all,axis = 0)
    cv_err_Yfit = np.sum(cv_err_Yfit_all,axis = 0)
    cv_err_Y = np.sum(cv_err_Y_all,axis = 0)
    cv_perm_rows = np.mean(cv_perm_rows_all,axis = 0)
    cv_match_rows = np.mean(cv_match_rows_all,axis = 0)
    
    results = {"cv_err":cv_err,
              "cv_err_Yfit":cv_err_Yfit,
              "cv_err_Y":cv_err_Y,
              "cv_perm_rows":cv_perm_rows,
              "cv_match_rows":cv_match_rows,
              "lambda_all":lambda_all}
    
    results = results
    
    return results   