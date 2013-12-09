verbose = False

def resolve_value(keyValMap, given_val):
    result = given_val
    for key, val in keyValMap.iteritems():
        match_string = "<{0}>".format(key)
        result = result.replace(match_string, val)
    if_verbose("  value resolved to : {0}".format(result))
    return result
    
def if_verbose(message):
    global verbose
    if (verbose):
        print message
            
class ClusterSpec(object):
    '''
    Wraps the cluster specification file *.cspec
    '''
    
    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        # verify spec path exists
        try:
            f = open(path, 'r')
            # verify first line has cspec flag
            header = f.readline()
            if (header != "#cspec\n"):
                print "cspec file must have this header:  '#cspec', {0} does not. Exiting.".format(path)
                f.close()
                exit()
            f.close()
            
            self.master_job_name = self.load_special_value(self.path, 'master_job_name:')
            self.trials = self.load_special_value(self.path, 'trials:')
            self.permuters = self.load_permutations(self.path, 'permute:')
            self.concise_print_map = self.load_concise_print_map(self.path)
            
            self.key_val_map = self.load_replaces(self.path)
            self.results_dir = self.load_dir(self.path, "results_dir:")
            # put the results_dir into the kvm so that permutation calculation wil find it
            self.key_val_map['results_dir'] = self.results_dir
            # and the master_job_name
            self.key_val_map['master_job_name'] = self.master_job_name
            
            self.qsub_commands = self.load_qsub_commands(self.path)
            self.commands = self.load_commands(self.path)
            
            self.script_dir = self.load_dir(self.path, "script_dir")
            self.one_up_basis = self.load_special_value(self.path, 'one_up_basis:')
            
            self.scores_permuters = self.load_permutations(self.path, 'scores_permute:')
            self.scores_from_filepath = ""
            self.scores_from_colname = ""
            self.scores_from_rownum = ""
            self.load_scores_from(self.path)
            self.scores_to = self.load_special_value(self.path,'scores_to:')
            self.scores_x_axis = self.load_special_value(self.path, 'scores_x_axis:')
            self.scores_y_axis = self.load_special_value(self.path, 'scores_y_axis:')
            #print "done loading cspec"
        except IOError:
            print "An error occured trying to open cspec file {0}".format(path)
            exit()

    def get_concise_name(self, permuter_name):
        if self.concise_print_map.has_key(permuter_name):
            return self.concise_print_map[permuter_name]
        else:
            return permuter_name
        
    def load_scores_from(self, path):
        f = open(path, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith('scores_from:')):
                command, scores_from_info = line.split(":")
                file_info, column_info, row_info = scores_from_info.split(',')
                file_flag, self.scores_from_filepath = file_info.split('=')
                colname_flag , self.scores_from_colname = column_info.split('=')
                rownum_flag, self.scores_from_rownum = row_info.split('=')
        
    
    def load_dir(self, path, dir_flag):
        f = open(path, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith(dir_flag)):
                command, dir = line.split(":")
                dir = resolve_value(self.key_val_map, dir)
                return dir
        return ""
    
    def load_special_value(self, path, flag):
        f = open(path, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith(flag)):
                flag_sans_colon, target = line.split(":")
                return target
        return ""

       
    def load_permutations(self, path, flag):
        f = open(path, 'r')
        permuters = {}
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith(flag)):
                if_verbose("  processing permute line - {0}".format(line))
                permute_command, permute_info = line.split(':')
                permuteKey, permute_list_string = permute_info.split('=')
                if (permute_list_string.find(" ") != -1):
                    permute_start, permute_end = permute_list_string.split(" ")
                    permute_list = range(int(permute_start), int(permute_end)+1)
                    permute_list = map(str, permute_list)
                    permute_list = zero_pad_to_widest(permute_list)
                elif (permute_list_string.find(",") != -1):
                    permute_list = permute_list_string.split(",")
                    permute_list = zero_pad_to_widest(permute_list)
                else:
                    # must be a singleton cvalue
                    permute_list = [ permute_list_string ]
                permuters[permuteKey] = permute_list
            else:
                pass
        f.close()
        return permuters
    
    def load_replaces(self, path):
        f = open(path, 'r')
        key_val_map = {}
        # set default tag as empty string
        key_val_map['tag'] = ""
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith("#")):
                pass
            elif (line.startswith("<replace>")):
                if_verbose("  processing keyVal line - {0}".format(line))
                replace_command, keyVal = line.split(":")
                key, val = keyVal.split("=")
                val = resolve_value(key_val_map, val)
                key_val_map[key] = val
            else:
                pass
        f.close()
        return key_val_map        
    

    def load_qsub_commands(self, path):
        f = open(path, 'r')
        qsub_commands = []
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith("qsub_command:")):
                if_verbose("  processing qsub_command line - {0}".format(line))
                x, this_command = line.split(":")
                qsub_commands.append(this_command)
            else:
                pass
        f.close()
        return qsub_commands
    
    def load_commands(self, path):
        f = open(path, 'r')
        commands = []
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith("command:")):
                if_verbose("  processing command line - {0}".format(line))
                x, this_command = line.split(":")
                commands.append(this_command)
            else:
                pass
        f.close()
        return commands
        
     
    def load_concise_print_map(self, path):
        f = open(path, 'r')
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
 
