from typing import List

from solver import WordleSolver

past_inputs: List[str] = []
past_results: List[str] = []
solver = WordleSolver()
for i in range(6):
    s = solver.suggest(i, past_inputs, past_results)
    print(f'[turn {i+1}] solver\'s suggestion: "{s}"')
    print(
        'enter your input and wordles result (e.g "apple BGGYY", here G means green, Y means yellow, B means other)'
    )
    i, r = input().rstrip().split()
    past_inputs.append(i)
    past_results.append(r)
