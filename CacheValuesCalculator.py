import argparse
import math

class CacheValuesCalculator:
    
# Maryna Korolova part starts here :)

    def __init__(self):
        self.__cache_size = None
        self.__block_size = None
        self.__associativity = None
        self.__replacement_policy = None
        self.__physical_memory = None
        self.__physical_memory_os_usage = None
        self.__instructions = None
        self.__virtual_address_space = 31  # in bits
        self.__page_size = 4096  # 4KB final page size
        self.__pte_entries_per_process = 524288 # 2^19 or 512K entries
        self.__page_table_entry_bits = 19  # 18 bits for PPN + 1 valid bit
        self.__trace_file = []

        self.__program_output = ""
        self.load()

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

    def get_cache_size(self):
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
    
    def get_page_size(self):
        return self.__page_size
        
    # --------------- Print menu for Config Values -----------------

    def print_config(self):
        print(f"Trace File:")
        for file in self.get_trace_file():
            print(f"\t{file}")
        print()
        print(f"***** Cache Input Parameters *****\n")
        print("{:<28}".format("Cache Size: ") + str(self.get_cache_size()) + " KB")
        print("{:<28}".format("Block Size: ") + str(self.get_block_size()) + " bytes")
        print("{:<28}".format("Associativity: ") + str(self.get_associativity()))
        print("{:<28}".format("Replacement Policy: ") + ("Round Robin" if self.get_replacement_policy() == 'rr' else "Random"))
        print("{:<28}".format("Physical Memory: ") + str(self.get_physical_memory()) + " MB")
        print("{:<28}".format("Percent Memory Used by System: ") + str(self.get_physical_memory_os_usage()) + "%")
        print("{:<28}".format("Instructions / Time Slice: ") + str(self.get_instructions())) #Number of Instructions
        print()

# Christopher Peters Part starts here >:) 

    # ---------- Cache Calculated Values ----------
    
    def get_cache_size_bytes(self):
        return self.get_cache_size() * 1024
    
    def get_total_blocks(self):
        return self.get_cache_size_bytes() // self.get_block_size()
    
    def get_total_rows(self):
        return self.get_total_blocks() // self.get_associativity()
    
    def get_index_size(self):
        return int(math.log2(self.get_total_rows()))
    
    def get_offset_size(self):
        return int(math.log2(self.get_block_size()))
    
    def get_physical_memory_bytes(self):
        return self.get_physical_memory() * 1024 * 1024
    
    def get_total_address_bits(self):
        return int(math.log2(self.get_physical_memory_bytes()))
    
    def get_tag_size(self):
        return self.get_total_address_bits() - self.get_index_size() - self.get_offset_size()
    
    def get_overhead_bits_per_block(self):
        return 1 + self.get_tag_size()
    
    def get_total_overhead_bits(self):
        return self.get_overhead_bits_per_block() * self.get_total_blocks()
    
    def get_overhead_bytes(self):
        return math.ceil(self.get_total_overhead_bits() / 8)
    
    def get_implementation_memory_bytes(self):
        return self.get_cache_size_bytes() + self.get_overhead_bytes()
    
    def get_implementation_memory_kb(self):
        return self.get_implementation_memory_bytes() / 1024
    
    def get_cost(self):
        return self.get_implementation_memory_kb() * 0.07
    
    # --------------- Print menu for Cache Calculated Values -----------------
    
    def print_cache_calculated_values(self):
        print("***** Cache Calculated Values *****\n")
        print(f"Total # Blocks:                  {self.get_total_blocks()}")
        print(f"Tag Size:                        {self.get_tag_size()} bits")
        print(f"Index Size:                      {self.get_index_size()} bits")
        print(f"Total # Rows:                    {self.get_total_rows()}")
        print(f"Overhead Size:                   {self.get_overhead_bytes()} bytes")
        print(f"Implementation Memory Size:      {self.get_implementation_memory_kb():.2f} KB ({self.get_implementation_memory_bytes()} bytes)")
        print(f"Cost:                            ${self.get_cost():.2f} @ $0.07 per KB")
        print()


