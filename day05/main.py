import re
from copy import deepcopy
from dataclasses import dataclass

get_letter_re = re.compile('[A-Z]')
get_number_re = re.compile('[0-9]+')


def read_from_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        _file_content: str = f.read()
    return _file_content


@dataclass
class Action:
    quantity: int
    from_stack: int
    to_stack: int


def read_stacks(stack_input_str) -> list[list[str]]:
    _stacks: list[list[str]] = []
    stack_input_lines: list[str] = stack_input_str.split('\n')

    number_of_stacks_match = re.search(r'\S+\s*$', stack_input_lines[-1])
    number_of_stacks: int = int(number_of_stacks_match.group())
    end_pos: int = number_of_stacks_match.span()[1]

    for _ in range(number_of_stacks):
        _stacks.append([])

    for line in reversed(stack_input_lines[: -1]):
        start_pos = 0
        current_stack = 0

        while start_pos < end_pos:
            next_letter = get_letter_re.search(line, start_pos, start_pos + 4)
            start_pos = start_pos + 4

            if next_letter:
                _stacks[current_stack].append(next_letter.group())
            current_stack += 1

    return _stacks


def read_actions(action_input_str) -> list[Action]:
    _actions = []

    action_input_lines = action_input_str.split('\n')
    for line in action_input_lines:
        quantity, from_, to_ = tuple(map(int, get_number_re.findall(line)))
        _actions.append(Action(quantity, from_ - 1, to_ - 1))
    return _actions


def move_stacks_9000(stacks_to_move, rearrange_actions) -> list[list[str]]:
    _stacks = deepcopy(stacks_to_move)

    for action in rearrange_actions:
        for _ in range(action.quantity):
            crate = _stacks[action.from_stack].pop()
            _stacks[action.to_stack].append(crate)
    return _stacks


def move_stacks_9001(stacks_to_move, rearrange_actions) -> list[list[str]]:
    _stacks = deepcopy(stacks_to_move)

    for action in rearrange_actions:
        crates = []
        for _ in range(action.quantity):
            crates.insert(0, _stacks[action.from_stack].pop())

        _stacks[action.to_stack].extend(crates)
    return _stacks


if __name__ == '__main__':
    init_input: str = read_from_file('./test_input.txt')
    stack_input, action_input = init_input.split('\n\n', 2)

    stacks: list[list[str]] = read_stacks(stack_input)
    actions: list[Action] = read_actions(action_input)

    stacks_part_one: list[list[str]] = move_stacks_9000(stacks, actions)
    stacks_part_two: list[list[str]] = move_stacks_9001(stacks, actions)

    print('Part One:', ''.join(stack[-1] for stack in stacks_part_one))
    print('Part Two:', ''.join(stack[-1] for stack in stacks_part_two))
