from concurrent.futures import ProcessPoolExecutor
from typing import List

from tqdm import tqdm


class WordleSolver:
    def __init__(
        self,
        dictionary_path="5_characters_dictionary_wordle.txt",
        word_list=["tares"],
    ) -> None:
        with open(dictionary_path) as f:
            self.dictionary = f.read().rstrip().split("\n")
        self._word_list = word_list

    @staticmethod
    def calc_result(answer: str, inp: str) -> str:
        res = []
        for a, i in zip(answer, inp):
            if a == i:
                res.append("G")
            elif i in answer:
                res.append("Y")
            else:
                res.append("B")
        return "".join(res)

    @staticmethod
    def search_candidates(
        dictionary: List[str], past_inputs: List[str], past_results: List[str]
    ) -> List[str]:
        fixed = []
        contained = []
        not_contained = []
        contained_set = set()
        for inp, res in zip(past_inputs, past_results):
            for idx, (i, r) in enumerate(zip(inp, res)):
                if r == "G":
                    fixed.append((i, idx))
                    contained_set.add(i)
                elif r == "Y":
                    contained.append((i, idx))
                    contained_set.add(i)
                else:
                    if i in contained_set:
                        contained.append((i, idx))
                    else:
                        not_contained.append(i)
        candidates = []

        for v in dictionary:
            ok = True

            # check fixed characters
            for (c, n) in fixed:
                if v[n] != c:
                    ok = False
                    break
            if not ok:
                continue

            # check contained characters
            for (c, n) in contained:
                if c not in v:
                    ok = False
                    break
                if v[n] == c:
                    ok = False
                    break
            if not ok:
                continue

            # check not contained characters
            for c in not_contained:
                if c in v:
                    ok = False
                    break
            if not ok:
                continue

            candidates.append(v)

        return candidates

    def suggest(
        self, turn: int, past_inputs: List[str], past_results: List[str]
    ) -> str:
        """[summary]

        Args:
            turn (int): past
            past_input (int): past inputs (e.g. apple)
            past_result (int): past results, BLACK: B, YELLOW: Y, GREEN: G (e.g. BGYYG)
        Returns:
            str: suggestion input
        """
        assert len(past_inputs) == len(past_results)
        assert len(past_inputs) == turn

        candidates = self.search_candidates(self.dictionary, past_inputs, past_results)

        if len(candidates) == 1:
            return candidates[0]

        if turn < len(self._word_list):
            return self._word_list[turn]

        min_cand = 1e9
        ret_cand = candidates[0]
        for c in candidates:
            cand = 0
            for a in candidates:
                r = self.calc_result(a, c)
                cand += len(
                    self.search_candidates(
                        candidates, past_inputs + [c], past_results + [r]
                    )
                )
            cand /= len(candidates)
            if min_cand > cand:
                min_cand = cand
                ret_cand = c
        return ret_cand


class WordleSolverSimulator:
    def __init__(self, solver: WordleSolver) -> None:
        self.solver = solver

    def simulate(self, answer: str) -> str:
        assert len(answer) == 5
        past_inputs: List[str] = []
        past_results: List[str] = []
        turn = "x"
        for i in range(6):
            s = self.solver.suggest(i, past_inputs, past_results)
            past_inputs.append(s)
            r = WordleSolver.calc_result(answer, s)
            past_results.append(r)
            if r == "GGGGG":
                turn = str(i + 1)
                break
        # print(f"Wordle {answer} {turn}/6")
        # for r in past_results:
        #     print("".join([{"G": "🟩", "Y": "🟨", "B": "⬛"}[v] for v in r]))

        return turn


if __name__ == "__main__":
    with open("5_characters_dictionary_large.txt") as f:
        answers = f.read().rstrip().split("\n")

    e = ProcessPoolExecutor(16)
    simulator = WordleSolverSimulator(WordleSolver())

    x = []
    futures = []
    turn_sum = 0
    for a in answers:
        futures.append(e.submit(simulator.simulate, a))
    for f, a in tqdm(list(zip(futures, answers))):
        turn = f.result()
        if turn == "x":
            print(a)
            x.append(a)
        else:
            turn_sum += int(turn)
    print("couldn't solve", len(x), x)
    print("mean turn of solution", turn_sum / (len(answers) - len(x)))
