# iSphereMAP for Shi Lab
Python-based common computational tools for spherical regression under mismatch corruption


# Acknowledgements
I would like to express my genuine appreciation for Prof. Xu shi for her patient help and instructive suggestions. 

## -- [NOT FINISHED YET] -- ##

@Author: Yufeng Zhang (adapted from Prof. Xu Shi's R code)

[1 Installation](#installation)\
[2 Usage](#usage)


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
  ``` 
  
**Help on using tool **
```console
python3 iSphereMAP.py

positional arguments:
  src_input             the input source embeddings
  trg_input             the input target embeddings
  group_information     the group_information for source input
  {OLS,cosine,spherical,lasso}
                        Methods to estimate Pi
  nlambda               evenly break [1e-5, 1-1e-5] into intervals
  {Top_one,hard_threshold,Top_k}
                        Methods to sparse Pi
  Beta_output           the estimated beta
  Pi_output             the estimated pi

optional arguments:
  -h, --help            show this help message and exit
  --k K                 k for Top_k method in sparse_Pi
  --seed SEED           the random seed (defaults to 0)

```
 
 
 
**Get rotation matrix and weight matrix**
 ```console
python3 iSphereMAP.py source.txt target.txt group_info.txt 'OLS' 5 'hard_threshold' beta.txt Pi.txt 
 ```



