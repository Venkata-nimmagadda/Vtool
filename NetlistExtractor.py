#!/usr/bin/python3

import sys, time, os
from datetime import datetime
import regex as re
import random
import EqChecker as ec
import Sig as sg 
import Module as md


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



class Netlist_graph_class(object):
    
    def __init__(self):
        self.script_path = ""
        self.original_path = sys.argv[1]
        self.obfuscated_path = sys.argv[2]
        self.directory = sys.argv[3]
        self.key_values = {}
        self.original_module = {}
        self.obfuscated_module = {}
        self.top_module = ""
        self.parameters = []
        self.includes = []
        self.parser()

    def file_reader(self, path):
        with open(path, "r") as fp:
            string = fp.read()
        return string
    
    def parser(self):

        # Reading the original and obfuscated netlists

        obfucated_design_string = self.file_reader(self.obfuscated_path)
        obfucated_design_string = pattern_line_comment.sub( "", obfucated_design_string)
        obfucated_design_string = pattern_block_comment.sub( "", obfucated_design_string)
        matches = pattern_module.finditer(obfucated_design_string)
        for match in matches:
            code = match.group(2)
            module_name = match.group(1)
            gen_module = md.Module(module_name)
            gen_module.code = code
            gen_module.module_extractor()
            self.obfuscated_module[module_name] = gen_module

        if(len(self.obfuscated_module) != 1):
            print("Error: There should be only one module in the synthesized code.\n\t there are %d modules in obfuscated design", len(self.obfuscated_module))
            exit()

        original_design_string = self.file_reader(self.original_path)
        original_design_string = pattern_line_comment.sub( "", original_design_string)
        original_design_string = pattern_block_comment.sub( "", original_design_string)
        matches = pattern_module.finditer(original_design_string)
        for match in matches:
            code = match.group(2)
            module_name = match.group(1)
            gen_module = md.Module(module_name)
            gen_module.code = code
            gen_module.module_extractor()
            self.original_module[module_name] = gen_module
            

        if(len(self.original_module) != 1):
            print("Error: There should be only one module in the synthesized code.\n\t there are %d modules in original design", len(self.original_module))
            exit()

        return

    def print_netlist(self):

        print("\n File path: ", self.netlist_file_path)
        print("\n Library path: ", self.library_file_path)
        print("\n")
        for key , value in self.graph.items():
            print(key, "\t:\t", value)

        print(self.gate_map)

        for key , value in self.modules.items():
            value.print_module()



if __name__ == "__main__":
    
    obj = Netlist_graph_class()
    ec.create_eq_checker_file(obj)
    ec.create_assertions_file(obj)



