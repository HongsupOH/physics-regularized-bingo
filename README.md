# Physics Regularized Bingo (PR-Bingo)
## Table of contents
    
* [Authors](#Authors)
* [Introduction](#Introduction)
* [Install Bingo](#Install-Bingo)
* [Install PR-Bingo](#Install-PR-Bingo)
* [Tutorials](#Tutorials)
* [Implement code with MPI](#Implement-code-with-MPI)
   * [Beam bending problem](#Beam-bending-problem)
   * [Poisson's equation](#Poissons-equation)
* [Contact](#Contact)

## Authors
- <b>[Hongsup Oh](https://github.com/HongsupOH)</b>, Department of Mechanical Engineering, University of Utah
- <b>[Roman Amici](https://github.com/roman-amici)</b>, Scientific Computing and Imaging Institute, School of Computing, University of Utah
- <b>[Geoffrey Bomarito](https://github.com/gbomarito)</b>, NASA Langley Research Center
- <b>[Shandian Zhe](https://users.cs.utah.edu/~zhe/)</b>, School of Computing, University of Utah
- <b>[Robert M. Kirby](https://users.cs.utah.edu/~kirby/)</b>, Scientific Computing and Imaging Institute, School of Computing, University of Utah
- <b>[Jacob D. Hochhalter](https://www.mech.utah.edu/directory/faculty/jacob-hochhalter/)</b>, Department of Mechanical Engineering, University of Utah

## Introduction
PR-GPSR is an interpretable machine learning package for the discovery of analytic solutions to differential equations. 
our paper is available for reading in [the Engineering with Computers](https://link.springer.com/article/10.1007/s00366-023-01915-7) journal or on [arxiv](https://arxiv.org/abs/2302.03175).

## Install Bingo
To install [Bingo](https://github.com/nasa/bingo), simply use `pip` or `pip3`. Detail descriptions of installation are [Here](https://nightdr.github.io/bingo/installation.html).
```
pip install bingo-nasa
```

You need to have `mpi` to properly install `mpi4py`. It can be installed by  
```
sudo apt install mpich 
```

## Install PR-Bingo
`RP-Bingo` is simply installed by `git clone`, after installing `Bingo`.
```
git clone https://github.com/HongsupOH/physics-regularized-bingo
```
## Tutorials
Two numerical experiments based on boundary-value
problems were selected to verify that physics-regularized
GPSR can evolve known solutions to differential equations. The first experiment verifies the solution to a linear,
fourth-order ODE (`Beam bending problem`). The second experiment then verifies a
linear, second-order PDE (`Poisson's equation`). Each experiment can be more easily understood through [Tutorial: Beam-bending](https://github.com/HongsupOH/physics-regularized-bingo/blob/master/Tutorial_Beambending.ipynb) and [Tutorial: Poisson's euqation](https://github.com/HongsupOH/physics-regularized-bingo/blob/master/Tutorial_Poisson.ipynb).

## Implement code with MPI
### Beam bending problem
First, you need to select the hyperparameters at [beam_bending.json](https://github.com/HongsupOH/physics-regularized-bingo/blob/master/experiment_files/beam_bending.json) file in [experiments](https://github.com/HongsupOH/physics-regularized-bingo/tree/master/experiment_files) folder.
Then, you can implement at `Ubuntu` or `Windows terminal`:
```
mpiexec -n <the number of cpu (int)> python soln_tests.py -e <Address of json file>/beam_bending.json
```
Where you need to fill `<>`. For example, it can be 
```
mpiexec -n 10 python soln_tests.py -e /mnt/c/Users/hong/bingo_diffeq_pt/experiment_files/beam_bending.json
```
Then, the progress of the evolution is written at `log file` in [logs](https://github.com/HongsupOH/physics-regularized-bingo/tree/master/logs) folder. The name of log file is `beam_bending_<cpu-rank>`. As the evolution is terminated, the obtained equation is written at the log file. Or you can open `pkl` file in [checkpoints](https://github.com/HongsupOH/physics-regularized-bingo/tree/master/checkpoints) folder to check the evolution process. The name of `pkl` file is `beam_bending_<gen>.pkl`. Then, you need write the name of `pkl` file with address in [OpenPKL.py](https://github.com/HongsupOH/physics-regularized-bingo/blob/master/OpenPKL.py) and implement code
```
python OpenPKL.py
```
then, you can check the obtained equation at the specific generation. 
### Poisson's equation
First, you need to select the hyperparameters at [poisson_simple.json](https://github.com/HongsupOH/physics-regularized-bingo/blob/master/experiment_files/poisson_simple.json) file in [experiments](https://github.com/HongsupOH/physics-regularized-bingo/tree/master/experiment_files) folder.
Then, you can implement at `Ubuntu` or `Windows terminal`:
```
mpiexec -n <the number of cpu (int)> python soln_tests.py -e <Address of json file>/poisson_simple.json
```
Where you need to fill `<>`. For example, it can be 
```
mpiexec -n 10 python soln_tests.py -e /mnt/c/Users/hong/bingo_diffeq_pt/experiment_files/poisson_simple.json
```
Then, the progress of the evolution is written at `log file` in [logs](https://github.com/HongsupOH/physics-regularized-bingo/tree/master/logs) folder. The name of log file is `poisson_simple_<cpu-rank>`. As the evolution is terminated, the obtained equation is written at the log file. Or you can open `pkl` file in [checkpoints](https://github.com/HongsupOH/physics-regularized-bingo/tree/master/checkpoints) folder to check the evolution process. The name of `pkl` file is `poisson_simple_<gen>.pkl`. Then, you need write the name of `pkl` file with address in [OpenPKL.py](https://github.com/HongsupOH/physics-regularized-bingo/blob/master/OpenPKL.py) and implement code
```
python OpenPKL.py
```
then, you can check the obtained equation at the specific generation. 
## Contact
If you have any issue about implementing code, you can contact us!

- Hongsup Oh: hongsup.oh@utah.edu
- Jacob D Hochhalter: jacob.hochhalter@utah.edu

Thanks to visit us!
