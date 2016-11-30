import sys, os, time
import subprocess

verbose = False

def main():
    if (len(sys.argv) < 3):
        usage()
        exit()
    permute_command = sys.argv[2]
    cspec_path = sys.argv[1]
    flags = ""
    if (len(sys.argv) == 4):
        flags = sys.argv[3]
    validate_args(permute_command, cspec_path, flags)
    validate_cluster_spec(cspec_path)
    if (flags == "-v"):
        global verbose
        verbose = True
    if (permute_command == "gen"):
        generate(cspec_path)
    elif (permute_command == "launch"):
        launch(cspec_path)
    elif (permute_command == "auto"):
        generate(cspec_path)
        launch(cspec_path)
    else:
        pass
        
def if_verbose(message):
    global verbose
    if (verbose):
        print message
    
def generate(cspec_path):
    permuters = load_permutes(cspec_path)
    concisePrintMap = load_concisePrintMap(cspec_path)
    keyValMap = load_keyValMap(cspec_path)
    qsub_commands = load_qsub_commands(cspec_path, keyValMap)
    commands = load_commands(cspec_path, keyValMap)
    
    permute_dictionary_list = expand_permutations(permuters)
    generate_scripts(keyValMap,commands, permute_dictionary_list, qsub_commands, concisePrintMap)
    
def launch(cspec_path):
    permuters = load_permutes(cspec_path)
    concisePrintMap = load_concisePrintMap(cspec_path)
    keyValMap = load_keyValMap(cspec_path)
    qsub_commands = load_qsub_commands(cspec_path, keyValMap)
    commands = load_commands(cspec_path, keyValMap)
    
    permute_dictionary_list = expand_permutations(permuters)
    launch_scripts(keyValMap, permute_dictionary_list, concisePrintMap)
    
def load_commands(cspec_path, keyValMap):
    f = open(cspec_path, 'r')
    commands = []
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("command:")):
            if_verbose("  processing command line - {0}".format(line))
            x, this_command = line.split(":")
            commands.append(this_command)
            #resolve_command(this_command, keyValMap, commands)
        else:
            pass
    f.close()
    return commands

def load_permutes(cspec_path):
    f = open(cspec_path, 'r')
    permuters = {}
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("permute:")):
            if_verbose("  processing permute line - {0}".format(line))
            foo, permuteKey, permute_list_string = line.split(':')
            if (permute_list_string.find(" ") != -1):
                permute_start, permute_end = permute_list_string.split(" ")
                permute_list = range(int(permute_start), int(permute_end)+1)
                permute_list = map(str, permute_list)
            else:
                permute_list = permute_list_string.split(",")
            permuters[permuteKey] = permute_list
        else:
            pass
    f.close()
    return permuters

def load_concisePrintMap(cspec_path):
    f = open(cspec_path, 'r')
    concisePrintMap = {}
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("concise_print:")):
            if_verbose("  processing concise_print line - {0}".format(line))
            command, conciseKeyVal = line.split(":")
            key, val = conciseKeyVal.split(",")
            concisePrintMap[key] = val
        else:
            pass
    f.close()
    return concisePrintMap
    
def load_keyValMap(cspec_path):
    f = open(cspec_path, 'r')
    keyValMap = {}
    # set default tag as empty string
    keyValMap['tag'] = ""
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("#")):
            pass
        elif (line.find("=") != -1):
            if_verbose("  processing keyVal line - {0}".format(line))
            key, val = line.split("=")
            val = resolve_value(keyValMap, val)
            keyValMap[key] = val
        else:
            pass
    f.close()
    return keyValMap
    
def load_qsub_commands(cspec_path, keyValMap):
    f = open(cspec_path, 'r')
    qsub_commands = []
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("qsub_command:")):
            if_verbose("  processing qsub_command line - {0}".format(line))
            x, this_command = line.split(":")
            qsub_commands.append(this_command)
            #resolve_command(this_command, keyValMap, qsub_commands)
        else:
            pass
    f.close()
    return qsub_commands
            
def validate_cluster_spec(path):
    pass
    
def resolve_value(keyValMap, given_val):
    result = given_val
    for key, val in keyValMap.iteritems():
        match_string = "<{0}>".format(key)
        result = result.replace(match_string, val)
    if_verbose("  value resolved to : {0}".format(result))
    return result
    
def resolve_command(command, keyValMap, commands):
    for key, val in keyValMap.iteritems():
        match_string = "<{0}>".format(key)
        command = command.replace(match_string, val)
    if_verbose("  command resolved to : {0}".format(command))
    commands.append(command)
            
