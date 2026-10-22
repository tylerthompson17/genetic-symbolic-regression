Genetic Programming - Homework 2

## Overview

Given a dataset of independent and dependent variables, can we use symbolic regression to recover the mystery function that three different datasets contain.


*Dataset 1* consists of 25,000 points, each containing an x value, and an f(x) value obtained by evaluating the mystery function at each x point. 
*Dataset 2* also consists of 25,000 points. Each points consists of x1, x2, and x3 values, as well as an f(x1, x2, x3) function that correspond to the three x's. Both dataset1 and dataset2's formula can be achieved by a combination of +, -, /, and * operators. 
*Dataset 3* also consists of a similar number of point. Each point constsists of an x value and an f(x) value. The formula for dataset3 can be achieved by a combiation of +, -, /, *, and sin, cos, log, and exp.

## How it works

*Formulas are trees.* Every formula is stored as a tree in `tree.py`. Operators (+, -, *, /) sit at the inner nodes and the leaves are either a variable (x, or x1, x2, x3) or a constant. For example, (x - 4) * x is a `*` node with the subtrees (x - 4) and x. `evaluate` computes a tree on all the x values at once with numpy. Division is protected: a denominator smaller than 0.000000001 becomes 1. For dataset3, sin, cos, exp, and log are added as one-child nodes. exp is capped at an input of 50, and log takes the absolute value of its input with a floor of 0.00000001.

*Trees never change after they are made.* Mutation and crossover build new trees and leave the old ones alone, so one tree can safely appear in many places in the population.

*The evolution loop.* `fit` in `gp.py` starts with 500 random trees and repeats these steps for up to 10,000 generations:
1. Score every tree with `get_fitness`. Lower is better.
2. Copy the best tree straight into the next generation (elitism), so the best score never gets worse.
3. Stop if the best score has not improved by at least 0.1 percent for 200 generations, or if it falls below 0.00001.
4. Fill the other 499 spots. Each spot draws a random number: 10 percent of the time a tournament winner is copied, otherwise two winners are crossed over (the child with the lower error is kept) or one winner is mutated.

*Tournament selection.* `get_individual` picks 5 random trees and keeps the one with the lowest error. Bigger trees are penalized by a percentage of their error per node (`SIZE_PENALTY`), so a smaller tree wins a near tie. This keeps the trees from bloating.

*Crossover and mutation.* Crossover picks a random node in each parent and swaps the branches below them. Mutation replaces a random node with a new random branch or leaf. Any child deeper than `MAX_DEPTH` is thrown away and its parent is kept instead. For dataset2, half of the mutations instead nudge one constant by a small random (Gaussian) amount, so decimal constants can be fine tuned.

*Train and test.* Each dataset is split into a training set, which GP sees, and a test set, which it never sees. `run_dataset2.py` and `run_dataset3.py` do 10 runs each and keep the one with the lowest test error. `run_dataset1.py` does one run.

## Files

- `tree.py`: the formula trees: making random trees, mutation, crossover, evaluating, and printing.
- `gp.py`: the evolution loop (`fit`), the fitness (`get_fitness`), and tournament selection (`get_individual`).
- `run_dataset1.py`, `run_dataset2.py`, `run_dataset3.py`: load a dataset, set its options, and run GP.
- `plot.py`: plots dataset3 with the best formula on top.

## How to run

```
python3 run_dataset1.py
python3 run_dataset2.py
python3 run_dataset3.py
```

Each prints its formulas with their errors. Dataset1 takes seconds. Datasets 2 and 3 take several minutes per run.

## Settings

| | Dataset 1 | Dataset 2 | Dataset 3 |
|---|---|---|---|
| Population | 500 | 500 | 500 |
| Fitness | mean squared error | mean relative error | mean squared error |
| Copy / crossover / mutation | 10 / 88 / 2 percent | 10 / 70 / 20 percent | 10 / 70 / 20 percent |
| Constants | whole numbers, -5 to 5 | decimals, -5 to 5, nudged | whole numbers, -5 to 5 |
| Max depth | 8 | 8 | 12 |
| Size penalty | 0.001 percent per node | 0.001 percent per node | 0.1 percent per node |
| Train / test points | 5,000 / 20,000 | 5,000 / 20,000 | 2,000 / 20,000 |

Note: `MUTATION_P` is never read by `fit`. The mutation rate is whatever is left after copying and crossover, so to change it, change `CROSSOVER_P`.

## Results

*Dataset 1.* f(x) = x² - 6x + 14. Every run we recorded with 500 trees found it within about 10 generations, as trees like ((x-2)+(((x-2)*(x-4))+4)-(x-4)) that simplify to it. Its train and test errors are 0.00058 and 0.0006. That is the noise in the data: points with the same x have slightly different y values, so no formula can do better.

*Dataset 2.* f(x1, x2, x3) = G * x1 * x2 / x3², with G = 6.673 x 10⁻¹¹. This is Newton's law of gravity: x1 and x2 are masses, x3 is the distance between them, and G is the gravitational constant (6.674 x 10⁻¹¹). Two things were needed to find it:
- Squared error did not work. y ranges from 0 to 160 billion and a single row made up 99.85 percent of the total squared error. The mean relative error (the miss divided by y + 1) treats every row equally.
- x1 and x2 are divided by 1,000,000 so all three inputs are between 0 and 10. GP found 66.73 * x1 * x2 / x3², which becomes 6.673 x 10⁻¹¹ in the original units.

Its test error is 0.43 percent. The exact law scores 0.38 percent, which is the noise in the measurements. About a third of the runs found it; most of the others got stuck at x1 * x2, which ignores the distance.

*Dataset 3 (extra credit).* We have not found the exact formula. The best run so far has a test error of 44 (a typical miss of about 7, on values between -2,900 and 3,700), but its formula is long and does not simplify. What the data shows:
- y * eˣ is symmetric: its values at -x and x match. So f(x) = e⁻ˣ * h(x), where h(-x) = h(x).
- h is zero at 0, π/2, π, and 3π/2, so it contains a wave like sin(2x).
- h grows roughly like x³.

We also tried fitting h(x) = y * eˣ instead of y. GP fit h well (a test error of 1.3 on h) and ran 4 times faster. But converting back to y multiplies the misses by e⁻ˣ, which is 148 at x = -5, so its test error on y was worse (2,340). `run_dataset3.py` fits y.

## What we learned

- *A bug made trees huge.* The depth check in `crossover` let a too-deep child through when the other child was exactly at the limit. On dataset3, trees grew to 17,000 nodes and runs took up to 19 hours. Checking each child on its own fixed it: runs now take minutes and stay under the depth limit.
- *A fixed size penalty only works at one scale.* An error of 1 and an error of 100,000 need very different penalties, so the penalty is now a percentage of the error.
- *More mutation helped dataset3.* With 20 percent mutation instead of 2 percent, no run got stuck and the typical error went from about 11,000 to about 3,200.
- *Deeper trees help, up to a point.* Our best dataset3 results came from depth 12. Depth 16 was only a little better and took four times as long.
- *GP exploits the protections.* It used x / (x - x) (division by zero, which becomes x) and log(-4) (the log of a negative number, which becomes log 4) as building blocks. 

