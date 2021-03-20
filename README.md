# iSphereMAP for Shi Lab
Python-based common computational tools for spherical regression under mismatch corruption:
Map ICD code embeddings between two institutions


# Acknowledgements
I would like to express my genuine appreciation for Prof. Xu shi for her patient help and instructive suggestions. 

@Author: Yufeng Zhang (adapted from Prof. Xu Shi's R code)

If you use this software for academic research, [please cite the relevant paper(s)](#publications).

[1 Installation](#installation)\
[2 Usage](#usage)\
[3 Example](#example)\
[4 Publication](#publication)


# Installation
**Required Packages**
- numpy
- scipy
- sklearn
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

```
* positional arguments:
  src_input             the input source embeddings(txt file)
  trg_input             the input target embeddings(txt file)
  group_information     the group_information for source input(txt file)
  {OLS,cosine,spherical,lasso} Methods to estimate Pi (string)
  nlambda               evenly break [1e-5, 1-1e-5] into intervals (integer)
  {Top_one,hard_threshold,Top_k}
                        Methods to sparse Pi (string)
  Beta_output           the estimated beta (string, indicating path)
  Pi_output             the estimated pi (string, indicating path)

* optional arguments:
  -h, --help            show this help message and exit
  --k K                 k for Top_k method in sparse_Pi (integer)
  --seed SEED           the random seed (defaults to 0) (integer)
```

**Help on using tool**
```
python3 iSphereMAP.py
```
 
**Get rotation matrix and weight matrix**
 ```
 python3 iSphereMAP.py source.txt target.txt group_info.txt 'OLS' 5 'hard_threshold' beta.txt Pi.txt 
 ```
# Example


Using data under example_data directory

```
python3 iSphereMAP.py ../example_data/en_overlap.txt ../example_data/it_overlap.txt ../example_data/group_info.txt 'cosine' 5 'hard_threshold' beta.txt Pi.txt
```




# Publication
If you use this software for academic research, please cite the paper:
```
@article{shi2020spherical,
  title={Spherical regression under mismatch corruption with application to automated knowledge translation},
  author={Shi, Xu and Li, Xiaoou and Cai, Tianxi},
  journal={Journal of the American Statistical Association},
  pages={1--12},
  year={2020},
  publisher={Taylor \& Francis}
}
```
