import os


def convert_bytes(size):
    for measure in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return '{0} {1}'.format(round(size, 1), measure)
        size /= 1024


def get_files(dir_path='.'):
    basedir = os.path.abspath(dir_path)
    dir_content = os.listdir(basedir)
    files = list()
    for item in dir_content:
        full_path = os.path.join(basedir, item)
        if os.path.isdir(full_path):
            files += (get_files(full_path))
        else:
            files.append(full_path)
    return files


def are_files_duplicates(file_path_1, file_path_2):
    if os.path.basename(file_path_1) == os.path.basename(file_path_2):
        if os.path.getsize(file_path_1) == os.path.getsize(file_path_2):
            return True
    return False


def pretty_print(file_path_1, file_path_2):
    sizeof_file_1 = os.path.getsize(file_path_1)
    pretty_sizeof_file_1 = convert_bytes(sizeof_file_1)
    print('\n\n{0}\n{1}\n\nRedundant: {2}'.format(file_path_1,
                                                  file_path_2,
                                                  pretty_sizeof_file_1))


def get_redundant_space(files):
    first, *rest = files
    totally_occupied = 0
    for file in rest:
        if are_files_duplicates(first, file):
            pretty_print(first, file)
            totally_occupied += os.path.getsize(first)
    if rest:
        totally_occupied += get_redundant_space(rest)
    return totally_occupied


if __name__ == '__main__':
    dir_to_scan = input('Input dir name: ')
    files = get_files(dir_to_scan)
    totally_occupied = get_redundant_space(files)
    totally_occupied = convert_bytes(totally_occupied)
    print('\n------------------\n{0} totally can be freed\n'.format(totally_occupied))
