# Content

This readme include my notes for problems in urban transportation, network problems, simulation, numerical optimization, and integer programming. Besides, my projects and algorithms implementation for some topics are also introduced.

Without implementation, knowledge is only knowledge while not ability. In the future, the author will try to use them solve some realistic problems. If you have any question want to chat with me or ask me, please contact: tjyangshan@gmail.com 

## Introduction

- [Urban Transportation](#urban-transportation)
  * [BPR Function](#bpr-function)
  * [User Euqilibrium](#user-euqilibrium)
    + [Mathematical Model](#mathematical-model)
    + [Heuristic method](#heuristic-method)
  * [Beckmann's Transformation](#beckmann-s-transformation)
  * [Frank-Wolfe Algorithm](#frank-wolfe-algorithm)
  * [System Optimum](#system-optimum)
    + [Model Introduction](#model-introduction)
    + [Price of Anarchy](#price-of-anarchy)
  * [Network Loading Models](#network-loading-models)
    + [Why investigate?](#why-investigate-)
    + [Choice Function](#choice-function)
    + [Logit-Based Loading Models](#logit-based-loading-models)
  * [Traffic bottleneck](#traffic-bottleneck)
    + [Stationary bottleneck](#stationary-bottleneck)
    + [Moving bottleneck](#moving-bottleneck)
- [Network Problem](#network-problem)
  * [Shortest Path Problem](#shortest-path-problem)
  * [Graph Algorithm](#graph-algorithm)
  * [Max-Flow Problem](#max-flow-problem)
    + [Ford-Fulkerson](#ford-fulkerson)
    + [Capacity Scaling Algorithm](#capacity-scaling-algorithm)
    + [Preflow Push Algorithm](#preflow-push-algorithm)
    + [Application](#application)
  * [Minimum Cost Flow](#minimum-cost-flow)
    + [Cycle canceling algorithm](#cycle-canceling-algorithm)
    + [Successive shortest path algorithm](#successive-shortest-path-algorithm)
    + [Application-Assignment](#application-assignment)
    + [Application-Schedule](#application-schedule)
- [Optimization Problem](#optimization-problem)
  * [Unconstrained Optimization](#unconstrained-optimization)
  * [Line Search Methods](#line-search-methods)
    + [Introduction to Line Search](#introduction-to-line-search)
    + [Steppest Direction](#steppest-direction)
    + [Newton Direction](#newton-direction)
  * [Scaling](#scaling)
  * [Trust Region](#trust-region)
  * [Quasi-Newton's Method](#quasi-newton-s-method)
  * [KKT Condition](#kkt-condition)
  * [Others](#others)
- [Integer Programming](#integer-programming)
  * [Algorithms](#algorithms)
  * [Branch and Bound](#branch-and-bound)
  * [Branch and Cut](#branch-and-cut)
  * [Column Generation](#column-generation)
  * [Bender Decomposition](#bender-decomposition)
  * [DW Decomposition](#dw-decomposition)
  * [Lagrangean Decomposition](#lagrangean-decomposition)
- [Reinforcement&Online Learning](#reinforcement-online-learning)

## Project and Algorithms

- Network-Loading Project: A project solving the 
- User Equilibrium Project:
- Network Algorithms: 
- Integer Programming Algorithms: 
- Travel Demand Prediction Project: 

# Urban Transportation 

This part contains some problems introduced in *Sheffi Y. Urban transportation networks[M]. Prentice-Hall, Englewood Cliffs, NJ, 1985* , wiki, and operation research

## BPR Function

Suppose we are considering a highway network. For each link there is a function stating the relationship between resistance and volume of traffic. The Bureau of Public Roads (BPR) developed a link (arc) congestion (or volume-delay, or link performance) function.

![1fe844a61968160ba88c7e2c8dc2e33a55094d16](img/1fe844a61968160ba88c7e2c8dc2e33a55094d16.svg)

$t_a$ = free-flow travel time on link a per unit of time

$Q_a$ = flow (or volume) of traffic on link a per unit of time (somewhat more accurately: flow attempting to use link a)

$c_a$ = capacity of link a per unit of time

$S_a(Q_a)$ is the average travel time for a vehicle on link a

## User Euqilibrium

**In brief, A network is in user equilibrium (UE) when every driver chooses the routes in its lowest cost between origin and destination regardless whether total system cost is minimized.**

The user optimum equilibrium assumes that all users choose their own route towards their destination based on the travel time that will be consumed in different route options. The users will choose the route which requires the least travel time. The user optimum model is often used in simulating the impact on traffic assignment by highway bottlenecks. When the congestion occurs on highway, it will extend the delay time in travelling through the highway and create a longer travel time. Under the user optimum assumption, the users would choose to wait until the travel time using a certain freeway is equal to the travel time using city streets, and hence equilibrium is reached. This equilibrium is called User Equilibrium, Wardrop Equilibrium or Nash Equilibrium.

[![img](https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/User_equilibrium_traffic_model.jpg/400px-User_equilibrium_traffic_model.jpg)](https://en.wikipedia.org/wiki/File:User_equilibrium_traffic_model.jpg)

The core principle of User Equilibrium is that all used routes between a given OD pair have the same travel time. An alternative route option is enabled to use when the actual travel time in the system has reached the free-flow travel time on that route.

For a highway user optimum model considering one alternative route, a typical process of traffic assignment is shown in figure 15. When the traffic demand stays below the highway capacity, the delay time on highway stays zero. When the traffic demand exceeds the capacity, the queue of vehicle will appear on the highway and the delay time will increase. Some of users will turn to the city streets when the delay time reaches the difference between the free-flow travel time on highway and the free-flow travel time on city streets. It indicates that the users staying on the highway will spend as much travel time as the ones who turn to the city streets. At this stage, the travel time on both the highway and the alternative route stays the same. This situation may be ended when the demand falls below the road capacity, that is the travel time on highway begins to decrease and all the users will stay on the highway. The total of part area 1 and 3 represents the benefits by providing an alternative route. The total of area 4 and area 2 shows the total delay cost in the system, in which area 4 is the total delay occurs on the highway and area 2 is the extra delay by shifting traffic to city streets.

Navigation function in Google Maps can be referred as a typical industrial application of dynamic traffic assignment based on User Equilibrium since it provides every user the routing option in lowest cost (travel time).

### Mathematical Model

Passengers can not choose another route to lower their cost.

<img src="img/image-20201128200610675.png" alt="image-20201128200610675" width="700" align="center" />

<img src="img/image-20201128203845278.png" alt="image-20201128203845278" width="700" align="center" />

<img src="img/image-20201122134743994.png" alt="image-20201122134743994" width="500" align="center" />

<img src="img/1000px-EquilibriumAssignment3.png" alt="1000px-EquilibriumAssignment3" width="600" align="center" />

### Heuristic method

1. All or Nothing

2. Incremental Assignment

## Beckmann's Transformation

Beckmann's transformation can convert the euqilibrium into a convex problem

<img src="img/image-20201122134920754.png" alt="image-20201122134920754" width="600" align="center" />

## Frank-Wolfe Algorithm

Dafermos (1968) applied the [Frank-Wolfe algorithm](https://en.wikipedia.org/wiki/Frank-Wolfe_algorithm) (1956, Florian 1976), which can be used to deal with the traffic equilibrium problem. 

<img src="img/Frank-Wolfe_Algorithm.png" alt="img"  width="500" align="center" />

## System Optimum

**In short, a network is in system optimum (SO) when the total system cost is the minimum among all possible assignments.**

System Optimum is based on the assumption that routes of all vehicles would be controlled by the system, and that rerouting would be based on maximum utilization of resources and minimum total system cost. (Cost can be interpreted as travel time.) Hence, in a System Optimum routing algorithm, all routes between a given OD pair have the same marginal cost. In traditional transportation economics, System Optimum is determined by equilibrium of demand function and marginal cost function. In this approach, marginal cost is roughly depicted as increasing function in traffic congestion. In traffic flow approach, the marginal cost of the trip can be expressed as sum of the cost(delay time, w) experienced by the driver and the externality(e) that a driver imposes on the rest of the users.

Suppose there is a freeway(0) and an alternative route(1), which users can be diverted onto off-ramp. Operator knows total arrival rate(A(t)), the capacity of the freeway(μ_0), and the capacity of the alternative route(μ_1). From the time $t_0$, when freeway is congested, some of the users start moving to alternative route. However, when $t_1$, alternative route is also full of capacity. Now operator decides the number of vehicles(N), which use alternative route. The optimal number of vehicles(N) can be obtained by calculus of variation, to make marginal cost of each route equal. Thus, optimal condition is $T_0=T_1+∆_1$. In this graph, we can see that the queue on the alternative route should clear $∆_1$ time units before it clears from the freeway. This solution does not define how we should allocates vehicles arriving between $t_1$ and $T_1$, we just can conclude that the optimal solution is not unique. If operator wants freeway not to be congested, operator can impose the congestion toll, $e_0-e_1$, which is the difference between the externality of freeway and alternative route. In this situation, freeway will maintain free flow speed, however alternative route will be extremely congested.

### Model Introduction

The system condition should meet the following：

<img src="img/image-20201128034804725.png" alt="image-20201128034804725" width="300" align="center" />

The KKT conditions of the SO problem:

<img src="img/image-20201128034709559.png" alt="image-20201128034709559" width="500" align="center" />

It is a simple problem to solve compared with the user euqilibrium.

### Price of Anarchy

The reason we have congestion is that people are selfish. The cost of that selfishness (when people behave according to their own interest rather than society's) is the price of anarchy*.

The ratio of system-wide travel time under User Equilibrium and System Optimal conditions.

For a two-link network with linear link performance functions (latency functions), Price of Anarchy is < 4/3.

## Network Loading Models

*Review is required*

### Why investigate?

When there are serval choice for passengers, different ways will afford different demands. For example, if from point A to point B people can choose subway or taxi, different people will choose different ways. As a result, different approches will afford different loading.

### Choice Function

Let $U = (U_1, ... , U_K)$ denote the vector of utilities associated with a given set of alternatives, $K$. This set includes K alternative snumbered 1, 2, ... , *K.* The utility of each alternative to a specific decision maker can be expressed as a function of the observed attributes of the alternatives and the observed characteristics of this decision maker. Let **a** denote the vector of variables which include these characteristics and attributes. Thus $U_k = U_k(a)$. To incorporate the effects of unobserved attributes and characteristics, the utility of each alternative is expressed as a random variable consisting of a systematic (deterministic) component, $V_k(a)$,and an additive random "error term", **k(a),**that is, 
$$
U_k(a) = V_k(a)+\xi_k(a)\;\forall k \in K
$$



The random component of the utility satisfies $E[\xi_k(a)]= 0$, meaning that $E[U_k(a)] = V_k(a)$.In this context, Uk(a) is sometimes referred to as the "per- ceived utility" and $V_k(a)$ as the "measured utility."

The choice probability is then the probability that $U_k(a)$ is higher than the utility of any other alternative and 
$$
P_k(s) = Pr[I_k(a)\geq U_l(a), \forall l \in K] \;\;\; \forall k \in K
$$


### Logit-Based Loading Models 

This logit modl is similar to the softmax model.

<img src="img/image-20201201154032854.png" alt="image-20201201154032854" width="200px" />

Project based on this model: [network-loading-model](network-loading-model)

## Traffic bottleneck

Traffic bottlenecks are disruptions of traffic on a roadway caused either due to road design, traffic lights, or accidents. There are two general types of bottlenecks, stationary and moving bottlenecks. Stationary bottlenecks are those that arise due to a disturbance that occurs due to a stationary situation like narrowing of a roadway, an accident. Moving bottlenecks on the other hand are those vehicles or vehicle behavior that causes the disruption in the vehicles which are upstream of the vehicle. Generally, moving bottlenecks are caused by heavy trucks as they are slow moving vehicles with less acceleration and also may make lane changes.

[![img](https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Percentage_split_of_causes_of_Traffic_Congestion.png/350px-Percentage_split_of_causes_of_Traffic_Congestion.png)](https://en.wikipedia.org/wiki/File:Percentage_split_of_causes_of_Traffic_Congestion.png)

Bottlenecks are important considerations because they impact the flow in traffic, the average speeds of the vehicles. The main consequence of a bottleneck is an immediate reduction in capacity of the roadway. The Federal Highway Authority has stated that 40% of all congestion is from bottlenecks figure 16 shows the pie-chart for various causes of congestion. Figure 17 shows the common causes of congestion or bottlenecks.

### Stationary bottleneck

The general cause of stationary bottlenecks are lane drops which occurs when the a multilane roadway loses one or more its lane. This causes the vehicular traffic in the ending lanes to merge onto the other lanes.

[![img](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Wikipedia_TrafficBottlenecks_regular.svg/350px-Wikipedia_TrafficBottlenecks_regular.svg.png)](https://en.wikipedia.org/wiki/File:Wikipedia_TrafficBottlenecks_regular.svg)

Consider a stretch of highway with two lanes in one direction. Suppose that the fundamental diagram is modeled as shown here. The highway has a peak capacity of Q vehicles per hour, corresponding to a density of kc vehicles per mile. The highway normally becomes jammed at kj vehicles per mile.

Before capacity is reached, traffic may flow at A vehicles per hour, or a higher B vehicles per hour. In either case, the speed of vehicles is vf, or "free flow," because the roadway is under capacity.

Now, suppose that at a certain location x0, the highway narrows to one lane. The maximum capacity is now limited to D', or half of Q, since only one lane of the two is available. D shares the same flowrate as state D', but its vehicular density is higher.

[![img](https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Wikipedia_TrafficBottlenecks_regular_tsd.svg/350px-Wikipedia_TrafficBottlenecks_regular_tsd.svg.png)](https://en.wikipedia.org/wiki/File:Wikipedia_TrafficBottlenecks_regular_tsd.svg)

Using a time-space diagram, we may model the bottleneck event. Suppose that at time 0, traffic begins to flow at rate B and speed vf. After time t1, vehicles arrive at the lower flowrate A.

Before the first vehicles reach location x0, the traffic flow is unimpeded. However, downstream of x0, the roadway narrows, reducing the capacity by half – and to below that of state B. Due to this, vehicles will begin queuing upstream of x0. This is represented by high-density state D. The vehicle speed in this state is the slower vd, as taken from the fundamental diagram. Downstream of the bottleneck, vehicles transition to state D', where they again travel at free-flow speed vf.

Once vehicles arrive at rate A starting at t1, the queue will begin to clear and eventually dissipate. State A has a flowrate below the one-lane capacity of states D and D'.

On the time-space diagram, a sample vehicle trajectory is represented with a dotted arrow line. The diagram can readily represent vehicular delay and queue length. It is a simple matter of taking horizontal and vertical measurements within the region of state D.

### Moving bottleneck

As explained above, moving bottlenecks are caused due to slow moving vehicles that cause disruption in traffic. Moving bottlenecks can be active or inactive bottlenecks. If the reduced capacity(qu) caused due to a moving bottleneck is greater than the actual capacity(μ) downstream of the vehicle, then this bottleneck is said to be an active bottleneck. Figure 20 shows the case of a truck moving with velocity 'v' approaching a downstream location with capacity 'μ'. If the reduced capacity of the truck (qu) is less than the downstream capacity, then the truck becomes an inactive bottleneck.

[![img](https://upload.wikimedia.org/wikipedia/commons/6/66/Active_Inactive_Moving_Bottleneck1.PNG)](https://en.wikipedia.org/wiki/File:Active_Inactive_Moving_Bottleneck1.PNG)

Laval 2009, presents a framework for estimating analytical expressions for the capacity reductions caused by a subset of vehicles forced to slow down at horizontal/vertical curves on multilane freeway. In each of the lane the underperforming stream is described in terms of its desired speed distribution and is modeled as per Newell’s kinematic wave theory for moving bottlenecks. Lane changing in the presence of trucks can lead to a positive or negative impact on capacity. If the target lane is empty then the lane-changing increases capacity

For this example, consider three lanes of traffic in one direction. Assume that a truck starts traveling at speed v, slower than the free flow speed vf. As shown on the fundamental diagram below, qu represents the reduced capacity (2/3 of Q, or 2 of 3 lanes available) around the truck.

State A represents normal approaching traffic flow, again at speed vf. State U, with flowrate qu, corresponds to the queuing upstream of the truck. On the fundamental diagram, vehicle speed vu is slower than vf. But once drivers have navigated around the truck, they can again speed up and transition to downstream state D. While this state travels at free flow, the vehicle density is less because fewer vehicles get around the bottleneck.

[![img](https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Wikipedia_TrafficBottlenecks_moving1.svg/350px-Wikipedia_TrafficBottlenecks_moving1.svg.png)](https://en.wikipedia.org/wiki/File:Wikipedia_TrafficBottlenecks_moving1.svg)

Suppose that, at time t, the truck slows from free-flow to v. A queue builds behind the truck, represented by state U. Within the region of state U, vehicles drive slower as indicated by the sample trajectory. Because state U limits to a smaller flow than state A, the queue will back up behind the truck and eventually crowd out the entire highway (slope s is negative). If state U had the higher flow, there would still be a growing queue. However, it would not back up because the slope s would be positive.

[![img](https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Wikipedia_TrafficBottlenecks_moving1_tsd.svg/350px-Wikipedia_TrafficBottlenecks_moving1_tsd.svg.png)](https://en.wikipedia.org/wiki/File:Wikipedia_TrafficBottlenecks_moving1_tsd.svg)

# Network Problem

## Shortest Path Problem

Refer to my another repository: https://github.com/seanys/Data-Structure-Algoirthm-Tongji-SEM

## Graph Algorithm

Refer to my another repository: https://github.com/seanys/Data-Structure-Algoirthm-Tongji-SEM

## Max-Flow Problem

### Ford-Fulkerson

Only can handle network that capacity is rational. Just find augument path iteratively.

<img src="img/image-20201130215025556.png" alt="image-20201130215025556" width ="600px" />

### Capacity Scaling Algorithm

Similar to ford-fulkerson.

<img src="img/image-20201130215311730.png" alt="image-20201130215311730" width="600px" />

### Preflow Push Algorithm



<img src="img/image-20201130215615845.png" alt="image-20201130215615845" width="600px" />

### Application

The same as shortest path problem, many issues can be converted to max-flow problem.

<img src="img/image-20201201011059155.png" alt="image-20201201011059155" width="600px" />

<img src="img/image-20201201011150282.png" alt="image-20201201011150282" width="600px" />

## Minimum Cost Flow

### Cycle canceling algorithm 

<img src="img/image-20201201011927115.png" alt="image-20201201011927115" width="400px" />

<img src="img/image-20201201012158423.png" alt="image-20201201012158423" width="500px" />

### Successive shortest path algorithm 

Need review.

<img src="img/image-20201201022715681.png" alt="image-20201201022715681" width="600px" />

<img src="img/image-20201201022737324.png" alt="image-20201201022737324" width="600px" />

### Application-Assignment

<img src="img/image-20201201011409080.png" alt="image-20201201011409080" width="600px" />

<img src="img/image-20201201011531758.png" alt="image-20201201011531758" width="600px" />

### Application-Schedule

<img src="img/image-20201201011641321.png" alt="image-20201201011641321" width="600px" />

<img src="img/image-20201201011729314.png" alt="image-20201201011729314" width="500px" />

# Optimization Problem

This part contains some issues introduced in *Nocedal J, Wright S. Numerical optimization[M]. Springer Science & Business Media, 2006* and *Boyd S, Boyd S P, Vandenberghe L. Convex optimization[M]. Cambridge university press, 2004*.

## Unconstrained Optimization

**First Oder Necessary Conditions**: If $x^*$ is a local minimizer and $f$ is continuously differentiable in an open neighborhood of $x^*$, then $\nabla  f(x^∗)=0$ .

**Second Oder Necessary Conditions**: If $x^*$ is a local minimizer of $f$ and $\nabla^2f$ exists and is continuous in an open neighborhood of $x^∗$, then $\nabla f(x^*) = 0$ and $\nabla f(x^*)$ is positive semidefinite.

**Second Order Sufficient Conditions**: Suppose that $\nabla^2 f$ is continuous in an open neighborhood of $x^*$ and that $\nabla f(x^*)=0$ and $\nabla^2 f(x^*)$ is positive definite. Then $x^*$ is a strict local minimizer of $f$.

**Second-Order Sufficient Conditions**: Suppose that $\nabla^2 f$ is continuous in an open neighborhood of  $x^*$ and that $\nabla f(x^*)  = 0$ and $\nabla^2 f$ is positive definite. Then $x^*$ is a strict local minimizer of $f$.

These four theorems introduce how to obtain the local optimal of a function $f$. Moreover, if $f$ if convex, any local minimizer $x^*$ is a global minimizer. If $f$ is differentiable, then any stationary point $x^*$ is a global minimizer.

## Line Search Methods 

### Introduction to Line Search

Algorithms Application: [User-Equilibrium-Project&Line-Search](User-Equilibrium-Project&Line-Search)

In the *line search* strategy, the algorithm chooses a direction $p_k$ and searches along this direction from the current iterate $x_k$ for a new iterate with a lower function value. The distance to move along $p_k$ can be found by approximately solving the following one- dimensional minimization problem to find a step length α: 

<img src="img/image-20201128034037517.png" alt="image-20201128034037517" width="150" align="center" />

We would derive the maximum benefit from the direction $p_k$ , but an exact minimization may be expensive and is usually unnecessary. Instead, the line search algorithm generates a limited number of trial step lengths until it finds one that loosely approximates the minimum of  this objective. At the new point, a new search direction and step length are computed, and the process is repeated. 

### Steppest Direction

<img src="img/image-20201128175350622.png" alt="image-20201128175350622" width="200" align="center" />

<img src="img/image-20201128175415159.png" alt="image-20201128175415159" width="500" align="center" />


### Newton Direction

<img src="img/image-20201128175312612.png" alt="image-20201128175312612" width="400" align="center"/>

<img src="img/image-20201128175654739.png" alt="image-20201128175654739" width="200" align="center" />

The Newton direction can be used in a line search method when $\nabla^2 f_k$ is positive definite, for in this case we have:

<img src="img/image-20201128175850712.png" alt="image-20201128175850712" width="350" align="center" />

Unlike the steepest descent direction, there is a “natural” step length of 1 associated with the Newton direction. Most line search implementations of Newton’s method use the unit step $\alpha = 1$  where possible and adjust α only when it does not produce a satisfactory reduction in the value of *f* . 

中文参考资料：https://zhuanlan.zhihu.com/p/33544363

## Scaling

<img src="img/image-20201128193724922.png" alt="image-20201128193724922" width="500" align="center" />

## Trust Region

Line search starts by fixing the direction $p_k$ and then identifying an appropriate distance, namely the step length $α_k$ . In trust region, we first choose a maximum distance—the trust-region radius $\Delta k$ —and then seek a direction and step that attain the best improvement possible subject to this distance constraint. If this step proves to be unsatisfactory, we reduce the distance measure $\Delta k$ and try again. 

<img src="img/image-20201128033854279.png" alt="image-20201128033854279" width="700" align="center" />

## Quasi-Newton's Method

*Quasi-Newton* search directions provide an attractive alternative to Newton’s method in that they do not require computation of the Hessian and yet still attain a superlinear rate of convergence.  In place of the true Hessian $\nabla^2 f_k$, they use an approximation $B_k$, which is updated after each step to take account of the additional knowledge gained during the step. 

<img src="img/image-20201128180845670.png" alt="image-20201128180845670" width="300" align="center" />

<img src="img/image-20201128181112829.png" alt="image-20201128181112829" width="400" align="center" />

This is the BFGS update. One can show that BFGS update generates positive definite approximations whenever the initial approximation $B_0$ is positive definite and $s_k^T y_k$ > 0.

The quasi-Newton search direction is:

<img src="img/image-20201128181238814.png" alt="image-20201128181238814" width="180" align="center" />



## KKT Condition

<img src="img/image-20201205212157819.png" alt="image-20201205212157819" width="600px" />

## Others

- No-linear eqution
- Least-Square Problem

# Integer Programming

In carsharing system, there many problems whose solutions are discrete such as scheduling and dispatching problem. Most of them are NP-hard. In general, heruistic algorithms for integer programming are efficient approaches to handle them. 

## Algorithms

- Branch and Bound
- Branch and Cut
- Branch and Price
- Lagrangian Decompsoition
- Column Generation
- DW Decomposition
- Bender Decomposition

## Branch and Bound

Branch and bound (BB, B&B, or BnB) is an algorithm design paradigm for discrete and combinatorial optimization problems, as well as mathematical optimization. A branch-and-bound algorithm consists of a systematic enumeration of candidate solutions by means of state space search: the set of candidate solutions is thought of as forming a rooted tree with the full set at the root. The algorithm explores branches of this tree, which represent subsets of the solution set. Before enumerating the candidate solutions of a branch, the branch is checked against upper and lower estimated bounds on the optimal solution, and is discarded if it cannot produce a better solution than the best one found so far by the algorithm.

![Branch and Bound Algorithm - GeeksforGeeks](img/knapsack3.png)

## Branch and Cut

Branch and cut is a method of combinatorial optimization for solving integer linear programs (ILPs), that is, linear programming (LP) problems where some or all the unknowns are restricted to integer values. Branch and cut involves running a branch and bound algorithm and using cutting planes to tighten the linear programming relaxations. Note that if cuts are only used to tighten the initial LP relaxation, the algorithm is called cut and branch.

![img](img/v2-2372587f8bf772f69318d37b5f9deae8_1440w.png)

## Column Generation

Reference: https://zhuanlan.zhihu.com/p/118516953

Code: [column generation.py](Integer-Programming-Algorithms/column_generation.py)

![img](https://pic4.zhimg.com/80/v2-e5eeaea4759c95762e6eb1ec51e33333_1440w.jpg)

![img](https://pic1.zhimg.com/80/v2-afccbdfef727a4e6ac72000a763d4cdc_1440w.jpg)

![img](https://pic4.zhimg.com/80/v2-80d0c573404e673648b8d0d2dcd4803b_1440w.jpg)

![img](https://pic1.zhimg.com/80/v2-7707a3c3a610d07106c4a22fcd8dd8e8_1440w.jpg)

![img](https://pic4.zhimg.com/80/v2-c03295ab9a1df004ef9d5f469416954b_1440w.jpg)

## Bender Decomposition

Code: [bender decomposition.py](Integer-Programming-Algorithms/bender_decomposition.py)

**Bender Decomposition is a algorithm for MIP problem.**

1. Problem can be formulated to have only one continous var with a lot more constraints
2. Because only a small number of constraints are useful, we can drop most of them.

**Procedure**

1. Start with a relaxed BMP with no constraints or just a few, sovle to optimal
2. We also have an upper bound Zub
3. Solve the dual problem to get u, it may be 
   1. Infeasible(Dual Unbounded), generate v to find violated feasibility cut
   2. has a solution, add u related optimality cut, we has a lower bound

<img src="img/bender_img.png" alt="在这里插入图片描述" width="500px" />

<img src="img/image-20200610113002827.png" alt="image-20200610113002827" height="500px" />

<img src="img/image-20200610113040574.png" alt="image-20200610113040574" height="340px" />

<img src="img/image-20200610194807165.png" alt="image-20200610194807165" height="400px" />

## DW Decomposition

Code: [dw decomposition.py](Integer-Programming-Algorithms/dw_decomposition.py)

![在这里插入图片描述](img/dw_decomposition.png)

It is a approache similar to column generation.

## Lagrangean Decomposition

![image-20201205144143258](img/image-20201205144143258.png)

http://egon.cheme.cmu.edu/ewo/docs/EWOLagrangeanGrossmann.pdf

# Reinforcement&Online Learning

RL has been applied to many NP-hard scenarios such as travel salesman problem and convex hull problem. In many problem with less 

Online learning is similar to reinfocment learning and has more implementation scenarios. Many problems shall be solved on time and the decision will changed with the development of the environment.

These two tools will be important to pobelms in carsharing and ridesharing in the future.

# 高等数学与线性代数

## 泰勒与拉格朗日展开



## 多元二阶泰勒展开

证明过程中文版：多元函数的泰勒展开式 -  https://zhuanlan.zhihu.com/p/33316479

![img](img/v2-84f1ca33aaebdaae45dd570d3d9b6cef_1440w.png)

## 拉普拉斯展开





## 统计学

