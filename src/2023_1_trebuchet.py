import utils


def first_number_in_string(text: str) -> str | None:
    for char in text:
        if char.isdigit():
            return char
    return None


def replace_name_with_number(text: str) -> str:
    values = {
        "one": "o1e",
        "two": "t2o",
        "three": "t3e",
        "four": "f4r",
        "five": "f5e",
        "six": "s6x",
        "seven": "s7n",
        "eight": "e8t",
        "nine": "n9e",
    }
    for key, value in values.items():
        text = text.replace(key, value)
    return text


def first_and_last_number(text: str) -> int:
    text = replace_name_with_number(text)
    first_number = first_number_in_string(text)
    last_number = first_number_in_string(text[::-1])
    if first_number is None or last_number is None:
        raise Exception(f"No number in string: {text}")
    return int(first_number + last_number)


def trebuchet(filename):
    accumulator = 0
    for calibration in utils.read_by_line(filename):
        accumulator += first_and_last_number(calibration)
    print(accumulator)


def test_samples():
    assert first_and_last_number("741two") == 72
    assert first_and_last_number("7eightvdr") == 78
    assert first_and_last_number("22ninehjq") == 29
    assert first_and_last_number("c8four") == 84
    assert first_and_last_number("25nine") == 29
    assert first_and_last_number("9threeclpdskczbl") == 93
    assert first_and_last_number("7eightk") == 78
    assert first_and_last_number("22tone") == 21
    assert first_and_last_number("5threespcbkb") == 53
    assert first_and_last_number("41nine") == 49
    assert first_and_last_number("twoxx") == 22
    assert first_and_last_number("ddgjgcrssevensix37twooneightgt ") == 78


if __name__ == "__main__":
    test_samples()
    trebuchet("src/2023_trebuchet.txt")
