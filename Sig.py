#!/usr/bin/python3

import sys, time, os
import regex as re
import random
import Module as md
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


class Signal(object):
    def __init__(self, sig_type, name, size=1, position=None):
        self.type = sig_type
        self.name = name
        self.size = size
        self.position = position

    def print_signal(self):
        print("\tName: ", self.name,",\tsize: ", self.size, "\ttype: ", self.type)


def signal_search(pattern, sig_type, code):
    dictionary = {}
    size = 1
    matches = pattern.finditer(code)
    for match in matches:
        if match.group(2) != None:
            size = int(match.group(2))
        names = match.group(3)
        in_name_matches = re.finditer(r"\w+", names)
        for name in in_name_matches:
            if(name.group() == r"k\d+"):
                print("Inputs are starting with 'k'!!!")
                exit()
            dictionary[name.group()] = Signal(sig_type, name.group(), size)
        size = 1
    return dictionary
