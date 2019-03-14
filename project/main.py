""" Test project for import-visualizer. """


import sys

# module_c imports both module_a and module_b
from path.to.module_c import MyClass

# module_d is in project/ but not imported anywhere


def main():
    my_instance = MyClass()
    my_instance.method()


if __name__ == "__main__":
    main()
