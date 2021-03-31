# nQueens solver
nqueens.py is a python function that finds a single solution to the the classic 
nQueens problem while minimizing time and space complexity.

***(note)***\
The ouput of the solver is formatted as a python list such that the value of the 
*i*-th element in the list represents the column of the Queen on row *i*.
(indexing starts at 1)\
E.g:
```
╔═════════════════╗
║ … … … … … Q … … ║
║ … … … Q … … … … ║
║ … … … … … … Q … ║
║ Q … … … … … … … ║
║ … … … … … … … Q ║
║ … Q … … … … … … ║
║ … … … … Q … … … ║
║ … … Q … … … … … ║
╚═════════════════╝
``` 
is represented as ```[4, 6, 8, 2, 7, 1, 3, 5]```

## What is the nQueens problem?

> The eight queens puzzle is the problem of placing eight chess queens on an 8×8
> chessboard so that no two queens threaten each other; thus, a solution requires 
> that no two queens share the same row, column, or diagonal.

from: [Wikipedia](wikipedia.org/wiki/Eight_queens_puzzle)

## Usage

Simply download the files and either:

* From a terminal, run ```python3 run.py testfile.txt```, with a delimited testfile.txt of ```board_size```'s

* Import nqueens.py in a python program with ```from nqueens import solve```, and use ```solve(board_size)```.