# Carlos Mejia Rosales Part starts here :(

    # ---------- Physical Memory Calculated Values ----------

    def get_number_physical_pages(self):
        return self.get_physical_memory_bytes() // self.get_page_size()
    
    def get_number_system_pages(self):
        return int(self.get_physical_memory_os_usage() / 100.0 * self.get_number_physical_pages())
    
    def get_number_available_to_user_pages(self):
        return self.get_number_physical_pages() - self.get_number_system_pages()

    def get_page_table_entry_bits(self):
        return self.__page_table_entry_bits
    
    def get_total_ram_for_page_tables_bytes(self):
        total_bits = self.__pte_entries_per_process * len(self.get_trace_file()) * self.get_page_table_entry_bits()
        return total_bits // 8

    def print_physical_memory_calculations(self):
        print("***** Physical Memory Calculated Values *****\n")
        print(f"Number of Physical Pages: {self.get_number_physical_pages():>20}")
        print(f"Number of Pages for System: {self.get_number_system_pages():>18}")
        print(f"Size of Page Table Entry: {self.get_page_table_entry_bits():>20} bits")
        print(f"Total RAM for Page Table(s): {self.get_total_ram_for_page_tables_bytes():>15} bytes")


    def get_program_output(self):

        self.__program_output += "Cache Simulator - CS 3853 - Team #7\n\n"

        # Input Parameters
        self.__program_output += "Trace File:\n"
        for file in self.get_trace_file():
            self.__program_output += f"\t{file}\n"

        self.__program_output += "\n"
        self.__program_output += "***** Cache Input Parameters *****\n\n"
        self.__program_output += "{:<32}".format("Cache Size: ") + str(self.get_cache_size()) + " KB\n"
        self.__program_output += "{:<32}".format("Block Size: ") + str(self.get_block_size()) + " bytes\n"
        self.__program_output += "{:<32}".format("Associativity: ") + str(self.get_associativity()) + "\n"
        self.__program_output += "{:<32}".format("Replacement Policy: ") + ("Round Robin\n" if self.get_replacement_policy() == 'rr' else "Random\n")
        self.__program_output += "{:<32}".format("Physical Memory: ") + str(self.get_physical_memory()) + " MB\n"
        self.__program_output += "{:<32}".format("Percent Memory Used by System: ") + str(self.get_physical_memory_os_usage()) + "%\n"
        self.__program_output += "{:<32}".format("Instructions / Time Slice: ") + str(self.get_instructions()) + "\n"
        self.__program_output += "\n"

        # Cache Calculated Values
        self.__program_output += "***** Cache Calculated Values *****\n\n"
        self.__program_output += "{:<32}".format("Total # Blocks: ") + str(self.get_total_blocks()) + "\n"
        self.__program_output += "{:<32}".format("Tag Size: ") + str(self.get_tag_size()) + "\n"
        self.__program_output += "{:<32}".format("Index Size: ") + str(self.get_index_size()) + "\n"
        self.__program_output += "{:<32}".format("Total # Rows: ") + str(self.get_total_rows()) + "\n"
        self.__program_output += "{:<32}".format("Overhead Size: ") + str(self.get_overhead_bytes()) + " bytes\n"
        self.__program_output += "{:<32}".format("Implementation Memory Size: ") + f"{self.get_implementation_memory_kb():.2f} KB ({self.get_implementation_memory_bytes()} bytes)\n"
        self.__program_output += "{:<32}".format("Cost: ") + f"${self.get_cost():.2f} @ $0.07 per KB\n"
        self.__program_output += "\n"

        # Physical Memory Calculated Values
        self.__program_output += "\n***** Physical Memory Calculated Values *****\n\n"
        self.__program_output += "{:<32}".format("Number of Physical Pages: ") + str(self.get_number_physical_pages()) + "\n"
        self.__program_output += "{:<32}".format("Number of Pages for System: ") + str(self.get_number_system_pages()) + "\n"
        self.__program_output += "{:<32}".format("Size of Page Table Entry: ") + str(self.get_page_table_entry_bits()) + " bits\n"
        self.__program_output += "{:<32}".format("Total RAM for Page Table(s): ") + str(self.get_total_ram_for_page_tables_bytes()) + " bytes\n"
       
        return self.__program_output