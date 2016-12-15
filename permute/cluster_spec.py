import os
import logging
import new_spec

def resolve_value(keyValMap, given_val):
    result = given_val
    for key, val in keyValMap.iteritems():
        match_string = "<{0}>".format(key)
        result = result.replace(match_string, val)
    #logging.debug("  value resolved to : {0}".format(result))
    return result
    
class ClusterSpec(object):
    '''
    Wraps the cluster specification file *.cspec
    '''
    
    def __init__(self, path, lines, stdout):
        '''
        Constructor
        '''
        self.stdout = stdout
        self.path = path
        self.lines = lines
        try:
            if (len(lines) == 0):
                print("cspec file empty:  {0}Exiting.".format(path))
            
            # verify first line has cspec flag
            header = lines[0]
            header = "".join(header.split()) # remove white spaces
            #print("header : {0} length {1} ".format(header, len(header)))
            if (header != "#cspec"):
                self.stdout.println("cspec file must have this header:  '#cspec', {0} does not. Exiting.".format(path))
                exit()
            
            cspec_filename = os.path.basename(self.path)
            self.cspec_name, file_ext  = cspec_filename.split('.')
            self.trials = self.load_special_value(self.lines, 'trials:')
            if self.trials == '':
                self.trials = '1'
            self.permuters = load_permuters(self.lines, 'permute:', '(permute):')
            self.concise_print_map = self.load_concise_print_map(self.lines)
            
            self.key_val_map = self.load_replaces(self.lines)
            self.root_dir = self.load_dir(self.lines, "root_dir:")
            self.root_dir = os.path.abspath(self.root_dir)
            self.job_results_dir = "{0}/{1}/{2}".format(self.root_dir, self.cspec_name, 'results')
            # put the results_dir into the kvm so that permutation calculation wil find it
            self.key_val_map['root_dir'] = self.root_dir
            self.key_val_map['job_results_dir'] = self.job_results_dir
            # and the master_job_name
            self.key_val_map['cspec_name'] = self.cspec_name
            
            self.qsub_commands = self.load_qsub_commands(self.lines)
            self.commands = self.load_commands(self.lines)
            
            self.script_dir = "{0}/{1}/{2}".format(self.root_dir, self.cspec_name, 'scripts')
            self.first_job_number = self.load_special_value(self.lines, 'first_job_number:')
            if self.first_job_number == '':
                self.first_job_number = '0'
            self.output_filename = self.load_special_value(self.lines, 'output_filename:')
            
            # disengage the scores_to and scores_from until we re-engage collection of results.
            #self.scores_permuters = load_permuters(self.lines, 'scores_permute:','(scores_permute):')
            #self.scores_from_filepath = ""
            #self.scores_from_colname = ""
            #self.scores_from_rownum = ""
            #self.load_scores_from(self.lines)
            #self.scores_to = self.load_special_value(self.lines,'scores_to:')
            #self.scores_x_axis = self.load_list(self.lines, 'scores_x_axis:')
            #self.scores_y_axis = self.load_list(self.lines, 'scores_y_axis:')
            #print "done loading cspec"
        except IOError:
            self.stdout.println("An error occurred trying to open cspec file {0}".format(path))
            exit()

    
    def get_permuters_trials_included(self):
        permuters_with_trials = {}
        for key, val in self.permuters.items():
            permuters_with_trials[key] = val
        permuters_with_trials['trial'] = self.get_trials_list()
        return permuters_with_trials
    
    def generate_results_dir_for_permutation(self, pcode):
        return "{0}/{1}".format(self.job_results_dir, pcode)
    
    def get_trials_list(self):
        result = []
        integer_list = range(1, int(self.trials) + 1)
        for integer in integer_list:
            result.append(str(integer))
        return result
    
    def get_concise_name(self, permuter_name):
        if self.concise_print_map.has_key(permuter_name):
            return self.concise_print_map[permuter_name]
        else:
            return permuter_name
    
    '''    
    def load_scores_from(self, lines):
        for line in lines:
            line = line.rstrip()
            line = "".join(line.split()) # remove white spaces
            if (line.startswith('scores_from:')):
                command, scores_from_info = line.split(":")
                file_info, column_info, row_info = scores_from_info.split(',')
                file_flag, self.scores_from_filepath = file_info.split('=')
                colname_flag , self.scores_from_colname = column_info.split('=')
                rownum_flag, self.scores_from_rownum = row_info.split('=')
    '''    
    
    def load_dir(self, lines, dir_flag):
        for line in lines:
            line = line.rstrip()
            line = "".join(line.split()) # remove white spaces
            if (line.startswith(dir_flag)):
                command, dir = line.split(":")
                dir = resolve_value(self.key_val_map, dir)
                return dir
        return ""
    
    def load_special_value(self, lines, flag):
        for line in lines:
            line = line.rstrip()
            line = "".join(line.split()) # remove white spaces
            if (line.startswith(flag)):
                flag_sans_colon, target = line.split(":")
                if (hasattr(self, 'key_val_map')):
                    resolved_target = resolve_value(self.key_val_map, target)
                    return resolved_target
                else:
                    return target
        return ""

    def load_list(self, lines, flag):
        for line in lines:
            line = line.rstrip()
            line = "".join(line.split()) # remove white spaces
            if (line.startswith(flag)):
                flag_sans_colon, target_list = line.split(":")
                list_items = target_list.split(',')
                if (not(hasattr(self, 'key_val_map'))):
                    return list_items
                resolved_list = []
                for item in list_items:
                    resolved_item = resolve_value(self.key_val_map, item)
                    resolved_list.append(resolved_item)
                return resolved_list
        return ""    
    
    
    def load_replaces(self, lines):
        key_val_map = {}
        # set default tag as empty string
        key_val_map['tag'] = ""
        for line in lines:
            line = line.rstrip()
            line = "".join(line.split()) # remove white spaces
            if (line.startswith("#")):
                pass
            elif (line.startswith("<replace>")):
                logging.debug("  processing keyVal line - {0}".format(line))
                replace_command, keyVal = line.split(":")
                key, val = keyVal.split("=")
                val = resolve_value(key_val_map, val)
                key_val_map[key] = val
            else:
                pass
        logging.debug("  key_val_map {0}".format(key_val_map))
        return key_val_map        
    

    def load_qsub_commands(self, lines):
        qsub_commands = []
        for line in lines:
            line = line.rstrip()
            if (line.startswith("qsub_command:")):
                logging.debug("  processing qsub_command line - {0}".format(line))
                x, this_command = line.split(":")
                qsub_commands.append(this_command)
            else:
                pass
        logging.debug("  qsub_commands {0}".format(qsub_commands))
        return qsub_commands
    
    def load_commands(self, lines):
        commands = []
        for line in lines:
            line = line.rstrip()
            if (line.startswith("command:")):
                logging.debug("  processing command line - {0}".format(line))
                x, this_command = line.split(":")
                commands.append(this_command)
            else:
                pass
        logging.debug("  commands {0}".format(commands))
        return commands
        
     
    def load_concise_print_map(self, lines):
        concisePrintMap = {}
        for line in lines:
            line = line.rstrip()
            line = "".join(line.split()) # remove white spaces
            if (line.startswith("concise_print:") or line.startswith("encode:")):
                logging.debug("  processing concise_print line - {0}".format(line))
                command, conciseKeyVal = line.split(":")
                key, val = conciseKeyVal.split(",")
                concisePrintMap[key] = val
            else:
                pass
        logging.debug("  concisePrintMap {0}".format(concisePrintMap))
        return concisePrintMap


