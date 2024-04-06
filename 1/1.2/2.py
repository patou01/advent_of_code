

parse_dict = {"one": 1,
              "two": 2,
              "three": 3,
              "four": 4,
              "five": 5,
              "six": 6,
              "seven": 7,
              "eight": 8,
              "nine": 9,
              }


def main():
    lines = read_file("input")

    total = 0
    for line in lines:
        parsed = handle_line(line)
        total += parsed
    print(total)


def handle_line(line: str):
    """
    The idea here is to replace eg "eight" with "8". However, "eightwo" should be replaced to "82", therefore,
    we replace each occurence with the digit and its name.
    "eightwo" becomes "8eight2two", we later then only need to look for the integers.
    :param line:
    :return:
    """
    integers = []
    length = len(line)
    for n, char in enumerate(line):
        try:
            integers.append(int(char))
            continue
        except:
            pass
        for digit, as_int in parse_dict.items():
            if n < length - len(digit):
                if line[n:n+len(digit)] == digit:
                    integers.append(as_int)
    return 10*integers[0] + integers[-1]


def read_file(file):
    with open(file, "r") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