def resolve_permutation(permute_dict, commands, keyValMap):
    # first make a copy of the keyValMap so taht we can resolve permutations with in its values
    keyValMap_permuation_specific = {}
    for key, val in keyValMap.iteritems():
        keyValMap_permuation_specific[key] = val
    
    # now use the copy to resolve permutations in the values
    for permKey, permVal in permute_dict.iteritems():
        #if_verbose("  key, val in permute step 1 : {0},{1}".format(permKey, permVal))
        keyValMap_permuation_specific_for_this_pass = {}
        match_string = "({0})".format(permKey)
        #if_verbose("  perm match_string : {0}".format(match_string))
        for key, val in keyValMap_permuation_specific.iteritems():
            resolved_val = val.replace(match_string, permVal)
            keyValMap_permuation_specific_for_this_pass[key] = resolved_val
        keyValMap_permuation_specific = keyValMap_permuation_specific_for_this_pass    
        #if_verbose("  keyValMap_permuation_specific after a pass of resolve_permutation: {0}".format(keyValMap_permuation_specific))
            
    # now do a pass through keyValMap_permuation_specific to resolve any now-refined lookups
    # FIXME - does this need to be iterative?
    keyValMap_final_for_permutation = {}
    for key, val in keyValMap_permuation_specific.iteritems():
        resolved_val = resolve_value(keyValMap, val)
        keyValMap_final_for_permutation[key] = resolved_val
    
    # then make a first pass through the commands and resolve permutations as some lookups will depend on that having been done
    commands_for_this_permutation = []
    for key, val in permute_dict.iteritems():
        #if_verbose("  key, val in permute step 1 : {0},{1}".format(key, val))
        commands_for_this_permutation = []
        match_string = "({0})".format(key)
        #if_verbose("  perm match_string : {0}".format(match_string))
        for command in commands:
            resolved_command = command.replace(match_string, val)
            commands_for_this_permutation.append(resolved_command)
        commands = commands_for_this_permutation    
        #if_verbose("  commands after a pass1 of resolve_permutation: {0}".format(commands))
        
    # now use keyValMap_final_for_permutation to resolve the commands
    for key, val in keyValMap_final_for_permutation.iteritems():
        #if_verbose("  key, val in permute step 2 : {0},{1}".format(key, val))
        match_string = "<{0}>".format(key)
        commands_for_this_permutation = []
        #if_verbose("  keyVal match_string : {0}".format(match_string))
        for command in commands:
            resolved_command = command.replace(match_string, val)
            commands_for_this_permutation.append(resolved_command)
        commands = commands_for_this_permutation    
        #if_verbose("  commands after a pass2 of resolve_permutation: {0}".format(commands))  
    if_verbose("  commands after resolve_permutation: {0}".format(commands_for_this_permutation))
    return commands_for_this_permutation

def expand_permutations(permuters):
    dict_list = []
    # permuteKey: someKey   permuteList:[valx, valy, valz]
    for permuteKey, permuteList in permuters.iteritems():
        if_verbose("  permute_key {0}, permute_list {1}".format(permuteKey, permuteList))
        if (len(dict_list) == 0):
            # first time through
            for permuteListValue in permuteList:
                new_dict = {}
                # new dictionaries just have the one item
                new_dict[permuteKey] = permuteListValue
                #if_verbose("adding new_dict[{0}] as {1}".format(permuteKey, permuteListValue))
                dict_list.append(new_dict)
        else:
            # we already have dictionaries to expand from
            expanded_dict_list = []
            # dict_list might look like [ { amount=5 } { amount = 10 } ]
            for existing_dict in dict_list:
                # {amount = 5}, for example
                for permuteListValue in permuteList:
                    new_dict = {}
                    #add each new value
                    new_dict[permuteKey] = permuteListValue
                    #... to the prior values
                    #if_verbose("  existing dict:  {0}".format(existing_dict))
                    for existingKey, existingVal in existing_dict.iteritems():
                        #if_verbose("adding new_dict[{0}] as {1}".format(existingKey, existingVal))
                        new_dict[existingKey] = existingVal
                    expanded_dict_list.append(new_dict)
            dict_list = expanded_dict_list
        if_verbose("  dict_list : {0}".format(dict_list))
    return dict_list                

def launch_scripts(keyValMap, permute_dictionary_list, concisePrintMap):
    user_job_number = 1
    if keyValMap.has_key('one_up_basis'):
        user_job_number = int(keyValMap['one_up_basis'])
    for permute_dict in permute_dictionary_list:
        permute_code = generate_perm_code(permute_dict, concisePrintMap)
        launch_script(user_job_number, keyValMap, permute_code)
        user_job_number = user_job_number + 1
        time.sleep(1.5)

