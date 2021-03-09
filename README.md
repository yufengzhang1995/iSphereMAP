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

The input file should be numerical matrix in txt file

**Install from GitHub**\
You can install the package with following command:
  ```console
    $ git clone https://github.com/yufengzhang1995/iSphereMAP.git
  ``` 
  

# Usage
**Input file format**
The input file should be numerical matrix in txt file


**Help on using tool**
```
python3 iSphereMAP.py

```
 
**Get rotation matrix and weight matrix**
 ```
python3 iSphereMAP.py source.txt target.txt group_info.txt 'OLS' 5 'hard_threshold' beta.txt Pi.txt 
 ```



