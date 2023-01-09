def read_from_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        _file_content: str = f.read()
    return _file_content


def inc_cycle_and_reg(cycle, increment, *, curr_val, curr_reg, watcher, cycles_to_watch, crt_arr):
    for i in range(1, increment + 1):
        cycle += 1
        # increment reg value if necessary
        if i == increment:
            curr_reg += curr_val
        # crt: lit pixel
        if -1 <= (cycle - 1) % 40 - curr_reg <= 1:
            crt_arr.append(cycle)
        # remember special cycle values
        if cycles_to_watch(cycle):
            watcher[cycle] = curr_reg
    return cycle, curr_reg


def watcher_rules(check_cycle):
    return check_cycle == 20 or (check_cycle - 20) % 40 == 0


def process_program(programm_code: str):
    _x, cycle, _x_register = 1, 1, {}
    _crt = [1]

    for line in programm_code.splitlines():
        match line.split():
            case ['addx', val]:
                cycle, _x = inc_cycle_and_reg(cycle, 2, curr_val=int(val), curr_reg=_x, watcher=_x_register,
                                              cycles_to_watch=watcher_rules, crt_arr=_crt)
            case ['noop']:
                cycle, _x = inc_cycle_and_reg(cycle, 1, curr_val=0, curr_reg=_x, watcher=_x_register,
                                              cycles_to_watch=watcher_rules, crt_arr=_crt)

    return _x_register, _crt


def draw_crt(lit_pixel_on_crt: list[int]):
    for y in range(6):
        print(''.join('#' if x + y * 40 in lit_pixel_on_crt else '.' for x in range(1, 41)))


if __name__ == '__main__':
    _init_input: str = read_from_file('./test_input.txt')
    x_register, crt = process_program(_init_input)
    print('Part one', sum(key * val for key, val in x_register.items()))
    print('Part two:')
    draw_crt(crt)
