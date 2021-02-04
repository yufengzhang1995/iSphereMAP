# iSphereMAP for Shi Lab
Python-based common computational tools for spherical regression under mismatch corruption

## -- [NOT FINISHED YET] -- ##

@Author: Yufeng Zhang (adapted from Prof. Xu Shi's R code)

[1 Installation](#installation)\
[2 Usage](#usage)\


# Installation
**Required Packages**
- numpy
- scipy
- pandas
- matplotlib

**Install from GitHub**\
You can install the package with following command:
  ```console
    $ git clone https://github.com/yufengzhang1995/iSphereMAP.git
    $ cd iSphereMAP
    $ python setup.py install
  ```
 **Generate random samples from finite mixture of von Mises-Fisher Distributions**
 ```console
 >>> from iSphereMAP import *
 >>> rmovMF(n,theta,alpha)
 ```
 
 **Get rotation matrix and weight matrix**
 ```console
 >>>iSphereMAP(X = X,Y = Y,estPi = "cosine",nlambda = 5,grp_info = grp_info)
 ```
 
 ..to be done...


