"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        self.output_file = output_stream
        self.curr_file_name = ""
        self.label_counter = 0
        self.function_counter = 0


    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self.curr_file_name = filename

    def close(self) -> None:
        """Closes the output file."""
        self.output_file.close()


    def write_init(self):
        """

        :return:
        """
        self.output_file.write("@256\n" + "D=A\n" + "@SP\n" + "M=D\n")
        self.write_call("Sys.init", 0)

    def write(self, args: list):
        """

        :param args:
        :return:
        """
        self.output_file.write("//")
        for i in args:
            self.output_file.write(str(i) + " ")
        self.output_file.write("\n")
        command_type = args[0]
        if command_type == "C_ARITHMETIC":
            self.write_arithmetic(args[1])
        elif command_type in ["C_PUSH", "C_POP"]:
            self.write_push_pop(args[1], args[2], args[3])
        elif command_type == "C_LABEL":
            self.write_label(args[2])
        elif command_type == "C_GOTO":
            self.write_go_to(args[2])
        elif command_type == "C_IF":
            self.write_if(args[2])
        elif command_type == "C_FUNCTION":
            self.write_function(args[2], args[3])
        elif command_type == "C_CALL":
            self.write_call(args[2], args[3])
        elif command_type == "C_RETURN":
            self.write_return()


    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """

        op_map = {'add': '+', 'sub': '-', 'and': '&', 'or': '|', 'neg': '-', 'not': '!',
                  'eq': 'JEQ', 'lt': 'JLT', 'gt': 'JGT', "shiftleft": "<<", "shiftright": ">>"}
        binary_op = ["add", "sub", "and", "or"]
        unary_op = ["neg", "not"]
        size_compare_op = ["eq", "gt", "lt"]
        shifts = ["shiftleft", "shiftright"]
        txt = ""
        # Your code goes here!
        if command in binary_op:
            txt = self.write_binary_op(command, op_map)
        elif command in unary_op:
            txt = self.write_unary_op(command, op_map)
        elif command in shifts:
            txt = self.write_shifts(command, op_map)
        elif command in size_compare_op:
            txt = self.write_size_compare_op(command)
            self.label_counter += 1
        self.output_file.write(txt + "\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """

        txt = ""
        if segment in ["local", "argument", "this", "that"]:
            txt = self.write_lcl_arg_this_that(command, segment, index)
        elif segment == "constant":
            txt = self.write_constant(index)
        elif segment == "static":
            txt = self.write_static(command, index)
        elif segment == "temp":
            txt = self.write_temp(command, index)
        elif segment == "pointer":
            txt = self.write_pointer(command, index)
        self.output_file.write(txt + "\n")

    def write_label(self, label: str):
        """

        :param label:
        :return:
        """
        self.output_file.write("(" + label + ")\n\n")

    def write_go_to(self, label: str):
        """

        :param label:
        :return:
        """
        self.output_file.write("@" + label + "\n0;JEQ\n\n")

    def write_if(self, label: str):
        """

        :param label:
        :return:
        """
        self.output_file.write("@SP\nAM=M-1\nD=M\n@" + label + "\nD;JNE\n\n")

    def write_function(self, func_name: str, num_vars: int):
        """

        :param func_name:
        :param num_vars:
        :return:
        """
        self.write_label(func_name)
        txt = ""
        while num_vars != 0:
            txt += self.write_constant(0)
            num_vars -= 1

        self.output_file.write(txt + "\n")

    def write_call(self, func_name: str, num_vars: int):
        """

        :param func_name:
        :param num_vars:
        :return:
        """
        txt = "@function_return" + str(self.function_counter) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        txt += "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        txt += "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        txt += "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        txt += "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        txt += "@SP\nD=M\n@5\nD=D-A\n @" + str(num_vars) + "\nD=D-A\n@ARG\nM=D\n"
        txt += "@SP\nD=M\n@LCL\nM=D\n"
        self.output_file.write(txt)
        self.write_go_to(func_name)
        self.write_label("function_return" + str(self.function_counter))
        self.function_counter += 1



    def write_return(self):
        """

        :return:
        """
        # r13 = LCL, R14 = *(R13-5)
        txt = "@LCL\nD=M\n@R13\nM=D\n@5\nD=D-A\nA=D\nD=M\n@R14\nM=D\n"
        txt += "@SP\n AM=M-1\nD=M\n@ARG\nA=M\nM=D\n"
        txt += "@ARG\nD=M+1\n@SP\nM=D\n"
        txt += "@R13\nD=M-1\nA=D\nD=M\n@THAT\nM=D\n"
        txt += "@R13\nD=M\n@2\nD=D-A\nA=D\nD=M\n@THIS\nM=D\n"
        txt += "@R13\nD=M\n@3\nD=D-A\nA=D\nD=M\n@ARG\nM=D\n"
        txt += "@R13\nD=M\n@4\nD=D-A\nA=D\nD=M\n@LCL\nM=D\n"
        txt += "@14\nA=D\n0;JEQ\n\n"
        self.output_file.write(txt)

    # write push/pop functions

    def write_lcl_arg_this_that(self, command: str, segment: str, index: int) -> str:
        """

        :param command:
        :param segment:
        :param index:
        :return:
        """
        pointer_map = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
        txt = "@" + pointer_map[segment] + "\nD=M\n@" + str(index) + "\nD=D+A\n@13\nM=D\n"
        if command == "pop":
            return txt + "@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n"
        elif command == "push":
            return txt + "A=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    def write_constant(self, index: int) -> str:
        """

        :param index:
        :return:
        """
        return "@" + str(index) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    def write_static(self, command: str, index: int) -> str:
        """

        :param command:
        :param index:
        :return:
        """
        file = self.curr_file_name + "." + str(index)
        if command == "pop":
            return "@SP\nM=M-1\nA=M\nD=M\n@" + file + "\n M=D\n"
        elif command == "push":
            return "@" + file + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

    def write_temp(self, command: str,  index: int) -> str:
        """

        :param command:
        :param index:
        :return:
        """
        txt = "@5\n D=A\n@" + str(index) + "\nD=D+A\n@13\nM=D\n"
        if command == "pop":
            return txt + "@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D\n"
        elif command == "push":
            return txt + "A=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    def write_pointer(self, command: str,  index: int) -> str:
        """

        :param command:
        :param index:
        :return:
        """
        pointer = "THIS" if index == 0 else "THAT"
        if command == "pop":
            return "@SP\nM=M-1\n@SP\nA=M\nD=M\n@" + pointer + "\nM=D\n"
        elif command == "push":
            return "@" + pointer + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    # write arithmetic functions

    def write_binary_op(self, command: str, op_map: dict) -> str:
        """

        :param command:
        :param op_map:
        :return:
        """
        return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M" + op_map[command] + "D\n"

    def write_unary_op(self, command: str, op_map: dict) -> str:
        """

        :param command:
        :param op_map:
        :return:
        """
        return "@SP\nA=M-1\nM=" + op_map[command] + "M\n"

    def write_shifts(self, command: str, op_map: dict) -> str:
        """

        :param command:
        :param op_map:
        :return:
        """
        return "@SP\nA=M-1\nM=M" + op_map[command] + "\n"

    def write_size_compare_op(self, command: str) -> str:
        """

        :param command:
        :return:
        """
        # templates
        def label_part(index: int): return "(part" + str(index) + com_i + ")\n"
        def go_to_part(index: int): return "@part" + str(index) + com_i + "\n"
        sp_to_d = "@SP\nAM=M-1\nD=M\n"
        temp_addr = "@R13\n"
        com_i = command + str(self.label_counter)
        end_true = "D=-1\n@" + com_i + "end\n0;JMP\n"
        end_false = "D=0\n@" + com_i + "end\n0;JMP\n"

        not_con_map = {"eq": "JNE", "lt": "JGE", "gt": "JLE"}
        # if y >= 0 jump to part 6
        part1 = sp_to_d + temp_addr + "M=D\n" + go_to_part(6) + "D;JGE\n"
        # else if x>=0 jump to part 5
        part2 = sp_to_d + go_to_part(5) + "D;JGE\n"
        # else(x<0 and y<0)  if not condition jump to part4 and write false and if condition write true
        part3 = temp_addr + "D=D-M\n" + go_to_part(4) + "D;" + not_con_map[command] + "\n" + end_true
        # part 4 writing false
        part4 = label_part(4) + end_false
        # part 5 if y<0 and x>=0
        part5 = label_part(5) + end_false if command in ["eq", "lt"] else label_part(5) + end_true
        # part 6  y>=0 (R13 = y) # if x>=0 jump to part 7
        part6 = label_part(6) + sp_to_d + go_to_part(7) + "D;JGE\n"
        # else y>=0 and x<0
        part6 = part6 + end_false if command in ["eq", "gt"] else part6 + end_true
        # part 7  y>=0 and x>=0
        part7 = label_part(7) + temp_addr + "D=D-M\n@part8" + com_i + "\nD;" + not_con_map[command] + "\n" + end_true
        # writing false
        part8 = label_part(8) + end_false
        # end
        end = "(" + com_i + "end)\n@SP\nAM=M+1\nA=A-1\nM=D\n"
        return part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + end
