import cluster_spec

verbose = False
#constants to help with permutation processing
IGNORE_TRIALS = False
INCLUDE_TRIALS = True

def if_verbose( message):
    global verbose
    if (verbose):
        print message
 


def generate_permutation_code(permute_dict, concisePrintMap, include_trials):
    code = ""
    keys = permute_dict.keys()
    sorted_keys = sorted(keys)
    for key in sorted_keys:
        if (include_trials == IGNORE_TRIALS and key == 'trials'):
            pass
        else:
            val = permute_dict[key]
            if (concisePrintMap.has_key(key)):
                key = concisePrintMap[key]
            if (concisePrintMap.has_key(val)):
                val = concisePrintMap[val]
            code = "{0}_{1}_{2}".format(code, key, val)
    code = code.lstrip('_')
    if_verbose("code determined as : {0}".format(code))
    return code        

    
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

          
def resolve_permutation(permute_dict, commands, keyValMap):
    # first make a copy of the keyValMap so taht we can resolve permutations with in its values
    keyValMap_permuation_specific = {}
    for key, val in keyValMap.iteritems():
        keyValMap_permuation_specific[key] = val
    
    # now use the copy to resolve permutations in the values
    for permKey, permVal in permute_dict.iteritems():
        if (permKey != 'trials'):
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
        resolved_val = cluster_spec.resolve_value(keyValMap, val)
        keyValMap_final_for_permutation[key] = resolved_val

    # then make a first pass through the commands and resolve permutations as some lookups will depend on that having been done
    commands_for_this_permutation = []
    for key, val in permute_dict.iteritems():
        #if_verbose("  key, val in permute step 1 : {0},{1}".format(key, val))
        if (key != 'trials'):
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


def get_job_number_width(permute_dictionary_list):
    permute_count = len(permute_dictionary_list)
    permute_count_as_string = str(permute_count)
    permute_count_width = len(permute_count_as_string)
    return permute_count_width