#!/usr/bin/env python3
''' Visualize the import relationships of a python project. '''


import argparse
import os
import sys
import distutils.sysconfig as sysconfig
from pprint import pprint
from modulefinder import ModuleFinder

from libinfo import is_py2_std_lib_module, is_py3_std_lib_module


# Python 2 or 3
PY_VERSION = sys.version_info[0]

# list of standard library module names, to be populated
STDLIB_MODULES = []


def get_std_lib_modules():
    global STDLIB_MODULES
    if STDLIB_MODULES:
        return STDLIB_MODULES
    std_lib = sysconfig.get_python_lib(standard_lib=True)
    STDLIB_MODULES = []
    for top, dirs, files in os.walk(std_lib):
        for nm in files:
            if nm != '__init__.py' and nm[-3:] == '.py':
                STDLIB_MODULES.append(
                    os.path.join(top, nm)[len(std_lib) + 1:-3].replace('/', '.'))
    return STDLIB_MODULES


def is_std_lib_module(mod_name):
    is_in_hardcoded_list = (is_py2_std_lib_module if PY_VERSION == 2 else is_py3_std_lib_module)
    return (is_in_hardcoded_list(mod_name) or mod_name in get_std_lib_modules())


def filter_std_lib_modules(modules):
    """ Filter out modules from the list that are in the standard library. """

    return {name: mod for name, mod in modules.items() if not
            is_std_lib_module(name)}


def get_modules_from_file(script, root_dir, use_sys_path=False):
    """ Use ModuleFinder.load_file() to get module imports for the given
    script.

    :param script: the script we're getting modules from
    :param root_dir: the project's root dir, if different from script's dir
    :param use_sys_path: use the system PATH when looking for module defs, this
    may be useful if you want to add stdlib modules
    :rtype: list of Modules
    """
    path = [root_dir]
    if use_sys_path:
        path.append(sys.path[:])

    finder = ModuleFinder(path)
    finder.load_file(script)
    modules = filter_std_lib_modules(finder.modules)
    return modules


def get_args():
    """ Parse and return command line args. """
    parser = argparse.ArgumentParser(description='Visualize imports of a given'
                                     ' python script.')
    parser.add_argument('script', type=str,
                        help='main python script/entry point for project')
    parser.add_argument('-r', '--rootdir', dest='root_dir', type=str,
                        help='root of the project directory, if it differs '
                        'from the script directory')
    return parser.parse_args()


def main():

    args = get_args()
    script, root_dir = args.script, args.root_dir
    if not root_dir:
        root_dir = os.path.dirname(script)

    modules = get_modules_from_file(script, root_dir)
    for name, mod in modules.items():
        print("SUBMODS for {}".format(name))
        submods = get_modules_from_file(mod.__file__, root_dir)
        pprint(submods)


if __name__ == '__main__':
    main()
