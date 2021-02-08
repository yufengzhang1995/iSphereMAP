import pyreadr
import pandas as pd
import numpy as np

def read_Rdta(file_path):

    """
    Read Rdata

    Input: Rdata consisting embeddings for X and Y and group information
    Output: Dictionary consisting embeddings for X and Y and group information

    """

    raw_data = pyreadr.read_r(file_path)
    X = raw_data['X'].to_numpy()
    Y = raw_data['Y'].to_numpy()
    grp_info = raw_data['grp.info']['g.index'].to_numpy()

    rslt = {"X":X,"Y":Y,"grp_info":grp_info}
    return rslt