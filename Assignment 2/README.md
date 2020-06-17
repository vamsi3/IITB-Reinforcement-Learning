## Programming Assignment 2

In this assignment, you will implement algorithms for finding an optimal policy for a given MDP. The first part of the assignment is to apply <ins>Linear Programming</ins>, based on the formulation presented in class. The second part of the assignment is to implement <ins>Howard's Policy Iteration</ins>. The third part of the assignment requires you to construct MDPs whose optimal policies satisfy a specified condition; you will use your solvers to validate your construction.

### Data

This [directory](resources/data) provides a few samples of input and output that you can use to test your code. The directory contains four MDPs encoded as text files, with each file in the following format.

```
Number of states
Number of actions
Reward function
Transition function
Discount factor
Type
```

In these files, and also in the MDPs on which your algorithms will be tested, the number of states S will be an integer greater than 0 and less than 150. Assume that the states are numbered 0, 1, 2, …, (S - 1). Similarly, actions will be numbered 0, 1, 2, …, (A - 1), where A is less than 100. The reward function will be provided over S×A lines, each line containing S entries. Each entry corresponds to R(s, a, s'), wherein state s, action a, and state s' are being iterated in sequence from 0 to (S - 1), 0 to (A - 1), and 0 to (S - 1), respectively. A similar scheme is adopted for the transition function T. Each reward lies between -1 and 1 (both included). The discount factor is a real number in [0, 1]. However, the discount factor will only be set to 1 if the underlying task is episodic. The last field in the file, denoted Type, will either be "continuing" or "episodic". If episodic, it is our convention that the very last state (numbered S - 1) will be a terminal state. The MDP will be such that for every starting state and policy, trajectories will eventually reach the terminal state.

Below is a snippet of python code that is used to generate MDP files.

```python
print S
print A

for s in range(0, S):
    for a in range(0, A):
        for sPrime in range(0, S):
            print str(R[s][a][sPrime]) + "\t",

        print "\n",

for s in range(0, S):
    for a in range(0, A):
        for sPrime in range(0, S):
            print str(T[s][a][sPrime]) + "\t",

        print "\n",

print gamma
print type
```

### Solution

Given an MDP, your program must compute the optimal value function V* and an optimal policy π* by applying the algorithm that is specified through the command line. Create a shell script called `planner.sh` to invoke your program. The arguments to `planner.sh` will be

- `--mdp` followed by a full path to the input MDP file, and
- `--algorithm` followed by one of `lp` and `hpi`.

Make no assumptions about the location of the MDP file relative to the current working directory; read it in from the full path that will be provided. The algorithms specified above correspond to Linear Programming and Howard's Policy Iteration, respectively. Here are a few examples of how your planner might be invoked (it will always be invoked from its own directory).

- `./planner.sh --mdp /home/user/temp/data/mdp-7.txt --algorithm lp`
- `./planner.sh --mdp /home/user/mdpfiles/mdp-5.txt --algorithm hpi`

You are free to implement the planner in any programming language of your choice. You are not expected to code up a solver for LP; rather, you can use available solvers as blackboxes (more below). Your effort will be in providing the LP solver the appropriate input based on the MDP, and interpreting its output appropriately. You are expected to write your own code for Howard's Policy Iteration; you may not use any custom-built libraries that might be available for the purpose. You can use libraries for solving linear equations in the policy evaluation step, but must write your own code for policy improvement. Recall that Howard's Policy Iteration switches **all** improvable states to some improving action; if there are two or more improving actions at a state, you are free to pick any one.

### Output Format

The output of your planner must be in the following format, and **written to standard output**.

```
V*(0)   π*(0)
V*(1)   π*(1)
.
.
.
V*(S - 1)   π*(S - 1)
```

In the `data` directory provided, you will find four output files corresponding to the MDP files, which have solutions in the format above.

Since your output will be checked automatically, make sure you have nothing printed to `stdout` other than the S lines as above in sequence. If the testing code is unable to parse your output, you will not receive any marks.

**Note:**

1. Your output has to be written to the standard output, not to any file.

2. For values, print at least 6 places after the decimal point. Print more if you'd like, but 6 (`xxx.123456`) will suffice.

3. If your code produces output that resembles the solution files: that is, S lines of the form

   ```
   value + "\t" + action + "\n"
   ```

   or even
   
   ```
value + " " + action + "\n"
   ```

   you should be okay. Make sure you don't print anything else.

4. If there are multiple optimal policies, feel free to print any one of them.

### Effect of Discount Factor on Optimal Policies

This part of the assignment requires you to design a family of MDPs that satisfy a specified property. While coming up with your answer, you can use your own solver to quickly check if you are on the right track.

What you need to construct is a family of MDPs that only differ in their discount factor: that is, they will all have the same set of states, set of actions, transition function, reward function, and type. The family must be such that all MDP instances with a discount factor in [0.01, 0.39]) must have the same (and unique) optimal policy π~1~; all MDP instances with a discount factor in [0.41, 0.74] must have the same (and unique) optimal policy π~2~; all MDP instances with a discount factor in [0.76, 0.99]) must have the same (and unique) optimal policy π~3~; such that π~1~ ≠ π~2~; ≠ π~3~; ≠ π~1~. The MDPs must all be continuing, and have exactly 2 actions. They may have at most 10 states.

