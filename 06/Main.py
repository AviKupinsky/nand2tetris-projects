"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    
    # init
    parser = Parser(input_file)
    symbol_table = SymbolTable()
    # first Pass
    num_of_commands = 0
    while parser.has_more_commands():
        if parser.command_type() == "L_COMMAND":
            symbol_table.add_entry(parser.symbol(),num_of_commands)
        elif parser.command_type() == "A_COMMAND" or parser.command_type() == "C_COMMAND":
            num_of_commands += 1
        parser.advance()

    # second Pass
    parser.curr_line = 0

    while parser.has_more_commands():
        if parser.command_type() == "A_COMMAND":
            symbol = parser.symbol()
            if symbol.isdigit():
                output_file.write("0" + symbol_table.convert_to_bin(int(symbol)))
                print("0" + symbol_table.convert_to_bin(int(symbol)))
            elif not symbol_table.contains(symbol):
                symbol_table.add_new_symbol(symbol)
                output_file.write(symbol_table.get_address(symbol))
                print(symbol_table.get_address(symbol))
            else:
                output_file.write(symbol_table.get_address(symbol))
                print(symbol_table.get_address(symbol))

        elif parser.command_type() == "C_COMMAND":
            comp = parser.comp()
            dest = parser.dest()
            jump = parser.jump()
            output_file.write("111" + Code.comp(comp) + Code.dest(dest) + Code.jump(jump))
            print("111" + Code.comp(comp) + Code.dest(dest) + Code.jump(jump))
        parser.advance()
    input_file.close()
    output_file.close()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)

    print(10.)