def load_permuters(lines, flag1, flag2):
    permuters = {}
    for line in lines:
        line = line.rstrip()
        line = "".join(line.split()) # remove white spaces
        if (line.startswith(flag1) or line.startswith(flag2)):
            logging.debug("  processing permute line - {0}".format(line))
            permute_command, permutation_info = line.split(':')
            permuteKey, permute_list_string = permutation_info.split('=')
            permute_list = []
            if (permute_list_string.startswith("range(")):
                range_spec = permute_list_string[6:]
                range_spec_length = len(range_spec)
                nums = range_spec.strip(')')
                numlist = nums.split(",")
                start = numlist[0]
                end = numlist[1]
                permute_list = []
                if (len(numlist) == 2):
                    permute_list = range(int(start), int(end))
                elif (len(numlist) == 3): 
                    permute_list = range(int(start), int(end), int(numlist[2]))
                else:
                    pass # shouldn't get here as validator prevents
                permute_list = map(str, permute_list)
                permute_list = zero_pad_to_widest(permute_list)
            elif (permute_list_string.find(",") != -1):
                permute_list = permute_list_string.split(",")
                permute_list = convert_escaped_commas(permute_list) # supports "6_comma_8_comma_10" -->  "6,8,10"
                permute_list = zero_pad_to_widest(permute_list)
            else:
                # must be a singleton cvalue
                permute_list = [ permute_list_string ]
            permuters[permuteKey] = permute_list
        else:
            pass
        logging.debug("  permuters : {0}".format(permuters))
    return permuters     
   
