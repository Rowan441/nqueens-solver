import sys
import time

from nqueens import solve

if len(sys.argv) < 2:
    print("\n\tUsage: python3 run.py <test-file>\n")
    exit(1)

in_file = sys.argv[1]

with open(in_file) as f:
    problems = map(int, f.readlines())

for p in problems:
    start = time.time()
    solution = solve(p)
    end = time.time()
    print(solution)
    print(p, "solved in:", end - start)

