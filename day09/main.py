from dataclasses import dataclass
from math import copysign
from typing import Self


@dataclass
class Position:
    x: int
    y: int

    def move(self, direction):
        match direction:
            case 'R':
                self.x += 1
            case 'L':
                self.x -= 1
            case 'D':
                self.y -= 1
            case 'U':
                self.y += 1

    def follow(self, other: Self):
        distance_x, distance_y = other.x - self.x, other.y - self.y

        if abs(distance_x) <= 1 and abs(distance_y) <= 1:
            return

        if abs(distance_x) > abs(distance_y):
            self.x, self.y = other.x - int(copysign(1, distance_x)), other.y
        elif abs(distance_x) < abs(distance_y):
            self.x, self.y = other.x, other.y - int(copysign(1, distance_y))
        else:
            # both distances 2
            self.x, self.y = other.x - int(copysign(1, distance_x)), other.y - int(copysign(1, distance_y))


def read_from_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        _file_content: str = f.read()
    return _file_content


def process_movements(init_input: str, number_of_knots: int):
    knots = [Position(0, 0) for _ in range(number_of_knots)]

    _positions = {(0, 0)}

    for line in init_input.splitlines():
        direction, quantity = line.split()
        quantity = int(quantity)

        for _ in range(quantity):
            knots[0].move(direction)
            for knot_number in range(1, len(knots)):
                knots[knot_number].follow(knots[knot_number - 1])
            _positions.add((knots[-1].x, knots[-1].y))
    return _positions


if __name__ == '__main__':
    _init_input: str = read_from_file('./test_input.txt')
    positions = process_movements(_init_input, number_of_knots=2)
    print('Part one', len(positions))
    positions = process_movements(_init_input, number_of_knots=10)
    print('Part two', len(positions))
