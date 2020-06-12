# ToCFinalProject
Coalition formation solver via reduction to SMT


# Introduction
Coalition formation for task allocation is the problem of assigning teams of agents to tasks such that the overall utility of the tasks completed is maximized. This project focuses on the decision problem (i.e., is the sum of utilities at least k?). The full details of the coalition formation for task allocation problem and its reduction to SMT can be found in writeup.pdf. This project was developed for Oregon State University's Theory of Computation course.

# Getting Started

You will need to install a recent version of Python, pySMT, and MathSAT.

To run a single decision problem, use the following command:

```
python solver.py [inFile] [outFile]
```
The input format is:

```
k

task1 utility resource1 ... resourceC
...
taskM utility resource1 ... resourceC

robot1 resource1 ... resourceC
...
robotN resource1 ... resourceC
```

An example of the input format can be seen in sampleInput.txt. The output file will contain an assignment of agents to tasks that satisfies the decision problem (if such an assignment exists) and the utility of the assignment.

# Running Experiments

Example code for running experiments can be found in experimentScript.py. 

To run a batch of experiments, use the following command:

```
python solver.py -e [inFolder] [outFile]
```

The output folder contains the name of each input problem file, the time that was required to find a solution, and the utility of the solution found.

An example of how to generate input problems can be found in problemGenerator.py. This method of problem generation is described in writeup.pdf.
