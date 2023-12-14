import utils


class Sequence:
    def __init__(self, raw_line):
        self.sequence = [int(num.strip()) for num in raw_line.split(" ")]

    def compute_diff(self, sequence):
        diff = []
        for i in range(1, len(sequence)):
            diff.append(sequence[i] - sequence[i - 1])
        return diff

    def compute_diffs_recursive(self, seq, results):
        if all([num == 0 for num in seq]):
            return results
        else:
            partial = self.compute_diff(seq)
            results.append(partial)
            return self.compute_diffs_recursive(partial, results)

    def predict_next_number(self):
        diffs = self.compute_diffs_recursive(self.sequence, [self.sequence])
        next_num = diffs[-1][-1]
        for i in range(len(diffs) - 1, 0, -1):
            next_num = next_num + diffs[i - 1][-1]
        return next_num

    def predict_first_number(self):
        diffs = self.compute_diffs_recursive(self.sequence, [self.sequence])
        next_num = diffs[-1][0]
        for i in range(len(diffs) - 1, 0, -1):
            next_num = diffs[i - 1][0] - next_num
        return next_num


def solution(filename):
    lines = utils.read_by_line(filename)
    seqs = []
    for line in lines:
        seqs.append(Sequence(line))

    for i, seq in enumerate(seqs):
        print(f"Seq {i}: {seq.predict_first_number()}")
    print(sum([seq.predict_next_number() for seq in seqs]))
    print(sum([seq.predict_first_number() for seq in seqs]))


def test_samples():
    lines = list(utils.read_by_line("src/2023_09_mirage_maintenance_sample.txt"))
    assert Sequence(lines[0]).sequence == [0, 3, 6, 9, 12, 15]
    assert Sequence(lines[0]).predict_next_number() == 18


if __name__ == "__main__":
    test_samples()
    solution("src/2023_09_mirage_maintenance.txt")
