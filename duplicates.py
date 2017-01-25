import os
from collections import Counter
from itertools import combinations


def convert_bytes(size):
    for measure in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return '{0} {1}'.format(round(size, 1), measure)
        size /= 1024


def get_duplicate_candidates(dir_path='.'):
    basedir = os.path.abspath(dir_path)
    print(dir_path)
    filecount = Counter()
    all_canidates = list()
    for root, dirs, files in os.walk(basedir):
        filecount.update(files)
        dir_candidates = [file for file in files if filecount[file] > 1]
        dir_candidates = [os.path.join(file, root) for file in dir_candidates]
        all_canidates += dir_candidates
    return all_canidates


def are_files_duplicates(file_path_1, file_path_2):
    if os.path.basename(file_path_1) == os.path.basename(file_path_2):
        return os.path.getsize(file_path_1) == os.path.getsize(file_path_2)


def pretty_print(file_path_1, file_path_2, sizeof_duplicate):
    pretty_sizeof_file_1 = convert_bytes(sizeof_duplicate)
    print('\n\n{0}\n{1}\n\nRedundant: {2}'.format(file_path_1,
                                                  file_path_2,
                                                  pretty_sizeof_file_1))


def get_redundant_space(candidates):
    totally_occupied = 0
    for file_1, file_2 in combinations(candidates, 2):
        if are_files_duplicates(file_1, file_2):
            sizeof_duplicate = os.path.getsize(file_1)
            pretty_print(file_1, file_2, sizeof_duplicate)
            totally_occupied += sizeof_duplicate
    return totally_occupied


if __name__ == '__main__':
    dir_to_scan = input('Input dir name: ')
    candidates = get_duplicate_candidates(dir_to_scan)
    totally_occupied = get_redundant_space(candidates)
    totally_occupied = convert_bytes(totally_occupied)
    print('\n------------------\n{0} totally can be freed\n'.format(totally_occupied))
