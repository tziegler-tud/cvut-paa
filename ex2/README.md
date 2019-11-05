# MIE-PAA
Project files for the course MIE-PAA "Problems and Algorythms" taught at CVUT in winter term 2019/2020

## Excercise 1: Solving the decision knapsack problem exactly
Instructions:
In order to be the homework accepted, these tasks must be accomplished:

Write a program solving the decision version of the 0/1 knapsack problem by
a brute force (i.e., by evaluating all combinations)
the branch & bound method
Perform experimental evaluation using these instances. Observe the dependency of the computational complexity on the instance size.
The computational complexity should be measured by the number of visited nodes in the decision tree (the number of recursion calls), not the run-time. 
There are 500 instances for each instance size. Observe both the average and maximum complexity, as a function of the instance size.
Note: do not try to solve the biggest instances now. For this homework, use instances up the size your computing power allows.
Nice summary tables and graphs will be appreciated.
Process the two instances sets (NR, ZR) separately. What differences do you see?
For at least one instance size, observe the frequency of the measured values (draw a histogram). I.e., there will be the time complexities on the x-axis and their frequency on the y-axis.
Write a report containing the measured dependencies and the source code. Do not insert the sourcecode directly into the report! Just insert a link.

Bonus tasks:
In order to obtain the full number of points (3), some extra work must be done. This could be, e.g.,
CPU time measurement. How does the CPU time correlate with the measured time complexity (i.e., measured by the number of visited states)? Some novel B&B technique, etc.
