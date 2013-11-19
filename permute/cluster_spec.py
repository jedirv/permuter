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
            self.key_val_map = self.load_key_val_map(self.path)
            self.qsub_commands = self.load_qsub_commands(self.path,self.key_val_map)
            self.commands = self.load_commands(self.path,self.key_val_map)
        except IOError:
            print "An error occured trying to open cspec file {0}".format(path)
            exit()

      
    def validate(self):
        pass

    
    def load_permutations(self, path):
        f = open(path, 'r')
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
    
    def load_key_val_map(self, path):
        f = open(path, 'r')
        key_val_map = {}
        # set default tag as empty string
        key_val_map['tag'] = ""
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if (line.startswith("#")):
                pass
            elif (line.find("=") != -1):
                if_verbose("  processing keyVal line - {0}".format(line))
                key, val = line.split("=")
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
    