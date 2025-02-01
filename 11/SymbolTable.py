"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    FIELD = "field"
    STATIC = "static"
    ARG = "argument"
    VAR = "var"
    CONS = "constructor"
    METHOD = "method"
    THIS = "this"
    LOCAL = "local"


    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self.counting_the_index = {sel7uyf.ARG: 0, self.STATIC: 0, self.VAR: 0, self.FIELD: 0}
        self.starting_subroutine_table = {}
        self.class_table = {}

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self.starting_subroutine_table = {}
        self.counting_the_index[self.ARG] = 0
        self.counting_the_index[self.VAR] = 0


    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if kind == self.STATIC:
            self.class_table[name] = (kind, type, self.counting_the_index[kind])
            self.counting_the_index[kind] += 1
        elif kind == self.FIELD:
            self.class_table[name] = (self.THIS, type, self.counting_the_index[kind])
            self.counting_the_index[kind] += 1
        elif kind == self.LOCAL:
            self.starting_subroutine_table[name] = (kind, type, self.counting_the_index[self.VAR])
            self.counting_the_index[self.VAR] += 1
        else:
            self.starting_subroutine_table[name] = (kind, type, self.counting_the_index[kind])
            self.counting_the_index[kind] += 1

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        return self.counting_the_index[kind]

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        if name in self.class_table:
            return self.class_table[name][0]
        elif name in self.starting_subroutine_table:
            return self.starting_subroutine_table[name][0]


    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self.class_table:
            return self.class_table[name][1]
        elif name in self.starting_subroutine_table:
            return self.starting_subroutine_table[name][1]

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if name in self.class_table:
            return self.class_table[name][2]
        elif name in self.starting_subroutine_table:
            return self.starting_subroutine_table[name][2]

    def check_if_var(self, name):
        if name in self.class_table.keys() or name in self.starting_subroutine_table.keys():
            return True
        return False

