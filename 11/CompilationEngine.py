"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from SymbolTable import *
from VMWriter import *

SPACE_TAB = "  "
SUBROUTINE_DEC = {"method", "function", "constructor"}
CLASS_VARDEC = {"static", "field"}
LIST_WORDS = {"true", "false", "this", "null"}
INT_CONT = "integerConstant"
STR_CONT = "stringConstant"
UNARY_OPERATORS = ['~', '-', '^', '#']
BINARY_OP = {'+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '='}
PUSH = "push"
POP = "pop"
THAT = "that"
THIS = "this"



class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_lines: list,
                output_stream: typing.TextIO) -> None:
        """
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.input_lines = input_lines
        self.curr_line = 0
        self.curr_token = ""
        self.curr_items = []
        self.output_file = output_stream
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(self.output_file)
        self.label_counter = 0

    def compile_input_file(self):
        """
        in this function we read from the list we have and from there we do based
        on what where is in the list
        """
        while self.has_more_lines():
            self.curr_items = self.input_lines[self.curr_line].split()
            if self.curr_items[0] == "<tokens>":
                self.curr_line += 1
                continue
            if self.curr_items[1] == "class":
                self.compile_class()

    def has_more_lines(self):
        """
        this function checks if there is more lines in the list
        """
        return self.curr_line < len(self.input_lines) - 1

    def advance(self, steps: int):
        self.curr_line += steps

    def writing_next_lines(self, num):
        """
        in this function we write the new line based on the num we got
        """
        while num != 0:
            self.output_file.write(self.input_lines[self.curr_line] + "\n")
            self.curr_line += 1
            num -= 1

    def compile_class(self) -> None:
        """Compiles a complete class."""

        self.writing_next_lines(3)
        self.curr_items = self.input_lines[self.curr_line].split()
        while self.curr_items[1] != "}":
            if self.curr_items[1] in SUBROUTINE_DEC:
                self.compile_subroutine()
            if self.curr_items[1] in CLASS_VARDEC:
                self.compile_class_var_dec()
            self.curr_items = self.input_lines[self.curr_line].split()
        self.writing_next_lines(1)
        self.output_file.write("</class>" + "\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""

        self.compile_var_dec()

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""

        kind = self.get_item()
        self.advance(1)
        type = self.get_item()
        self.advance(1)
        name = self.get_item()
        self.symbol_table.define(name, type, kind)
        self.advance(1)
        while self.curr_items[1] == ",":
            self.advance(1)
            name = self.get_item()
            self.symbol_table.define(name, type, kind)
            self.advance(1)
        self.advance(1)  # for  ;

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self.output_file.write("<subroutineDec>" + "\n")
        self.writing_next_lines(4)
        self.compile_parameter_list()
        self.output_file.write("<subroutineBody>" + "\n")
        self.writing_next_lines(1)
        self.curr_items = self.input_lines[self.curr_line].split()
        while self.curr_items[1] == "var":
            self.output_file.write("<varDec>" + "\n")
            self.compile_var_dec()
            self.output_file.write("</varDec>" + "\n")
            self.curr_items = self.input_lines[self.curr_line].split()
        self.compile_statements()
        self.writing_next_lines(1)
        self.output_file.write("</subroutineBody>" + "\n")
        self.output_file.write("</subroutineDec>" + "\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.output_file.write("<parameterList>" + "\n")
        self.curr_items = self.input_lines[self.curr_line].split()
        while self.curr_items[1] != ")":
            self.writing_next_lines(2)
            self.curr_items = self.input_lines[self.curr_line].split()
            if self.curr_items[1] == ",":
                self.writing_next_lines(1)
                self.curr_items = self.input_lines[self.curr_line].split()
        self.output_file.write("</parameterList>" + "\n")
        self.writing_next_lines(1)

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.output_file.write("<statements>" + "\n")
        self.curr_items = self.input_lines[self.curr_line].split()
        while self.curr_items[1] != "}":
            if self.curr_items[1] == "do":
                self.compile_do()
            elif self.curr_items[1] == "let":
                self.compile_let()
            elif self.curr_items[1] == "while":
                self.compile_while()
            elif self.curr_items[1] == "if":
                self.compile_if()
            elif self.curr_items[1] == "return":
                self.compile_return()
            self.curr_items = self.input_lines[self.curr_line].split()
        self.output_file.write("</statements>" + "\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.output_file.write("<doStatement>" + "\n")
        self.writing_next_lines(1)
        self.compile_subroutin_call()
        self.writing_next_lines(1)
        self.output_file.write("</doStatement>" + "\n")

    """  done  """
    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.advance(1)  # for let
        name = self.get_item()
        self.advance(1)  # for var_name
        if self.get_item() == "[":
            self.compile_let_arr(name)
        else:
            self.advance(1)  # for =
            self.compile_expression()
            self.push_pop_var("pop", name)
        self.advance(1)  # for ;

    def compile_let_arr(self, name):
        """Helper for compiling let array statement"""

        self.advance(1)  # for [
        self.push_pop_var(PUSH, name)
        self.compile_expression()
        self.advance(2)   # for ] =
        self.vm_writer.write_arithmetic("add")
        self.vm_writer.write_pop("temp", 0)
        self.vm_writer.write_pop("pointer", 1)
        self.vm_writer.write_push("temp", 0)
        self.vm_writer.write_pop(THAT, 0)

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""

        self.advance(2)  # for if (
        self.compile_expression()
        self.advance(2)  # for ) {
        self.vm_writer.write_arithmetic("not")
        self.vm_writer.write_if("IF_1_" + str(self.label_counter))
        self.compile_statements()
        self.advance(1)  # for }
        self.vm_writer.write_goto("IF_2_" + str(self.label_counter))
        self.vm_writer.write_label("IF_1_" + str(self.label_counter))
        if self.get_item() == "else":
            self.advance(2)  # for else {
            self.compile_statements()
            self.advance(1)  # for }
        self.vm_writer.write_label("IF_2_" + str(self.label_counter))

    """  done  """
    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.vm_writer.write_label("WHILE_1_" + str(self.label_counter))
        self.advance(2)  # for while (
        self.compile_expression()
        self.advance(2)  # for ) {
        self.vm_writer.write_arithmetic("not")
        self.vm_writer.write_if("WHILE_2_" + str(self.label_counter))
        self.compile_statements()
        self.advance(1)  # for }
        self.vm_writer.write_goto("WHILE_1_" + str(self.label_counter))
        self.vm_writer.write_label("WHILE_2_" + str(self.label_counter))

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.output_file.write("<returnStatement>" + "\n")
        self.writing_next_lines(1)
        self.curr_items = self.input_lines[self.curr_line].split()
        if self.curr_items[1] == ";":
            self.writing_next_lines(1)
        else:
            self.compile_expression()
            self.writing_next_lines(1)
        self.output_file.write("</returnStatement>" + "\n")



    # handle functions!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def compile_expression(self) -> None:
        """Compiles an expression."""

        item1 = self.get_item()
        if item1 == ";" or item1 == "," or item1 == ")":
            self.advance(1)
            return
        elif item1 == '(':
            self.compile_parenthesis()
            self.compile_expression()
        elif item1.isdigit():
            self.vm_writer.write_push("constant", int(item1))
            self.advance(1)
            self.compile_expression()
        elif item1 in BINARY_OP or item1 in UNARY_OPERATORS:
            self.advance(1)
            self.compile_expression()
            self.vm_writer.write_arithmetic(item1)           # is it legal? fix it!!!!!!!!!!!!!
        else:
            # var or func
            self.compile_var_or_func()

    def compile_var_or_func(self):
        """Compiles an variable or function expression."""

        item1 = self.get_item()
        if self.symbol_table.check_if_var(item1):
            self.push_pop_var(PUSH, item1)
            self.advance(1)
            if self.get_item() == '.':
                self.advance(1)
                self.compile_function_exp()
            self.compile_expression()
        else:
            self.advance(1)
            if self.get_item() == '.':
                # do something with library name!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.advance(1)
            self.compile_function_exp()

    def compile_function_exp(self):
        """Compiles an function expression."""

        name = self.get_item()
        self.advance(1)  # for (
        num_of_vars = self.compile_expression_list()
        self.advance(1)  # for )
        self.vm_writer.write_call(name, num_of_vars)

    def compile_parenthesis(self):
        """Compiles an parenthesis expression."""
        self.advance(1)
        self.compile_expression()


    def compile_subroutin_call(self):
        pass




    def compile_term(self) -> None:
        """
        Compiles a term.
        """
        self.output_file.write("<term>" + "\n")
        self.curr_items = self.input_lines[self.curr_line].split()
        if self.curr_items[1] in LIST_WORDS or self.curr_items[0] == INT_CONT or self.curr_items[0] == STR_CONT:
            self.writing_next_lines(1)
        elif self.curr_items[1] == "(":
            self.writing_next_lines(1)
            self.compile_expression()
            self.writing_next_lines(1)
        elif self.curr_items[1] in UNARY_OPERATORS:
            self.writing_next_lines(1)
            self.compile_term()
        elif self.input_lines[self.curr_line + 1].split()[1] == "." or self.input_lines[self.curr_line + 1].split()[1] == "(":
            self.compile_subroutin_call()
        elif self.input_lines[self.curr_line + 1].split()[1] == "[":
            self.writing_next_lines(2)
            self.compile_expression()
            self.writing_next_lines(1)
        else:
            self.writing_next_lines(1)
        self.output_file.write("</term>" + "\n")

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        vars_counter = 0
        while self.get_item() != ")":
            self.compile_expression()
            vars_counter += 1
        return vars_counter

    def get_item(self) -> str:
        """Gets the item from xml line"""
        return self.input_lines[self.curr_line].split()[1]

    def push_pop_var(self, command: str, name: str) -> None:
        segment = self.symbol_table.type_of(name)
        index = self.symbol_table.index_of(name)
        if command == PUSH:
            self.vm_writer.write_push(segment, index)
        else:
            self.vm_writer.write_pop(segment, index)

