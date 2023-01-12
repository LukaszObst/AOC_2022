import ast


def read_from_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        _file_content: str = f.read()
    return _file_content


def check_input(input_to_check: str):
    if any(c not in '[],0123456789' for c in input_to_check):
        raise ValueError('Invalid input: ' + input_to_check)
    return input_to_check


def process_input_into_packet_pairs(raw_input: str) -> list[int]:
    input_lines = filter(str.strip, raw_input.splitlines())
    return [ast.literal_eval(check_input(line)) for line in input_lines]


def is_packet_pair_order_right(left_input: list | int, right_input: list | int) -> bool:
    next_to_compare: list[tuple] = [(left_input, right_input)]

    while next_to_compare:
        left, right = next_to_compare.pop(0)
        match left, right:
            case int(), int():
                if left == right:
                    continue
                return left < right
            case int(), list():
                next_to_compare.insert(0, ([left], right))
            case list(), int():
                next_to_compare.insert(0, (left, [right]))
            case list(), list():
                for pos, (left_next, right_next) in enumerate(zip(left, right)):
                    next_to_compare.insert(pos, (left_next, right_next))
                next_to_compare.insert(min(len(left), len(right)), (len(left), len(right)))

    return True


def part1(packets):
    ind_of_packets_in_right_order = [ind // 2 + 1 for ind in range(0, len(packets), 2) if
                                     is_packet_pair_order_right(packets[ind], packets[ind + 1])]
    return sum(ind_of_packets_in_right_order)


def part2(packets):
    divider1, divider2 = [[2]], [[6]]
    count1, count2 = 1, 2
    for packet in packets:
        if is_packet_pair_order_right(packet, divider1):
            count1 += 1
        if is_packet_pair_order_right(packet, divider2):
            count2 += 1
    return count1 * count2


if __name__ == '__main__':
    file_content: str = read_from_file('./test_input.txt')
    _packets = process_input_into_packet_pairs(file_content)

    print('Part one', part1(_packets))
    print('Part two', part2(_packets))
