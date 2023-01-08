def read_from_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        _file_content: str = f.read()
    return _file_content


def process_input(init_input: str):
    cwd = ''
    for line in init_input.splitlines():
        match line.split():
            case ['$', 'cd', '/']:
                cwd = ''
            case ['$', 'cd', '..']:
                cwd = cwd[:cwd.rindex('/') if '/' in cwd else 0]
            case ['$', 'cd', directory]:
                cwd = '/'.join((cwd, directory))
            case ['$' | 'dir',  _]:
                pass
            case file_size, filename:
                file_size = int(file_size)




if __name__ == '__main__':
    _init_input: str = read_from_file('./example_input.txt')
    process_input(_init_input)
