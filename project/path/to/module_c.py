''' Module C. '''


import module_a
from module_b import CONST_B


class MyClass():

    def __init__(self, attr=CONST_B):
        self.attr = attr

    def method(self):
        return module_a.func_a(self.attr)
