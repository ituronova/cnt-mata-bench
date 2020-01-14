#!/usr/bin/env python3

import argparse
import csv
import sys
from tabulate import tabulate

# fmt = 'text'
fmt = 'csv'

###########################################
def proc_res(fd):
    """proc_res(fd) -> _|_

    processes results from file descriptor 'fd'
"""
    reader = csv.reader(
        fd, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    engines = list()
    engines_match = list()
    results = dict()
    for row in reader:
        eng, pattern = row[1], row[2]
        if pattern not in results:
            results[pattern] = dict()
        if eng not in engines:
            engines.append(eng)
            engines_match.append(eng + '-matches')

        if row[0] == 'finished':
            retcode, count_lines, run_time = row[3], row[4], row[6]

            results[pattern][eng] = run_time
            results[pattern][eng + '-matches'] = count_lines

        if row[0] == 'error':
            results[pattern][eng] = 'ERR'
            results[pattern][eng + '-matches'] = 'ERR'

        if row[0] == 'timeout':
            results[pattern][eng] = 'TO'
            results[pattern][eng + '-matches'] = 'TO'

    list_ptrns = list()
    for ptrn in results:
        ls = [ptrn]
        for eng in engines:
            if eng in results[ptrn]:
                ls.append(results[ptrn][eng])
            else:
                ls.append(None)
        for eng in engines_match:
            if eng in results[ptrn]:
                ls.append(results[ptrn][eng])
            else:
                ls.append(None)
        list_ptrns.append(ls)

    header = ['pattern'] + engines + engines_match

    if fmt == 'html':
        print(tabulate(list_ptrns, header, tablefmt='html'))
    elif fmt == 'text':
        print(tabulate(list_ptrns, header, tablefmt='text'))
    elif fmt == 'csv':
        writer = csv.writer(
            sys.stdout, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(list_ptrns)
    else:
        raise Exception('Invalid output format: "{}"'.format(fmt))
    return


###############################
if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 1:
        fd = sys.stdin
    elif argc == 2:
        fd = open(sys.argv[1], "r")
    else:
        print("Invalid number of arguments: either 0 or 1 required")
        sys.exit(1)

    proc_res(fd)
    if argc == 2:
        fd.close()
