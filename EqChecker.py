#!/usr/bin/python3

import sys, time, os
from datetime import datetime
import random
import regex as re
import Sig as sg 
import Module as md

key_map_string = r"\{([a-zA-Z0-9_[\].-]+)\}"
key_string = r"[10x]+"

pattern_key_port_map = re.compile(key_map_string)
pattern_key = re.compile(key_string)

def extract_keys(obj):
    count = 0
    concatinator = ", "
    key_inputs = []
    with open("keyVectors.txt","r") as fpk:
        key_vector_string = fpk.read()
    with open("keyPortMapping.txt","r") as fpm:
        port_mapping_string = fpm.read()
    
    port_map_matches = pattern_key_port_map.finditer(port_mapping_string)
    if port_map_matches:
        for match in port_map_matches:
            key_inputs.append(match.group(1))
    
    key_matches = pattern_key.finditer(key_vector_string)
    if key_matches:
        for match in key_matches:
            count = count+1
            obj.key_values[(concatinator.join(key_inputs), count)] = match.group()

    return obj


def create_eq_checker_file(obf, inout_switch = 0):
    now = datetime.now()
    dt1 = now.strftime("%b/%d/%Y - %H:%M:%S")
    file_string = "\n"
    key_string = ""
    file_string = file_string + "/" * 100 + "\n" 
    file_string = file_string + "/" * 2 + " Top module file\n"
    file_string = file_string + "/" * 2 + " File : Top connecting obfuscated and unobsfuscated designs for Functional\Equivalence checking\n"        
    file_string = file_string + "/" * 2 + " Version : Vtool 1.04a\n" 
    file_string = file_string + "/" * 2 + " Date and time : "+ dt1 +"\n" 
    file_string = file_string + "/" * 2 + " Created by Venkat and Maneesh\n" 
    file_string = file_string + "/" * 100 + "\n"
    file_string = file_string + "\n\nmodule "

    org_name, org_value = random.choice(list(obf.original_module.items()))
    mod_org = org_value

    print(mod_org.print_module())

    obf_name, obf_value = random.choice(list(obf.obfuscated_module.items()))

    file_string = file_string + org_name + "_verify_top" + " ( "
    for name in mod_org.inputs.keys():
        file_string = file_string + name + ", "
    if "verification_output" not in set(mod_org.outputs.keys()):
        file_string = file_string + "verification_output, "
    else:
        file_string = file_string + "verification_output_tmp, "
    if(inout_switch == 1):
        for name in mod_org.inouts.keys():
            file_string = file_string + name + ", "
    file_string = file_string[0:-2] + " );\n\n"
    for name, value in mod_org.inputs.items():
        if(value.size > 1):
            file_string = file_string + "input wire [" + str(value.size) + ":0] " + name + " ;\n"
        else:
            file_string = file_string + "input wire " + name + " ;\n"
    file_string = file_string[0:-2] + ";\n\n"
    file_string = file_string + "output "
    if "verification_output" not in set(mod_org.outputs.keys()):
        file_string = file_string + "verification_output;\n\n"
    else:
        file_string = file_string + "verification_output_tmp;\n\n"
    file_string = file_string + "wire "
    for name in mod_org.outputs.keys():
        file_string = file_string + name + "_obf" + ", "
    for name in mod_org.outputs.keys():
        file_string = file_string + name + ", "
    file_string = file_string[0:-2] + ";\n\n"
    if(inout_switch == 1 and (len(mod_org.inouts) > 0)):
        file_string = file_string + "inout "
        for name in mod_org.inouts.keys():
            file_string = file_string + name + ", "
        file_string = file_string[0:-2] + ";\n\n"
    
    file_string = file_string + org_name + " original_design" +" ( "
    for name in mod_org.inputs.keys():
        file_string = file_string + "." +name +"("+name+ "), "
    for name in mod_org.outputs.keys():
        file_string = file_string + "." +name +"("+name+ "), "
    if(inout_switch == 1):
        for name in mod_org.inouts.keys():
            file_string = file_string + "." +name +"("+name+ "), "
    file_string = file_string[0:-2] + " );\n\n"
    
    file_string = file_string + obf_name + " obfuscated_design" +" ( "
    for name in mod_org.inputs.keys():
        file_string = file_string + "." +name +"("+name+ "), "
    for name in mod_org.outputs.keys():
        file_string = file_string + "." + name +"("+ name + "_obf" + "), "
    if(inout_switch == 1):
        for name in mod_org.inouts.keys():
            file_string = file_string + "." +name +"("+name+ "), "
    file_string = file_string[0:-2] + " );\n\n"
    file_string = file_string + "assign verification_output = "
    for name in mod_org.outputs.keys():
        file_string = file_string + "(" + name + "_obf ^ " + name + " ) | "
    file_string = file_string[0:-2] + ";\n\n"
    file_string = file_string + "endmodule\n\n"
    with open(obf.original_path[:-2]+"_verify_top.v", "w") as fpvt:
        fpvt.write(file_string)


