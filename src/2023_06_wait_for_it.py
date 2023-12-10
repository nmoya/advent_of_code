from typing import List

import utils


def parse_line(raw_line, line_name) -> List[int]:
    line = raw_line.replace(line_name + ":", "")
    out = []
    for number in line.strip().split(" "):
        if number == "":
            continue
        out.append(int(number.strip()))
    return out


def parse_time(line) -> List[int]:
    return parse_line(line, "Time")


def parse_distance(line) -> List[int]:
    return parse_line(line, "Distance")


def count_solutions(time: int, record: int) -> int:
    count = 0
    for i in range(time):
        speed = i
        remaining_time = time - i
        distance = remaining_time * speed
        if distance > record:
            count += 1
    return count


def solution(filename):
    lines = list(utils.read_by_line(filename))
    times = parse_time(lines[0])
    distance = parse_distance(lines[1])
    total_solutions = 1
    for i, time in enumerate(times):
        total_solutions *= count_solutions(time, distance[i])
    print(total_solutions)

    str_times = [str(time) for time in times]
    str_distance = [str(dist) for dist in distance]
    total_time = int("".join(str_times))
    total_distance = int("".join(str_distance))
    print(count_solutions(total_time, total_distance))


def test_samples():
    lines = utils.read_by_line("src/2023_06_wait_for_it_sample.txt")
    pass


if __name__ == "__main__":
    test_samples()
    solution("src/2023_06_wait_for_it.txt")
