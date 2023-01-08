def read_from_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        _file_content: str = f.read()
    return _file_content


def process_calories_from_input(_init_input: str) -> list[int]:
    _elf_calories: list[int] = [sum(map(int, elf_input.split())) for elf_input in _init_input.split('\n\n')]
    return _elf_calories


def part_one(_sorted_elf_calories):
    return _sorted_elf_calories[-1]


def part_two(_sorted_elf_calories):
    return sum(_sorted_elf_calories[-3:])


if __name__ == '__main__':
    init_input: str = read_from_file('./test_input.txt')
    elf_calories = process_calories_from_input(init_input)
    sorted_elf_calories = sorted(elf_calories)

    most_calories = part_one(sorted_elf_calories)
    calories_of_top_three = part_two(sorted_elf_calories)

    print(most_calories, calories_of_top_three)
