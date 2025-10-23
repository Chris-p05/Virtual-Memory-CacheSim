import argparse

class FileTracer:
    
    def __init__(self):
        self.__cache_size = None
        self.__block_size = None
        self.__associativity = None
        self.__replacement_policy = None
        self.__physical_memory = None
        self.__physical_memory_os_usage = None
        self.__instructions = None
        self.__virtual_address_space = 32  # in bits
        self.__trace_file = []

    def load(self):

        parser = argparse.ArgumentParser(description = 'VM Cache Simulator')

        parser.add_argument(
            '-s', 
            '--cache-size',
            type = int,
            choices = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096],
            required = True
        )
        parser.add_argument(
            '-b',
            '--block-size',
            type = int,
            choices = [8, 16, 32, 64],
            required= True
        )
        parser.add_argument(
            '-a',
            '--associativty',
            type = int,
            choices = [2, 4, 8, 16],
            required = True
        )
        parser.add_argument(
            '-r',
            '--replacement-policy',
            type = str,
            choices = ["r", "rr"],
            required = True
        )
        parser.add_argument(
            '-p',
            '--physical-memory',
            type = int,
            choices=[128, 256, 512, 1024, 2048, 4096],
            required = True
        )
        parser.add_argument(
            '-u',
            '--physical-memory-os-usage',
            type = int,
            choices=range(1, 101),
            required = True
        )
        parser.add_argument(
            '-n',
            '--instructions',
            type = int,
            required = True
        )
        parser.add_argument(
            '-f',
            '--trace-file',
            action='append',
            type=str,
            required=True,
            help='Specify 1-3 trace files'
        )

        args = parser.parse_args()

        self.__cache_size = args.cache_size
        self.__block_size = args.block_size
        self.__associativity = args.associativty
        self.__replacement_policy = args.replacement_policy
        self.__physical_memory = args.physical_memory
        self.__physical_memory_os_usage = args.physical_memory_os_usage
        self.__instructions = args.instructions
        

        if not (1 <= len(args.trace_file) <= 3):
            parser.error("argument -f/--trace-file: must be given between 1 and 3 times")

        self.__trace_file = args.trace_file

        return self
    
    def print_config(self):
        print(f"Trace File:")
        for file in self.get_trace_file():
            print(f"\t{file}")
        print()
        print(f"***** Cache Input Parameters *****")
        print("{:<28}".format("Cache Size: ") + str(self.get_chache_size()) + " KB")
        print("{:<28}".format("Block Size: ") + str(self.get_block_size()) + " bytes")
        print("{:<28}".format("Associativity: ") + str(self.get_associativity()))
        print("{:<28}".format("Replacement Policy: ") + ("Round Robin" if self.get_replacement_policy() == 'rr' else "Random"))
        print("{:<28}".format("Physical Memory Size: ") + str(self.get_physical_memory()) + " MB")
        print("{:<28}".format("Physical Memory OS Usage: ") + str(self.get_physical_memory_os_usage()) + "%")
        print("{:<28}".format("Number of Instructions: ") + str(self.get_instructions()))

        print()

    def get_chache_size(self):
        return self.__cache_size
        
    def get_block_size(self):
        return self.__block_size
    
    def get_associativity(self):
        return self.__associativity
    
    def get_replacement_policy(self):
        return self.__replacement_policy
    
    def get_physical_memory(self):
        return self.__physical_memory
    
    def get_physical_memory_os_usage(self):
        return self.__physical_memory_os_usage
    
    def get_instructions(self):
        return self.__instructions
    
    def get_trace_file(self):
        return self.__trace_file
    
    def get_virtual_address_space(self):
        return self.__virtual_address_space
   
    