def convert_escaped_commas(list_with_comma_maybe_):
    newList = []
    for val in list_with_comma_maybe_:
        newVal = val.replace("_comma_",",")
        newList.append(newVal)
    return newList
     
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
               
               
def validate(lines, stdout):
    result_permute = validate_permute_entries(lines)
    if not(result_permute):
        stdout.println("problem found in permute statements")
        
    result_replace = validate_replace_entries(lines)
    if not(result_replace):
        stdout.println("problem found in replace statements")
    
    result_root_dir = validate_statement_present(lines,"root_dir:","some_dir", stdout)
    if not(result_root_dir):
        stdout.println("problem found in root_dir statement")
        
    result_trials = validate_statement_present(lines,"trials:","some_integer", stdout)
    if not(result_trials):
        stdout.println("problem found in trials statement")
    
    result_scores_info = validate_scores_gathering_info(lines, stdout)
    if not(result_scores_info):
        stdout.println("problem found in scores gathering info entries")
        
    output_filename = validate_statement_present(lines, "output_filename:", "some_filename", stdout)
    if not(output_filename):
        stdout.println("problem found in output_filename: statement")
    return result_permute and result_replace and result_root_dir and result_trials and result_scores_info and output_filename


def validate_statement_present(lines, statement, val, stdout):
    result = True
    value = "unknown"
    statement_command = "unknown"
    for line in lines:
        line = line.rstrip()
        if (line.startswith(statement)):
            # should be one =
            statement_command, value = line.split(":")
    if (statement_command == "unknown"):
        result = False
        stdout.println("cluster_spec missing statement {0}{1}".format(statement, val))
    if (value == "unknown" or value == "" or value == None):
        result = False
        stdout.println("cluster_spec missing value for statement {0}{1}".format(statement, val))
    return result
    

def validate_replace_entries(lines):
    result = True
    for line in lines:
        line = line.rstrip()
        if (line.startswith("<replace>:")):
            line = "".join(line.split()) # remove white spaces
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
    

def validate_permute_entries(lines):
    result = True
    for line in lines:
        line = line.rstrip()
        if (line.startswith("permute:") or line.startswith("(permute):")):
            line = "".join(line.split()) # remove white spaces
            # should be 3 colons
            colon_count = line.count(':')
            if (colon_count != 1):
                print "permute line malformed - {0} - should be permute:var=vals where vals can be:".format(line)
                print "   range of integers with a space    range(1,5) (expanded to 1,2,3,4,5)"
                print "   range of integers with a space    range(1,5,2) (expanded to 1,3,5)"
                print "   single value                    x   (this exposes the value in the permutation code)"
                print "   comma separated list of values  aa,bb,cc"
                result = False
            else:
                permutecommand, permutation_info = line.split(':')
                permuteKey, permute_list_string = permutation_info.split('=')
                if (permute_list_string.startswith("range(")):
                    range_spec = permute_list_string[6:]
                    range_spec_length = len(range_spec)
                    if range_spec[range_spec_length - 1] != ')':
                        print "range spec should be of form range(a,b) or range(a,b,c) : {0}".format(permute_list_string)
                        result = False
                    else: 
                        nums = range_spec.strip(')')
                        numlist = nums.split(",")
                        for num in numlist:
                            if not num.isdigit():
                                print "{0} is not an integer in range: {1}".format(num, line)
                                result = False
                                return

                        start = int(numlist[0])
                        end = int(numlist[1])
                        if (start > end):
                            print "start or range is greater than end {0}".format(line)
                            result = False
                            return
                        if (len(numlist) == 2):
                            result = True
                        elif (len(numlist) == 3):
                            stepInt = int(numlist[2])
                            if not end > stepInt:
                                print "step interval must be less than range end {0}".format(line)
                                result = False
                            else:
                                result = True    
                        else:
                            print "wrong number of digits in range expression - should be range(a,b) or range(a,b,c)"
                            result = False
                elif (permute_list_string.find(",") != -1):
                    # no way I can think of to mess this up
                    pass
                else:
                    # must be a singleton cvalue
                    # no way I can think of to mess this up
                    pass
    return result

def lines_contains_prefix(lines, prefix):
    for line in lines:
        if (line.startswith(prefix)):
            return True
    return False

