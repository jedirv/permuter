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
            
            
            self.permuters = self.load_permutations(self.path)
            self.concise_print_map = self.load_concise_print_map(self.path)
            self.key_val_map = self.load_replaces(self.path)
            self.qsub_commands = self.load_qsub_commands(self.path,self.key_val_map)
            self.commands = self.load_commands(self.path,self.key_val_map)
            self.script_dir = self.load_script_dir(self.path)
            self.one_up_basis = self.load_one_up_basis(self.path)
            #print "done loading cspec"
        except IOError:
            print "An error occured trying to open cspec file {0}".format(path)
            exit()

    def load_one_up_basis(self, path):
        f = open(path, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith("one_up_basis:")):
                command, basis = line.split(":")
                return basis
        return ""
    
      
    def load_script_dir(self, path):
        f = open(path, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith("script_dir:")):
                command, dir = line.split(":")
                dir = resolve_value(self.key_val_map, dir)
                return dir
        # validation pass should prevent the following from ever happening
        return "script_dir_not_specified"
    
    def load_permutations(self, path):
        f = open(path, 'r')
        permuters = {}
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith("permute:")):
                if_verbose("  processing permute line - {0}".format(line))
                permute_command, permute_info = line.split(':')
                permuteKey, permute_list_string = permute_info.split('=')
                if (permute_list_string.find(" ") != -1):
                    permute_start, permute_end = permute_list_string.split(" ")
                    permute_list = range(int(permute_start), int(permute_end)+1)
                    permute_list = map(str, permute_list)
                elif (permute_list_string.find(",") != -1):
                    permute_list = permute_list_string.split(",")
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
    

    def load_qsub_commands(self, path, key_val_map):
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
    
    def load_commands(self, path, key_val_map):
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
    
def validate(path):
    result_permute = validate_permute_entries(path)
    result_replace = validate_replace_entries(path)
    result_script_dir = validate_script_dir(path)
    if not(result_permute):
        print "problem found in permute statements"
    if not(result_replace):
        print "problem found in replace statements"
    if not(result_script_dir):
        print "problem found in script_dir statement"
    return result_permute and result_replace and result_script_dir
    
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
    