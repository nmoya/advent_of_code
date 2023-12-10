def read_input(filename):
    with open(filename, 'r') as f:
        return f.read()


def read_by_line(filename):
    content = read_input(filename)
    for line in content.split('\n'):
        yield line


def create_template(name):
    with open(f'./src/{name}.py', 'w') as f:
        f.write(
            f'''import utils


def solution(filename):
    lines = utils.read_by_line(filename)
    for line in lines:
        pass


def test_samples():
    lines = utils.read_by_line("src/{name}_sample.txt")
    pass


if __name__ == "__main__":
    test_samples()
    solution("src/{name}_sample.txt")
'''
        )

    with open(f'./src/{name}.txt', 'w') as f:
        f.write("")
    with open(f'./src/{name}_sample.txt', 'w') as f:
        f.write("")


if __name__ == "__main__":
    create_template('2023_06_wait_for_it')