Once you have worked out your family, encode it in the same format of the MDPs you have been provided. You only need to provide a single instance, with a discount factor of 0.5; call the instance `mdp-family.txt`. We will create multiple MDP instances that only differ in the discount factor, and run our own code to compute their optimal policies.

### Submission

Place these items in a directory named `submission`.

- `planner.sh` and all the code that it needs to run.
- `mdp-family.txt`.
- `notes.txt` (You can describe your code and MDP construction if you would like us to see, but this item is optional.).
- `references.txt` (See the section on Academic Honesty on the course web page.).

Compress the directory into `submission.tar.gz` and upload on Moodle under Programming Assignment 2.

### Evaluation

Your planner will be tested on a large number of MDPs. Your task is to ensure that it prints out the correct solution (V* and π*) in each case, using each of the algorithms you have been asked to implement. 4 marks each are allotted for the correctness of your Linear Programming and Howard's Policy Iteration algorithms. 2 marks are allotted for the correctness of the MDP family you construct. We shall verify correctness by computing and comparing optimal policies for a large number of MDPs from the family (obtained by varying the discount factor in `mdp-family.txt`).

The TAs and instructor may look at your source code to corroborate the results obtained by your program, and may also call you to a face-to-face session to explain your code.

### Deadline and Rules

Your submission is due by 11.55 p.m., Sunday, September 15. Finish working on your submission well in advance, keeping enough time to test your code and upload to Moodle.

Your submission will not be evaluated (and will be given a score of zero) if it is not uploaded to Moodle by the deadline. Do not send your code to the instructor or TAs through any other channel. Requests to evaluate late submissions will not be entertained.

Your submission will receive a score of zero if your code does not execute on the sl2 machines. To make sure you have uploaded the right version, download it and check after submitting (but before the deadline, so you can handle any contingencies before the deadline lapses). If your code needs any special libraries to run on the sl2 machines, it is **your** responsibility to get them installed. You can do so by [filing a bug](https://bugs.cse.iitb.ac.in/bugs/enter_bug.cgi) with the CSE system administrators.

You are expected to comply with the rules laid out in the "Academic Honesty" section on the course web page, failing which you are liable to be reported for academic malpractice.

### References for Linear Programming

Although you are free to use any library of your choice for LP, we recommend that you use the Python library `PuLP` (https://pythonhosted.org/PuLP/) or the `lp_solve` program (http://lpsolve.sourceforge.net/5.5/). Both of these are already installed on the `sl2` machines.

`PuLP` is convenient to use directly from Python code: here is a [short tutorial](https://www.youtube.com/watch?v=7yZ5xxdkTb8) and here is a [reference](https://www.coin-or.org/PuLP/index.html).

`lp_solve` can be used both through an API and through the command line. Here is a [reference](http://lpsolve.sourceforge.net/5.5/) and here is an [introductory example](http://lpsolve.sourceforge.net/5.5/formulate.htm).