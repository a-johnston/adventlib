from datetime import datetime
from importlib import import_module
from itertools import chain
import os
import sys

def _get_working_path():
    if len(sys.argv) > 1:
        return (sys.argv[1] if 'day' in sys.argv[1] else f'day{sys.argv[1]}').rstrip(os.path.sep)
    return ''

def _get_files(ext):
    base = _get_working_path()
    return (os.path.join(base, name) for name in os.listdir(base or '.') if name.endswith(ext))

def _get_solvers(file):
    try:
        module = import_module(file.replace(os.path.sep, '.')[:-3])
        for name in dir(module):
            if name.startswith('solve'):
                yield name[6:], getattr(module, name)
    except ModuleNotFoundError:
        print('! Failed to import', file)

def _get_text_files(for_solver, all_solvers):
    for file in _get_files('.txt'):
        if file.startswith('skip'):
            continue
        if any(name in file for name in all_solvers) and for_solver not in file:
            continue
        yield file

def _run_solver(solver, file):
    with open(file) as fp:
        start = datetime.now()
        lines = [line.strip() for line in fp.readlines()]
        solution = str(solver(lines))
        if '\n' in solution:
            solution = '\n  ' + solution.replace('\n', '\n  ')
        print(f'\n {file:<12}: {solution}')
        duration = (datetime.now() - start).total_seconds()
        print(f' Completed in {duration:0.4f}s')

def _run_all_solvers(solvers):
    print(os.path.basename(os.getcwd()).replace('day', 'Day '))
    start = datetime.now()
    for name, solver in solvers.items():
        if name:
            print('\n' + name.replace('p', 'Part '))
        all_files = list(_get_text_files(name, solvers))
        if all_files:
            for file in all_files:
                _run_solver(solver, file)
        else:
            print(' [No matching text files]')
    duration = (datetime.now() - start).total_seconds()
    print(f'\nOverall completed in {duration:0.4f}s')

def cli():
    sys.path.append('')
    solvers = dict(chain(*map(_get_solvers, _get_files('.py'))))
    if solvers:
        _run_all_solvers(solvers)
    else:
        print('[No solvers found]')
