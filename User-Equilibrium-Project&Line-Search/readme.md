# Traffic Assignment Project

Since user equilibrium and system optimum have been introduced, this folder mainly concerns about the exact line search algorithm for solving user equilibrium.  

Besides , a course project in *Network Optimization and Modelling* lectured by Dr. Wang Xiaolei and a paper prospoed Dr. Wang will be showed. [A Convex Programming Approach for Ridesharing User Equilibrium Under Fixed Driver/Rider Demand](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3589442).

- [Line Search](#line-search)
- [Paper Introduction](#paper-introduction)
- [Course Project](#course-project)

## Line Search

### Introduction

https://www.cnblogs.com/jeromeblog/p/3801025.html

<img src="img/211446115822646.png" alt="img" width="500px" />

In general gradient method, we should find a search direction meet the following requirement: 

<img src="img/image-20201204190418293.png" width="300px" />

When $d_k = -\nabla f(x)$, f(x) will decrease most quickly. However, this is not the necessary condition for searching the optimum. All directions that meet $\nabla f(x_k)^Td_k<0$ is fine. In general, the search direction is presented:

<img src="img/image-20201204193341275.png" alt="image-20201204193341275" width="200px" />

$B_k$ is positive definite matrix.

- Fast gradient descent: $B_k=I$  
- Newton Method: $B_k = H(x_k)^(-1)$ and $H(x_k)=\nabla^2f(x_k)$ is positive definite matrix

However, determine the step size is also a important problem. Neither too small nor too big will make convergence a hard thing. So, many line search algorithms are proposed

<img src="img/211449112394066.png" alt="img" width="700px" />

### Example-Backtracking

Source Code: [Backtracking](line-search.py)

First of all, the armijo condition is a very useful method to find the range of stepsize.

<img src="img/211450267074821.png" alt="img" width="500px" />

<img src="img/211451239894421.png" alt="img" width="500px" />

Use backtracking to find the exact stepsize is very efficient way. For example, the left plot is $f(x) = e^x - 2*x$ and the right plot is the process find the optimum position from x = -5.

<img src="img/image-20201204230958077.png" alt="image-20201204230958077" width="700px" />

```
# Iteration Process
x [-5.000000, -3.006738, -1.056191, 0.596031, 0.781130, 0.689161, 0.697118, 0.693139, 0.693147]
f(x) [10.006738, 6.062929, 2.460159, 0.622839, 0.621679, 0.613722, 0.613721, 0.613706, 0.613706]
f(x)' [-1.993262, -1.950547, -1.652222, -0.185098, 0.183938, -0.007957, 0.007957, -0.000016, -0.000000]
```

### Other algorithm

Source Code: [Line Search.py](line_search.py)

- Wolf Search
- Newtons Method
- Quasi-Newton Method
- ......

They will be added to this readme.

## Solve User Equilibrium

After the beckmann transformation, it is easy to solve the UE problem with frank wolf algorithm.

<img src="/Users/sean/Documents/image-20201205001842403.png" alt="image-20201205001842403" width="600px" />

## Course Project

### Requirments

[Traffic Assignment-Course Project](Traffic Assignment-Course Project.pdf)

![image-20201204154550373](img/image-20201204154550373.png)

### Solution

Editing....