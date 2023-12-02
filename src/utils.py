def read_input(filename):
    with open(filename, 'r') as f:
        return f.read()


def read_by_line(filename):
    content = read_input(filename)
    for line in content.split('\n'):
        yield line
