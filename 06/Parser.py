"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads and assembly language
    command, parses it, and provides convenient access to the commands
    components (fields and symbols). In addition, removes all white space and
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_file.read().splitlines()
        self.input_lines = input_file.read().splitlines()
        self.curr_line = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!

        return self.curr_line < len(self.input_lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        self.curr_line = self.curr_line + 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """

        self.input_lines[self.curr_line] = self.input_lines[self.curr_line].replace(" ", "")
        if "//" in self.input_lines[self.curr_line]:
            self.input_lines[self.curr_line] = self.input_lines[self.curr_line].split("//")[0]
        if not self.input_lines[self.curr_line]:
            return "empty"
        if self.input_lines[self.curr_line][0] == "":
            return "empty"
        elif self.input_lines[self.curr_line][0] == "(":
            return "L_COMMAND"
        elif self.input_lines[self.curr_line][0] == "/":
            return "docstring"
        elif self.input_lines[self.curr_line][0] == "@":
            return "A_COMMAND"
        else:
            return "C_COMMAND"  # need to check all options

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or
            "L_COMMAND".
        """
        if self.input_lines[self.curr_line][0] == "(":
            return self.input_lines[self.curr_line][1:].split(")")[0]

        # @command
        return self.input_lines[self.curr_line][1:]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if "=" in self.input_lines[self.curr_line]:
            return self.input_lines[self.curr_line].split("=")[0]
        return "null"

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if "=" in self.input_lines[self.curr_line]:
            temp = self.input_lines[self.curr_line].split("=")[1]
            if ";" in temp:
                return temp.split(";")[0]
            return temp
        # else ";" has to be
        return self.input_lines[self.curr_line].split(";")[0]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if ";" in self.input_lines[self.curr_line]:
            return self.input_lines[self.curr_line].split(";")[1]
        return "null"