def validate_scores_gathering_info(lines, stdout):
    x_axis_info_present = lines_contains_prefix(lines, 'scores_x_axis')
    y_axis_info_present = lines_contains_prefix(lines, 'scores_y_axis')
    permute_info_present = lines_contains_prefix(lines, 'scores_permute')
    from_info_present = lines_contains_prefix(lines, 'scores_from')
    to_info_present = lines_contains_prefix(lines, 'scores_to')
    # since scores collection is optional, if none of them are present, cspec is still ok
    if (not(x_axis_info_present) and
        not(y_axis_info_present) and
        not(permute_info_present) and
        not(from_info_present) and
        not(to_info_present)):
        return True
    
    # if any of them are present, then all but the permute line MUST be present
    if (not(x_axis_info_present)):
        print ('missing scores_x_axis: declaration')
        return False
    
    if (not(y_axis_info_present)):
        print ('missing scores_y_axis: declaration')
        return False
    
    if (not(from_info_present)):
        print ('missing scores_from: declaration')
        return False
    
    if (not(to_info_present)):
        print ('missing scores_to: declaration')
        return False
    
    if (not(validate_axis_list(lines,'scores_x_axis:'))):
        print 'problem in scores_x_axis: declaration'
        return False
    
    if (not(validate_axis_list(lines,'scores_y_axis:'))):
        print 'problem in scores_y_axis: declaration'
        return False
    
    if (not(validate_scores_to(lines))):
        print 'problem in scores_to: declaration'
        return False
    
    if (not(validate_scores_from(lines))):
        print 'problem in scores_from: declaration'
        return False
    
    return True

def single_entry_present(lines, prefix):
    count = 0
    for line in lines:
        if (line.startswith(prefix)):
            count = count + 1
    if (count == 1):
        return True
    else:
        return False

def validate_scores_from(lines):
    #scores_from:file=<permutation_output_dir>/(resolution).csv,column_name=auc,row_number=1
    if (not(single_entry_present(lines, 'scores_from:'))):
        print 'more than one entry for scores_from:  Should be one entry'
        return False
    for line in lines:
        line = line.rstrip()
        if (line.startswith('scores_from:')):
            line = "".join(line.split()) # remove white spaces
            flag, from_info = line.split(':')
            path_info, column_info, row_info = from_info.split(',')
            path_flag, path = path_info.split('=')
            if (not(path.startswith('<permutation_output_dir>'))):
                print 'scores_from: entry should start with "<permutation_output_dir>"'
                print 'currently is:  {0}'.format(line)
                return False
            if (not(path.endswith('.csv'))):
                print 'scores_from: entry should have a file that is a .csv file'
                print 'currently is:  {0}'.format(line)
                return False
            column_flag, column_name = column_info.split('=')
            if (not(column_flag == 'column_name')):
                print 'scores_from should be of this form: scores_from:file=<permutation_output_dir>/some_name.csv,column_name=some_col,row_number=some_int'
                print 'currently is:  {0}'.format(line)
                return False
            row_flag, row_num = row_info.split('=')
            if (not(row_flag == 'row_number')):
                print 'scores_from should be of this form: scores_from:file=<permutation_output_dir>/some_name.csv,column_name=some_col,row_number=some_int'
                print 'currently is:  {0}'.format(line)
                return False
            if (not(row_num.isdigit())):
                print 'scores_from should have integer row number'
                print 'currently is:  {0}'.format(line)
                return False
    return True
        
def validate_scores_to(lines):
    if (not(single_entry_present(lines, 'scores_to:'))):
        print 'more than one entry for scores_to:  Should be one entry'
        return False
    for line in lines:
        line = line.rstrip()
        if (line.startswith('scores_to:')):
            line = "".join(line.split()) # remove white spaces
            flag, dir = line.split(':')
            if (os.path.exists(dir)):
                return True
            else:
                os.makedirs(dir)
                if (os.path.exists(dir)):
                    return True
                else:
                    print 'Could not create directory specified in scores_to:'
    return False
    
def validate_axis_list(lines, axis_choice):
    if (not(single_entry_present(lines, axis_choice))):
        print 'more than one entry for {0}.  Should be one entry'.format(axis_choice)
        return False
    for line in lines:
        line = line.rstrip()
        if (line.startswith(axis_choice)):
            line = "".join(line.split()) # remove white spaces
            # grab the list and make sure each entry is a valid permuter
            axis_flag, list_info = line.split(":")
            axis_var_list = list_info.split(',')
            for axis_var in axis_var_list:
                if (not(is_valid_permuter(axis_var, lines))):
                    print "cluster_spec has axis choice for {0} that is not a valid permuter: {1}".format(axis_choice, axis_var) 
                    return False   
    return True

def is_valid_permuter(name, lines):
    for line in lines:
        if (line.startswith('permute:') or line.startswith('scores_permute') or line.startswith('(permute):') or line.startswith('(scores_permute)')):
            line = "".join(line.split()) # remove white spaces
            permute_flag, permute_info = line.split(':')
            permuter_name, vals = permute_info.split('=')
            if permuter_name == name:
                return True
    print 'invalid permuter detected: {0}'.format(name)
    return False


def generate_new_spec(cspec_path):
    new_cspec = new_spec.NewSpec(cspec_path)
    new_cspec.persist()
    
            
            
            
            
            
            
            
            
            
            
            
            
            