import operator
from copy import deepcopy
from dataclasses import dataclass
from math import lcm
from typing import Callable


def read_from_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        _file_content: str = f.read()
    return _file_content


@dataclass
class Monkey:
    id: int
    current_items: list[int]
    worry_level_operation: Callable[[int], int]
    test_condition: int
    if_test_true_monkey: int
    if_test_false_mokey: int
    inspected_items: int = 0

    def __lt__(self, other):
        return self.id < other.id


def init_monkeys(init_input: str) -> list[Monkey]:
    monkeys: list[Monkey] = []

    for cur_block in init_input.split('\n\n'):
        cur_block = cur_block.splitlines()
        monkey_number: int = int(cur_block[0].split(' ')[1][:-1])
        starting_items: list[int] = list(map(int, cur_block[1].split(':')[1].split(',')))
        worry_level_operation: Callable[[int], int] = eval('lambda old: ' + cur_block[2].split('=')[1])
        test_condition: int = int(cur_block[3].split('divisible by')[1])
        if_test_true_monkey = int(cur_block[4].split('to monkey')[1])
        if_test_false_mokey = int(cur_block[5].split('to monkey')[1])
        _monkey: Monkey = Monkey(id=monkey_number, current_items=starting_items,
                                 worry_level_operation=worry_level_operation,
                                 test_condition=test_condition, if_test_true_monkey=if_test_true_monkey,
                                 if_test_false_mokey=if_test_false_mokey)
        monkeys.append(_monkey)
    monkeys.sort()
    return monkeys


def play_round(current_monkeys: list[Monkey], relief_func: Callable[[int], int]):
    for _monkey in current_monkeys:
        while _monkey.current_items:
            item_worry_level = _monkey.current_items.pop(0)
            _monkey.inspected_items += 1
            new_worry_level = relief_func(_monkey.worry_level_operation(item_worry_level))
            if (new_worry_level % _monkey.test_condition) == 0:
                throw_to_monkey_with_id: int = _monkey.if_test_true_monkey
            else:
                throw_to_monkey_with_id: int = _monkey.if_test_false_mokey
            current_monkeys[throw_to_monkey_with_id].current_items.append(new_worry_level)


def play_rounds(current_monkeys: list[Monkey], number_of_rounds: int, relief_func: Callable[[int], int]):
    for i in range(number_of_rounds):
        play_round(current_monkeys, relief_func)


def part1(monkeys: list[Monkey]):
    play_rounds(monkeys, 20, relief_func=lambda x: x // 3)
    monkeys.sort(key=operator.attrgetter('inspected_items'), reverse=True)
    print('Part one', monkeys[0].inspected_items * monkeys[1].inspected_items)


def part2(monkeys: list[Monkey]):
    lcm_monkey_test = lcm(*(monkey.test_condition for monkey in monkeys))
    play_rounds(monkeys, 10000, relief_func=lambda x: x % lcm_monkey_test)
    monkeys.sort(key=operator.attrgetter('inspected_items'), reverse=True)
    print('Part two', monkeys[0].inspected_items * monkeys[1].inspected_items)


if __name__ == '__main__':
    _init_input: str = read_from_file('./example_input.txt')
    monkeys_init: list[Monkey] = init_monkeys(_init_input)

    part1(deepcopy(monkeys_init))
    part2(deepcopy(monkeys_init))
