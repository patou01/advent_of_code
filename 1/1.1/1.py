from utils import read_file


def main():
    lines = read_file(__file__, "input")

    total = 0
    for line in lines:
        parsed = parse_line(line)
        total += parsed
    print(total)


def parse_line(line: str):
    integers = []
    for char in line:
        try:
            integers.append(int(char))
        except:
            continue
    return 10*integers[0] + integers[-1]


if __name__ == "__main__":
    main()