def generate_scripts(keyValMap, commands, permute_dictionary_list, qsub_commands, concisePrintMap):
    user_job_number = 1
    if keyValMap.has_key('one_up_basis'):
        user_job_number = int(keyValMap['one_up_basis'])
    for permute_dict in permute_dictionary_list:
        permute_code = generate_perm_code(permute_dict, concisePrintMap)
        commands_for_this_permutation = resolve_permutation(permute_dict, commands, keyValMap)
        generate_script(user_job_number, keyValMap, permute_code, commands_for_this_permutation, qsub_commands)
        user_job_number = user_job_number + 1
         
def get_script_path_root(user_job_number, keyValMap, permute_code):
    dir_script = keyValMap['dir_script']
    if (not(os.path.isdir(dir_script))):
        os.makedirs(dir_script)
    tag = ""
    pathname_root = ""
    if (keyValMap.has_key('tag')):
        tag = keyValMap['tag']
        pathname_root = "{0}{1}j{2}_{3}{4}".format(dir_script, os.sep, user_job_number, permute_code, tag)
    else:
        pathname_root = "{0}{1}j{2}_{3}".format(dir_script, os.sep, user_job_number, permute_code)
    return pathname_root
    
def launch_script(user_job_number, keyValMap, permute_code):
    pathname_root = get_script_path_root(user_job_number, keyValMap, permute_code)
    pathname = "{0}.sh".format(pathname_root)
    try: 
        print "calling qsub {0}".format(pathname)
        subprocess.check_call(["qsub", pathname])
    except CalledProcessError:
        print "There was a problem invoking the script: {0}".format(pathname)
        print "Return code was {0}".format(CallProcessError.returncode)
    
def generate_script(user_job_number, keyValMap, permute_code, commands_for_this_permutation, qsub_commands):
    pathname_root = get_script_path_root(user_job_number, keyValMap, permute_code)
    pathname = "{0}.sh".format(pathname_root)
    print "  pathname of script file: {0}".format(pathname)
    f = open(pathname, 'w')
    f.write("#!/bin/csh\n")
    f.write("#\n")
    f.write("# use current working directory for input and output - defaults is\n")
    f.write("# to use the users home directory\n")
    f.write("#$ -cwd\n")
    f.write("#\n")
    f.write("# name this job\n")
    tag = ""
    if (keyValMap.has_key('tag')):
        tag = keyValMap['tag']
    if (tag != ""):
        f.write("#$ -N j{0}_{1}{2}\n".format(user_job_number, permute_code, tag))
    else:
        f.write("#$ -N j{0}_{1}\n".format(user_job_number, permute_code))
        
    f.write("#\n")
    f.write("#$ -q eecs,eecs1,eecs2,share\n")
    f.write("#$ -M jedirv@gmail.com\n")
    f.write("#$ -m beas\n")
    f.write("# send stdout and stderror to this file\n")
    f.write("#$ -o {0}.out\n".format(pathname_root))
    f.write("#$ -e {0}.err\n".format(pathname_root))
    f.write("#\n")
    f.write("#see where the job is being run\n")
    f.write("hostname\n")
    for cur_command in commands_for_this_permutation:
        f.write("{0}\n".format(cur_command))
    f.close()  

def generate_perm_code(permute_dict, concisePrintMap):
    code = ""
    for key, val in permute_dict.iteritems():
        if (concisePrintMap.has_key(key)):
            key = concisePrintMap[key]
        code = "{0}_{1}_{2}".format(code, key, val)
    code = code.lstrip('_')
    if_verbose("code determined as : {0}".format(code))
    return code        
            
def validate_args(permute_command, cspec_path, flags):
    if (not(permute_command == "gen" or permute_command == "launch" or permute_command == "auto")):
        usage()
        exit()
    # verify spec path exists
    try:
        f = open(cspec_path, 'r')
        # verify first line has cspec flag
        header = f.readline()
        if (header != "#cspec\n"):
            print "cspec file must have this header:  '#cspec', {0} does not. Exiting.".format(cspec_path)
            f.close()
            exit()
        f.close()
    except IOError:
        print "An error occured trying to open {0}".format(cspec_path)
        exit()
    if (flags != ""):
        if (flags != "-v"):
            print "Invalid flag {0}. Only -v for verbose is supported".format(flags)
            exit()
    
def usage():
    print "usage:  permute <path of cluster_spec> gen|launch|auto [-v]"
    
if __name__ == '__main__':
    main()
	
