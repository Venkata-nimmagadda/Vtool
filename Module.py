#!/usr/bin/python3

import sys, time, os
import regex as re
import random
import Sig as sg 
import NetlistExtractor as ne

# REGEX patterns
line_comments_string = r'//.*'
block_comments_string = r'/[*]((.|\n)*?)[*]/'
input_string = r"input\s+(\[(\d+):\d\]\s+)?([\w+,?\s*]+);"
output_string = r"output\s+(\[(\d+):\d\]\s+)?([\w+,?\s*]+);"
inout_string = r"inout\s+(\[(\d+):\d\]\s+)?([\w+,?\s*]+);"
wire_string = r"wire\s+(\[(\d+):\d\]\s+)?([\w+,?\s*]+);"
reg_string = r"reg\s+(\[(\d+):\d\]\s+)?([\w+,?\s*]+);"
module_string = r"module\s(\w+)\s?((\s|(?!endmodule).)*)endmodule"
parameters_string = r"(parameter|localparam)\s+([(\w+\s*=\s*\d+\'\w+\s*,?;?\s*)(\w+\s*=\s*\d+\s*,?;?\s*)]+)"
parem_string = r"(\w+)(\s*=\s*)(\d+[']\w+\s*,?;?|\d+\s*,?;?)"
includes_string = r'`include\s+["](.+)["]'
module_instance_string = r"\s((?!([module]))\w+)\s+(\w+)\s+\(((\s*\.(\w+)\s*\(\s*(\{?(\s*\w+\s*(\[\s*\d+(\s*:\s*\d+)?\s*\])*\,?)+\}?)\s*\)\s*,?)+)\);"
port_map_string = r"(\s*\.(\w+)\s*\(\s*(\{?(\s*\w+\s*(\[\s*\d+(\s*:\s*\d+)?\s*\])*\,?)+\}?)\s*\)\s*,?)"

pattern_line_comment = re.compile(line_comments_string)
pattern_block_comment = re.compile(block_comments_string)
pattern_input = re.compile(input_string)
pattern_output = re.compile(output_string)
pattern_inout = re.compile(inout_string)
pattern_wire = re.compile(wire_string)
pattern_reg = re.compile(reg_string)
pattern_module = re.compile(module_string)
pattern_parameter = re.compile(parameters_string)
pattern_include = re.compile(includes_string)
pattern_parem = re.compile(parem_string)
pattern_module_instance = re.compile(module_instance_string)
pattern_port_map = re.compile(port_map_string)



class Module(object):
    def __init__(self, name):
        self.name = name
        self.instance_name = ""
        self.gates = {}
        self.inputs = {}
        self.outputs = {}
        self.inouts = {}
        self.wires = {}
        self.regs = {}
        self.code = ""


    def module_extractor(self):
        self.inputs = sg.signal_search(pattern_input, "input", self.code)
        self.outputs = sg.signal_search(pattern_output, "output", self.code)
        self.inout = sg.signal_search(pattern_inout, "inout", self.code)
        self.wires = sg.signal_search(pattern_wire, "wire", self.code)
        self.regs = sg.signal_search(pattern_reg, "reg", self.code)
        return
    

    def print_module(self):
        print("\tModule Name: ", self.name)
        print("\n======================================================= GATES ==========================================================\n")
        for value in self.gates.values():
            value.print_gate()

        print("\n======================================================= INPUTS ==========================================================\n")
        for value in self.inputs.values():
            value.print_signal()

        print("\n======================================================= OUTPUTS ==========================================================\n")
        for value in self.outputs.values():
            value.print_signal()

        print("\n======================================================= INOUTS ==========================================================\n")
        for value in self.inouts.values():
            value.print_signal()

        print("\n======================================================= WIRES ==========================================================\n")
        for value in self.wires.values():
            value.print_signal()

        print("\n======================================================= REGS ==========================================================\n")
        for value in self.regs.values():
            value.print_signal()
            
        print("\n======================================================= done ==========================================================\n")
