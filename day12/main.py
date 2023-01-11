from dataclasses import dataclass
from typing import Self, Callable


def read_from_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        _file_content: str = f.read()
    return _file_content


@dataclass
class Node:
    height: str
    pos_x: int
    pos_y: int
    neighbors: list[Self]


def forward_search(cur_node, other_node):
    return ord(cur_node.height) <= ord(other_node.height) + 1


def backwards_search(cur_node, other_node):
    return ord(cur_node.height) + 1 >= ord(other_node.height)


def connect_nodes(_nodes: dict[tuple[int, int], Node], rows: int, cols: int, reverse_search: bool):
    height_test = forward_search if reverse_search else backwards_search

    for (pos_x, pos_y), cur_node in _nodes.items():
        neighbors_pos = [(pos_x + delta_x, pos_y) for delta_x in range(-1, 2, 2) if 0 <= pos_x + delta_x <= rows]
        neighbors_pos.extend([(pos_x, pos_y + delta_y) for delta_y in range(-1, 2, 2) if 0 <= pos_y + delta_y <= cols])

        for (neighbor_x, neighbor_y) in neighbors_pos:
            if height_test(cur_node, _nodes[(neighbor_x, neighbor_y)]):
                cur_node.neighbors.append(_nodes[(neighbor_x, neighbor_y)])


def init_nodes(init_str: str, reverse_search: bool) -> tuple[dict[tuple[int, int], Node], Node, Node]:
    _nodes: dict[tuple[int, int], Node] = {}
    lineno, letter_no, start_node, end_node = 0, 0, None, None

    for lineno, line in enumerate(init_str.splitlines()):
        for letter_no, letter in enumerate(line):
            _nodes[(lineno, letter_no)] = Node(height=letter, pos_x=lineno, pos_y=letter_no, neighbors=[])
            if letter == 'S':
                start_node = _nodes[(lineno, letter_no)]
                start_node.height = 'a'
            if letter == 'E':
                end_node = _nodes[(lineno, letter_no)]
                end_node.height = 'z'

    connect_nodes(_nodes, rows=lineno, cols=letter_no, reverse_search=reverse_search)
    return _nodes, start_node, end_node


def find_path(start_node: Node, check_if_finished: Callable[[Node], bool]):
    visited, path, paths_to_explore = [], [], [(0, start_node)]
    while paths_to_explore:
        steps, node = paths_to_explore.pop(0)

        if node in visited:
            continue

        visited.append(node)
        for neighbor in node.neighbors:
            if check_if_finished(neighbor):
                return steps + 1
            if neighbor not in visited:
                paths_to_explore.append((steps + 1, neighbor))
    return -1


if __name__ == '__main__':
    file_content: str = read_from_file('./test_input.txt')
    nodes, start, end = init_nodes(file_content, False)
    shortest_path_from_s_steps = find_path(start, check_if_finished=lambda n: n == end)
    print('Part one', shortest_path_from_s_steps)

    # noinspection PyRedeclaration
    nodes, start, end = init_nodes(file_content, True)
    shortest_path_overall_steps = find_path(end, check_if_finished=lambda n: n.height == 'a')
    print('Part two', shortest_path_overall_steps)