def zero_pad_to_widest(permute_values):
    result = permute_values
    # if any of the entries are not numbers, just return the list
    for val in permute_values:
        if (not(is_string_an_int(val))) and (not(is_string_a_float(val))):
             return result
                                     
    # they are all numbers, find the highest integral width
    max_width = 0
    for val in permute_values:
        integer_number_string = str(int(float(val)))
        cur_width = len(integer_number_string)
        if cur_width > max_width:
            max_width = cur_width
            
    # pad all the values to that width
    result = []
    for val in permute_values:
        integer_portion = int(float(val))
        integer_portion_as_string = str(integer_portion)
        decimal_portion = float(val) - float(integer_portion)
        decimal_portion_as_string = str(decimal_portion)
        decimal_portion_as_string_sans_leading_zero = decimal_portion_as_string.lstrip("0")
        zero_padded_integer_string = integer_portion_as_string.zfill(max_width)
        #print "zero_padded_integer_string {0}".format(zero_padded_integer_string)
        if (decimal_portion_as_string_sans_leading_zero == ".0"):
            # leave out the decimal portion
            new_val = zero_padded_integer_string
        else:
            new_val = "{0}{1}".format(zero_padded_integer_string,decimal_portion_as_string_sans_leading_zero)
        result.append(new_val)
    return result

def is_string_an_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
    
def is_string_a_float(val):
    try:
        x = float(val)
        return True
    except ValueError:
        return False
               
def validate(path):
    result_permute = validate_permute_entries(path)
    if not(result_permute):
        print "problem found in permute statements"
        
    result_replace = validate_replace_entries(path)
    if not(result_replace):
        print "problem found in replace statements"
        
    result_script_dir = validate_script_dir(path)
    if not(result_script_dir):
        print "problem found in script_dir statement"
  
    result_results_dir = validate_results_dir(path)
    if not(result_results_dir):
        print "problem found in results_dir statement"
    
    return result_permute and result_replace and result_script_dir and result_results_dir

   
def validate_results_dir(path):
    result = True
    results_dir = "unknown"
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("results_dir:")):
            # should be one =
            results_dir_command, results_dir = line.split(":")
    if (results_dir == "unknown"):
        result = False
        print "cluster_spec missing results_dir declaration (results_dir:some_dir) {0}".format(path)    
    if (results_dir.find('_PERMUTATION_CODE_') == -1):
        result = False
        print "cluster_spec results_dir declaration must contain the string _PERMUTATION_CODE_ {0}".format(path)      
    return result
    
def validate_script_dir(path):
    result = True
    script_dir = "unknown"
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("script_dir:")):
            # should be one =
            script_dir_command, script_dir = line.split(":")
    if (script_dir == "unknown"):
        result = False
        print "cluster_spec missing script_dir declaration (script_dir:some_dir) {0}".format(path)      
    return result

def validate_master_job_name(path):
    result = True
    master_job_name = "unknown"
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("master_job_name:")):
            # should be one =
            master_job_name_command, master_job_name = line.split(":")
    if (master_job_name == "unknown"):
        result = False
        print "cluster_spec missing master_job_name declaration (master_job_name:some_name) {0}".format(path)      
    return result


def validate_trials(path):
    result = True
    trials = "unknown"
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("trials:")):
            # should be one =
            trials_command, trials = line.split(":")
    if (trials == "unknown"):
        result = False
        print "cluster_spec missing trials declaration (trials:some_name) {0}".format(path)      
    return result

def validate_replace_entries(path):
    result = True
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("<replace>:")):
            colon_count = line.count(':')
            if (colon_count != 1):
                # should be one :
                print "<replace>:key=value - line malformed - {0}".format(line)
                result = False
            else:
                replace_command, keyVal = line.split(":")
                equal_count = keyVal.count('=')
                if (equal_count != 1):
                    # should be one =
                    print "<replace>:key=value - line malformed - {0}".format(line)
                    result = False
                else:
                    key, val = keyVal.split('=')
                    # key has to be nonempty string
                    if (key == ""):
                        print "<replace>:key=value - key must be non-empty string {0}".format(line)
                        result = False
                    elif (val == ""):
                        print "<replace>:key=value - val must be non-empty string {0}".format(line)
                        result = False
                    else:
                        pass
    return result
    
def validate_permute_entries(path):
    result = True
    f = open(path, 'r')
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        if (line.startswith("permute:")):
            # should be 3 colons
            colon_count = line.count(':')
            if (colon_count != 1):
                print "permute line malformed - {0} - should be permute:var=vals where vals can be:".format(line)
                print "   range of integers with a space    1 5 (expanded to 1,2,3,4,5)"
                print "   single value                    x   (this exposes the value in the permutation code)"
                print "   comma separated list of values  aa,bb,cc"
                result = False
            else:
                permutecommand, permute_info = line.split(':')
                permuteKey, permute_list_string = permute_info.split('=')
                if (permute_list_string.find(" ") != -1):
                    permute_start, permute_end = permute_list_string.split(" ")
                    # start of range is an int?
                    try:
                        foo = int(permute_start)
                    except:
                        print "{0} is not an integer in {1}".format(permute_start, line)
                        result = False
                    # end of range is an int?    
                    try:
                        foo = int(permute_end)
                    except:
                        print "{0} is not an integer in {1}".format(permute_end, line)
                        result = False
                    if (result):
                        start = int(permute_start)
                        end = int(permute_end)
                        if (start > end):
                            print "start or range is greater than end {0}".format(line)
                            result = False
                elif (permute_list_string.find(",") != -1):
                    # no way I can think of to mess this up
                    pass
                else:
                    # must be a singleton cvalue
                    # no way I can think of to mess this up
                    pass
    f.close()
    return result
    