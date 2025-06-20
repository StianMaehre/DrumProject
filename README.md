# DrumProject

## Background
Can you hear the shape of a drum? An interesting question which actucally gives a lot of insight to wave dynamic on different domain. This project aims to solve the necessary equation and thereby show visually that you indeed can hear the shape.

The equation govering the modes and eigenvalues of a drum is Helmholtz equation, here written in terms of eigenfrequency $\omega$:
![Helmholtz](.\figures\Helmholtz.png)


This can be solved numerically by using finite difference method. The discretized version of the equation is: 
![Discrete](.\figures\dicrete.png)

Which can be rewritten to matrix form:
$\\ \textbf{A}U=\lambda U $

Then the main task is to find the A matrix with our boundary conditions and then solve the eigenvalue problem. The eigenvectors is then the modes of the vibrating drum on the domain.

To analyze if the eigenfrequency of a drum depend on the shape, we want to change the shape without changing the area of the domain. A simple way to do this is to take all the straight line, divide it into 4 equal parts and then raise one part and another equally. If that is done on the 4 sides of a square, the area is preserved, but the shape is different. This can be reapeated to desired level. This is then used to decide the boundary conditions for the A matrix. 

## Numerical steps in the project
1. Generate koch square to desired level
2. Make the A matrix with given koch square as boundary condition
3. Solve the eigenvalue problem
4. Plot the results

## How to run the project
This is the way to run the product:
1. Be sure to be in right directory
2. run python main.py. 

Without any arguments, the project will initialize, solve, save the raw data, plot and save the plots for a koch square with level 3.

To solve for a system with a koch square on another level, the user can add "--level int". Note as higher level needs more points, it will take longer to run. A level higher than 4 is not recommended.

There is a possibility for the user to choose which action to do by adding the arument "--action string", with 3 different options:
1. "initializeAndSolve", this will initialize and solve the system for the given level.
2. "plot", this will plot and save the plots, IF the system is already solved and the raw data is saved.
3. "all", which initialize, solve, save the raw data, plot and saves the plots for the given level. This is set to be default

## Structure of project
The project consits of 5 python files
1. $\verb|main.py|$ is where the aruments is taken and the different functions is called.
2. $\verb|initialize.py|$ generates the koch fractals for the given level and uses this to generate the A matrix.
3. $\verb|solving.py|$ solves the eigenvalue problem.
4. $\verb|filehandling.py|$ has funtions to save and read the raw data.
5. $\verb|plotting.py|$ plots the modes and the domain.
6. $\verb|testing.py|$ testes the program.
7. $\verb|config.py|$ contains values that should not be easily changed. Change them at your own risk.

## Reference

Based on:
[V. P. Simonsen, N. Hale, I. Simonsen, *Am. J. Phys.* **92**, 115 (2024)](https://doi.org/10.1119/5.0140853)  
Free access: [arXiv:2309.13613](https://arxiv.org/abs/2309.13613)