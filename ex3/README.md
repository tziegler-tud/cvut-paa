# MIE-PAA
Project files for the course MIE-PAA "Problems and Algorythms" taught at CVUT in winter term 2019/2020

## Excercise 2: Exact and heuristic solutions of the Knapsack Problem
Instructions:

1. Write a program solving the optimization version of the 0/1 knapsack problem using the simple cost/weight heuristic (see Lecture 4). Observe the run-time and the average and maximum errors, for each instance size.
2. Write a program solving the optimization version of the 0/1 knapsack problem using the modified (extended) cost/weight heuristic (see Lecture 4). Observe the average and maximum error, for each instance size. Compare these errors with the simple heuristic.
3. Write a program solving the optimization version of the 0/1 knapsack problem using dynamic programming. You can choose between the decomposition by the knapsack capacity or total cost. Observe the run-time (as a function of the instance size). Observe the run-time and compare it with the brute force and B&B from the 1st homework, and the simple cost/weight heuristic.
4. Write a program solving the 0/1 knapsack problem using an FPTAS approximation algorithm. Observe the dependency of the algorithm run-time and the relative error (maximum, average) on the chosen precision, for a selected instances size (40 or all instance sizes is suggested). The FPTAS algorithm can be obtained by modifying the dynamic programming algorithm based on decomposition by the total cost. Decomposition by the knapsack capacity cannot be used here (!) since the FPTAS property cannot be guaranteed.
	- Hint: there are instances, in which there are items with a higher weight than the knapsack capacity. These must be excluded from the total cost computation (i.e., excluded at the beginning of the algorithm). Otherwise, the cost division factor may immensely grow, and so the error.
