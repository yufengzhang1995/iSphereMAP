import numpy as np 
from scipy.linalg import block_diag
import pandas as pd
import sys
from .utils import *
from .iterate_update import *
from .pre_process import *

def iSphereMAP(X,Y,grp_info,estPi,nlambda,sparse_method = "Top_one",k = 3):


    """
    Input: 
    
    file_path: 
    estPi: string; "OLS", "cosine" or "spherical"
    nlambda: scalar
    =============================================
    Output: 

    dictionary consisting estimated W and Pi
    """

    # data = read_Rdta(file_path)
    # X = data["X"]
    # Y = data["Y"]
    # grp_info = data["grp_info"]

    if X.shape != Y.shape:
        sys.exit('The dimensions of X and Y do not match!')
    
    if X.shape == Y.shape:
        N,p = X.shape

        # W estimation
        Beta = gradient_update_nogrp(X,Y,alpha = 1,convergence = 1e-10)
        Yhat = X.dot(Beta)

        # Lambda searching
        cv_rslt = find_lambda_cv(estPi,p,N,Y,Yhat,nlambda,grp_info,sparse_method,k)
        cv_err = cv_rslt["cv_err"]
        lambda_all = cv_rslt["lambda_all"]
        lambda_cv = lambda_all[np.argmin(cv_err)]

        # Pi estimation
        Pi = fitpi_CV(estPi,Y,Yhat,lambda_cv,grp_info,sparse_method,k)
        ind = np.asarray(np.where(np.amax(norm_l2(Pi),axis = 0) == 1)).flatten()
        X_match = Pi.dot(X)[ind,:]
        Y_match = Y[ind,:]
        index_matched = grp_info[ind]
        ugrp_matched = np.unique(index_matched)

        # Using matched data to estimate W again
        Beta_update = gradient_update_nogrp(X_match,Y_match,alpha=1,convergence=1e-10)

        results = {'beta' :Beta_update,'pi':Pi}

        return results

# def iSphereMAP(X,Y,estPi,nlambda,grp_info):
    
#     if X.shape == Y.shape:
#         N,p = X.shape
#         Beta = gradient_update_nogrp(X,Y,alpha = 1,convergence = 1e-10)
#         Yhat = X.dot(Beta)
#         cv_rslt = find_lambda_cv(estPi = estPi,p = p,N = N,Y = Y,Yhat = Yhat,nlambda = nlambda,grp_info = grp_info)
#         cv_err = cv_rslt["cv_err"]

#         lambda_all = cv_rslt["lambda_all"]
#         lambda_cv = lambda_all[np.argmin(cv_err)]
#         Pi = fitpi_CV(estPi = estPi,Ytrgt = Y,Yhat = Yhat,lambda_cv = lambda_cv,grp_info = grp_info)
#         ind = np.asarray(np.where(np.amax(norm_l2(Pi),axis = 0) == 1)).flatten()
#         X_match = Pi.dot(X)[ind,:]
#         Y_match = Y[ind,:]
#         index_matched = grp_info[ind]
#         ugrp_matched = np.unique(index_matched)
#         Beta_update = gradient_update_nogrp(X_match,Y_match,alpha=1,convergence=1e-10)

#         results = {'beta:' :Beta,'pi:':Pi}

#         return results