import numpy as np 
import argparse
from scipy.linalg import block_diag
import pandas as pd
import sys
from utils import *
from iterate_update import *
from pre_process import *

# def iSphereMAP(X,Y,grp_info,estPi,nlambda,sparse_method = "Top_one",k = 3):
def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description = 'Map ICD code embeddings in two institutions into a shared space')
    parser.add_argument('src_input', help = 'the input source embeddings')
    parser.add_argument('trg_input', help = 'the input target embeddings')
    parser.add_argument('group_information', help = 'the group_information for source input')
    parser.add_argument('estPi', choices = ['OLS', 'cosine','spherical','lasso'],default = 'cosine', help = 'Methods to estimate Pi')
    parser.add_argument('nlambda', type = int, default = 5, help = 'evenly break [1e-5, 1-1e-5] into intervals')
    parser.add_argument('sparse_method', choices = ['Top_one', 'hard_threshold','Top_k'], default = 'cosine', help = 'Methods to sparse Pi')
    parser.add_argument('Beta_output', help = 'the estimated beta')
    parser.add_argument('Pi_output', help = 'the estimated pi')
    parser.add_argument('--k', type = int, default = 3, help = 'k for Top_k method in sparse_Pi')
    parser.add_argument('--seed', type = int, default = 0, help = 'the random seed (defaults to 0)')
    args = parser.parse_args()
    
    np.random.seed(args.seed)

    # read files
    # srcfile = open(args.src_input, encoding = 'utf-8', errors='surrogateescape')
    # trgfile = open(args.trg_input, encoding = 'utf-8', errors='surrogateescape')
    # grpfile = open(args.group_information, encoding = 'utf-8', errors='surrogateescape')
    X = read_mat_file(args.src_input)
    Y = read_mat_file(args.trg_input) 
    grp_info =  read_mat_file(args.group_information) 



    estPi = args.estPi
    nlambda = args.nlambda
    sparse_method = args.sparse_method
    
    # check dimension match
    if X.shape != Y.shape:
        print('The dimensions of X and Y do not match!')
        sys.exit(-1)

    if X.shape == Y.shape:
        N,p = X.shape

        # W estimation
        Beta = gradient_update_nogrp(X,Y,alpha = 1,convergence = 1e-10)
        Yhat = X.dot(Beta)

        # Lambda searching
        cv_rslt = find_lambda_cv(estPi,p,N,Y,Yhat,nlambda,grp_info,sparse_method,args.k)
        cv_err = cv_rslt["cv_err"]
        lambda_all = cv_rslt["lambda_all"]
        lambda_cv = lambda_all[np.argmin(cv_err)]

        # Pi estimation
        Pi = fitpi_CV(estPi,Y,Yhat,lambda_cv,grp_info,sparse_method,args.k)
        ind = np.asarray(np.where(np.amax(norm_l2(Pi),axis = 0) == 1)).flatten()
        X_match = Pi.dot(X)[ind,:]
        Y_match = Y[ind,:]
        index_matched = grp_info[ind]
        ugrp_matched = np.unique(index_matched)

        # Using matched data to estimate W again
        Beta_update = gradient_update_nogrp(X_match,Y_match,alpha=1,convergence=1e-10)

        results = {'beta' :Beta_update,'pi':Pi}

       # Write mapped embeddings
        # Betafile = open(args.Beta_output, mode='w', encoding=args.encoding, errors='surrogateescape')
        # Pifile = open(args.Pi_output, mode='w', encoding=args.encoding, errors='surrogateescape')
        np.savetxt(args.Beta_output,Beta_update)
        np.savetxt(args.Pi_output,Pi)
        # Betafile.close()
        # Pifile.close()


if __name__ == '__main__':
    main()