def create_assertions_file(obf, inout_switch = 0):
    verification_signal = "verification_output"
    obf = extract_keys(obf)
    now = datetime.now()
    dt1 = now.strftime("%b/%d/%Y - %H:%M:%S")
    file_string = "\n"
    key_string = ""
    file_string = file_string + "/" * 100 + "\n" 
    file_string = file_string + "/" * 2 + " Assertions file\n"
    file_string = file_string + "/" * 2 + " File : File contains all the assertions and assumptions to perform equivalence checking using JG\n"        
    file_string = file_string + "/" * 2 + " Version : Vtool 1.04a\n" 
    file_string = file_string + "/" * 2 + " Date and time : "+ dt1 +"\n" 
    file_string = file_string + "/" * 2 + " Created by Venkat and Maneesh\n" 
    file_string = file_string + "/" * 100 + "\n"
    file_string = file_string + "\n\nmodule "
    for mod_name, value in obf.original_module.items():
        file_string = file_string + mod_name + "_assertions" + " ( "
        mod_org = value
        for name in mod_org.inputs.keys():
            file_string = file_string + name + ", "
        if "verification_output" not in set(mod_org.outputs.keys()):
            file_string = file_string + "verification_output, "
        else:
            file_string = file_string + "verification_output_tmp, "
            verification_signal = "verification_output_tmp"
        if(inout_switch == 1):
            for name in mod_org.inouts.keys():
                file_string = file_string + "." +name +"("+name+ "), "
        file_string = file_string[0:-2] + " );\n\n"
        for name, value in mod_org.inputs.items():
            if(value.size > 1):
                file_string = file_string + "input wire [" + str(value.size) + ":0] " + name + " ;\n"
            else:
                file_string = file_string + "input wire " + name + " ;\n"
        file_string = file_string + "input wire " + verification_signal + " ;\n "
        if(inout_switch == 1 and (len(mod_org.inouts) > 0)):
            for name, value in mod_org.inouts.items():
                if(value.size > 1):
                    file_string = file_string + "inout wire [" + str(value.size) + ":0] " + name + " ;\n"
                else:
                    file_string = file_string + "inout wire " + name + " ;\n"
        file_string = file_string + "\n"
        for (key_set, cycle), value in obf.key_values.items():
            file_string = file_string + "property key_at_cycle_" + str(cycle) + ";\n\t( ##"+ str(cycle) +" {" + key_set + "} == "+ str(len(value)) + "\'b" + str(value) + " );\nendproperty\n\n"
        for (key_set, cycle), value in obf.key_values.items():
            file_string = file_string + "constrain_key_cycle_" + str(cycle) + " : assume property ( key_at_cycle_" + str(cycle) + " );\n" 
        file_string = file_string + "\nproperty eq_output;\n\t ##"+ str(len(obf.key_values)+1) +" (" + verification_signal + " == 0);\nendproperty\n\n"
        file_string = file_string + "check_eq_output : assert property (eq_output);\n\n"
        file_string = file_string + "endmodule\n\n"
        file_string = file_string + "bind " + mod_name + "_verify_top " + mod_name + "_assertions assertions( "
        for name in mod_org.inputs.keys():
            file_string = file_string + "." +name +"("+name+ "), "
        if "verification_output" not in set(mod_org.outputs.keys()):
            file_string = file_string + ".verification_output(verification_output), "
        else:
            file_string = file_string + ".verification_output_tmp(verification_output_tmp), "
        if(inout_switch == 1):
            for name in mod_org.inouts.keys():
                file_string = file_string + "." + name + "(" + name + "), "
        file_string = file_string[0:-2] + " );\n\n"
    with open(obf.original_path[0:-2]+"_assertions.sva", "w") as fpa:
        fpa.write(file_string)

