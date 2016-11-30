import cluster_spec
import logging
#constants to help with permutation processing
IGNORE_TRIALS = False
INCLUDE_TRIALS = True
 
def get_list_of_output_files(permutation_info, cspec):
    output_file_paths = []
    scores_permutations = expand_permutations(cspec.scores_permuters)
    complete_permutation_infos = []
    if (len(scores_permutations) == 0):
        complete_permutation = {}
        for key, val in permutation_info.items():
            complete_permutation[key] = val
        complete_permutation_infos.append(complete_permutation)
    else:
        #print "scores_permutations {0}".format(scores_permutations)
        for scores_permutation in scores_permutations:
            complete_permutation = {}
            for key, val in permutation_info.items():
                complete_permutation[key] = val
            for key, val in scores_permutation.items():
                complete_permutation[key] = val
            complete_permutation_infos.append(complete_permutation)
    #print "complete_permutation_infos {0}".format(complete_permutation_infos)   
    for complete_permutation_info in complete_permutation_infos:        
        unresolved_output_files = []
        #print "cspec.scores_from_filepath {0}".format(cspec.scores_from_filepath)
        #print "cspec.key_val_map {0}".format(cspec.key_val_map)
        unresolved_output_files.append(cspec.scores_from_filepath)
        kvm_with_results_dir_resolved = {}
        for key, val in cspec.key_val_map.items():
            kvm_with_results_dir_resolved[key] = val
        kvm_with_results_dir_resolved['permutation_results_dir'] = get_resolved_results_dir_for_permutation(permutation_info, cspec)      
        resolved_list_of_one = resolve_list_for_permutation(complete_permutation_info, unresolved_output_files, kvm_with_results_dir_resolved)
        #print resolved_list_of_one
        output_file_paths.append(resolved_list_of_one[0])
    return output_file_paths
    #resolve_permutation(permutation_info, commands, keyValMap)
    #scores_from:file=<permutation_results_dir>/score_out_(color).csv,column_name=auc,row_number=1
    #...need to generate list of all output files for permutation, keying off
    #scores_permute:color=red,blue,
    
def generate_perm_code(permutation_info, concisePrintMap, include_trials):
    code = ""
    keys = permutation_info.keys()
    sorted_keys = sorted(keys)
    # ensure that 'trial' is the last key
    deferred_trial_val = ''
    for key in sorted_keys:
        if (include_trials == IGNORE_TRIALS and key == 'trial'):
            pass
        else:
            val = permutation_info[key]
            if key == 'trial':
                deferred_trial_val = val
            else:
                if (concisePrintMap.has_key(key)):
                    key = concisePrintMap[key]
                if (concisePrintMap.has_key(val)):
                    val = concisePrintMap[val]
                code = "{0}_{1}_{2}".format(code, key, val)
    if deferred_trial_val != '':
        code = "{0}_{1}_{2}".format(code, 'trial', deferred_trial_val)
    code = code.lstrip('_')
    logging.info("   perm code : {0}".format(code))
    # change commas to dashes
    code = code.replace(",","-")
    return code        

    
def expand_permutations(permuters):
    dict_list = []
    keys = permuters.keys()
    sorted_keys = sorted(keys)
    
    # permuteKey: someKey   permuteList:[valx, valy, valz]
    #for permuteKey, permuteList in permuters.iteritems():
    for permuteKey in sorted_keys:
        permuteList = permuters[permuteKey]
        sortedPermuteList = sorted(permuteList)
        #logging.debug("  permute_key {0}, permute_list {1}".format(permuteKey, sortedPermuteList))
        if (len(dict_list) == 0):
            # first time through
            for permuteListValue in sortedPermuteList:
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
                for permuteListValue in sortedPermuteList:
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
        dict_list = sorted(dict_list)
        logging.info("  perms expanded to : {0}".format(dict_list))
    return dict_list                 

          
def resolve_list_for_permutation(permutation_info, commands, keyValMap):
    # first make a copy of the keyValMap so that we can resolve permutations with in its values
    keyValMap_permuation_specific = {}
    for key, val in keyValMap.iteritems():
        keyValMap_permuation_specific[key] = val
    
    # now use the copy to resolve permutations in the values
    for permKey, permVal in permutation_info.iteritems():
        if (permKey != 'trial'):
            logging.debug("  key, val in permute step 1 : {0},{1}".format(permKey, permVal))
            keyValMap_permutation_specific_for_this_pass = {}
            match_string = "({0})".format(permKey)
            logging.debug("  perm match_string : {0}".format(match_string))
            for key, val in keyValMap_permuation_specific.iteritems():
                resolved_val = val.replace(match_string, permVal)
                keyValMap_permutation_specific_for_this_pass[key] = resolved_val
            keyValMap_permuation_specific = keyValMap_permutation_specific_for_this_pass  
            logging.debug("  keyValMap_permuation_specific after a pass of resolve_permutation: {0}".format(keyValMap_permuation_specific))
    #print "keyValMap_permuation_specific {0}".format(keyValMap_permuation_specific) 
    # now do a pass through keyValMap_permuation_specific to resolve any now-refined lookups
    # FIXME - does this need to be iterative?
    keyValMap_final_for_permutation = {}
    for key, val in keyValMap_permuation_specific.iteritems():
        resolved_val = cluster_spec.resolve_value(keyValMap, val)
        keyValMap_final_for_permutation[key] = resolved_val
    #print "keyValMap_final_for_permutation {0}".format(keyValMap_final_for_permutation) 
    # then make a first pass through the commands and resolve permutations as some lookups will depend on that having been done
    commands_for_this_permutation = []
    for key, val in permutation_info.iteritems():
        logging.debug("  key, val in permute step 1 : {0},{1}".format(key, val))
        if (key != 'trial'):
            commands_for_this_permutation = []
            match_string = "({0})".format(key)
            logging.debug("  perm match_string : {0}".format(match_string))
            for command in commands:
                resolved_command = command.replace(match_string, val)
                commands_for_this_permutation.append(resolved_command)
            commands = commands_for_this_permutation    
            logging.debug("  commands after a pass1 of resolve_permutation: {0}".format(commands))
    
    # now use keyValMap_final_for_permutation to resolve the commands
    for key, val in keyValMap_final_for_permutation.iteritems():
        logging.debug("  key, val in permute step 2 : {0},{1}".format(key, val))
        match_string = "<{0}>".format(key)
        commands_for_this_permutation = []
        logging.debug("  keyVal match_string : {0}".format(match_string))
        for command in commands:
            resolved_command = command.replace(match_string, val)
            commands_for_this_permutation.append(resolved_command)
        commands = commands_for_this_permutation    
        logging.debug("  commands after a pass2 of resolve_permutation: {0}".format(commands))  
    #print "  commands after resolve_permutation: {0}".format(commands_for_this_permutation)
    logging.info("  commands after resolve_permutation: {0}".format(commands_for_this_permutation))
    return commands_for_this_permutation

def get_resolved_results_dir_for_permutation(permutation_info, cspec):
    pcode = generate_perm_code(permutation_info, cspec.concise_print_map, True)
    interim_results_dir = cspec.generate_results_dir_for_permutation(pcode)
    dir_list = [interim_results_dir]
    resolved_results_dir =  resolve_list_for_permutation(permutation_info, dir_list, cspec.key_val_map)[0]
    logging.info("  resolved_results_dir: {0}".format(resolved_results_dir))
    return resolved_results_dir
    
    