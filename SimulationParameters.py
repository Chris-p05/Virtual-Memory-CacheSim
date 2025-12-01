import math
from Instruction import Instruction

class SimulationParametersBuilder:
    def __init__(self):
        self.instructions: dict[str, List[Instruction]] = {}

        ##os
        self.page_size = None  # 4KB final page size
        self.physical_memory_os_usage = None
        self.physical_system_page_number = None
        self.physical_user_page_number = None
        self.total_ram_for_page_tables_bytes = None

        ## Virtual memory Parameters 
        self.instruction_number = None
        self.virtual_address_space = None  # in bits
        self.pte_entries_per_process = None # 2^19 or 512K entries
        self.page_table_entry_bits = None  # 18 bits for PPN + 1 valid bit
        
        ##Cache Parameters
        self.cache_size_kb = None
        self.cache_size_bytes = None
        self.block_size_bytes = None
        self.associativity = None
        self.replacement_policy = None
        self.total_blocks = None
        self.total_rows = None
        self.total_address_size_bits = None
        self.index_size_bits = None
        self.offset_size_bits = None
        self.tag_size_bits = None
        self.overhead_bits_per_block = None
        self.overhead_bits_total = None
        self.overhead_bytes_total = None
        self.implementation_memory_bytes = None
        self.implementation_memory_kb = None
        self.cost = None

        ##Physical memory Parameters
        self.physical_memory_mb = None
        self.physical_memory_bytes = None
        self.physical_page_number = None

        ## files
        self.trace_file = []

    def build(self):
        return SimulationParameters(self)

    def set_arg(self, arg):
        self.trace_file = arg.trace_files
        self.page_size= 4096

        #Virtual memory 
        self.instruction_number = arg.instructions
        self.virtual_address_space = 31
        self.pte_entries_per_process = 524288
        self.page_table_entry_bits = 19
        self.total_ram_for_page_tables_bytes = (self.pte_entries_per_process * len(self.trace_file) * self.page_table_entry_bits) // 8 

        # Physical memory
        self.physical_memory_mb = arg.physical_memory
        self.physical_memory_bytes = self.physical_memory_mb * 1024 * 1024
        self.physical_page_number = self.physical_memory_bytes // self.page_size
        self.physical_memory_os_usage = arg.physical_memory_os_usage
        self.physical_system_page_number = int(self.physical_memory_os_usage / 100.0 * self.physical_page_number)
        self.physical_user_page_number = self.physical_page_number - self. physical_system_page_number

        # Cache
        self.cache_size_kb = arg.cache_size
        self.cache_size_bytes = self.cache_size_kb * 1024
        self.block_size_bytes = arg.block_size
        self.associativity = arg.associativity
        self.replacement_policy = arg.replacement_policy 
        self.total_blocks = self.cache_size_bytes // self.block_size_bytes
        self.total_rows = self.total_blocks // self.associativity
        self.total_address_size_bits = int(math.log2(self.physical_memory_bytes))
        self.index_size_bits = int(math.log2(self.total_rows))
        self.offset_size_bits = int(math.log2(self.block_size_bytes))
        self.tag_size_bits = self.total_address_size_bits -  self.index_size_bits - self.offset_size_bits
        self.overhead_bits_per_block = 1 + self.tag_size_bits
        self.overhead_bits_total = self.overhead_bits_per_block * self.total_blocks
        self.overhead_bytes_total = math.ceil(self.overhead_bits_total / 8)
        self.implementation_memory_bytes = self.cache_size_bytes + self.overhead_bytes_total
        self.implementation_memory_kb = self.implementation_memory_bytes / 1024
        self.cost = self.implementation_memory_kb * 0.07

        return self



class SimulationParameters:

    def __init__ (self, builder:SimulationParametersBuilder):

        ##os
        self.__page_size = builder.page_size # 4KB final page size
        self.__physical_memory_os_usage = builder.physical_memory_os_usage
        self.__physical_system_page_number = builder.physical_system_page_number
        self.__physical_user_page_number = builder.physical_user_page_number
        self.__total_ram_for_page_tables_bytes = builder.total_ram_for_page_tables_bytes

        ## Virtual memory Parameters 
        self.__instruction_number = builder.instruction_number
        self.__virtual_address_space = builder.virtual_address_space  # in bits
        self.__pte_entries_per_process = builder.pte_entries_per_process # 2^19 or 512K entries
        self.__page_table_entry_bits = builder.page_table_entry_bits  # 18 bits for PPN + 1 valid bit
        
        ##Cache Parameters
        self.__cache_size_kb = builder.cache_size_kb
        self.__cache_size_bytes = builder.cache_size_bytes
        self.__block_size_bytes = builder.block_size_bytes
        self.__associativity = builder.associativity
        self.__replacement_policy = builder.replacement_policy
        self.__total_blocks = builder.total_blocks
        self.__total_rows = builder.total_rows
        self.__total_address_size_bits = builder.total_address_size_bits
        self.__index_size_bits = builder.index_size_bits
        self.__offset_size_bits = builder.offset_size_bits
        self.__tag_size_bits = builder.tag_size_bits
        self.__overhead_bits_per_block = builder.overhead_bits_per_block
        self.__overhead_bits_total = builder.overhead_bits_total
        self.__overhead_bytes_total = builder.overhead_bytes_total
        self.__implementation_memory_bytes = builder.implementation_memory_bytes
        self.__implementation_memory_kb = builder.implementation_memory_kb
        self.__cost = builder.cost

        ##Physical memory Parameters
        self.__physical_memory_mb = builder.physical_memory_mb
        self.__physical_memory_bytes = builder.physical_memory_bytes
        self.__physical_page_number = builder.physical_page_number

        ## files
        self.__trace_file = builder.trace_file
        
    ## OS
    def get_page_size(self): return self.__page_size
    def get_physical_memory_os_usage(self): return self.__physical_memory_os_usage
    def get_physical_system_page_number(self): return self.__physical_system_page_number
    def get_physical_user_page_number(self): return self.__physical_user_page_number
    def get_total_ram_for_page_tables_bytes(self): return self.__total_ram_for_page_tables_bytes

    ## Virtual Memory
    def get_instruction_number(self): return self.__instruction_number
    def get_virtual_address_space(self): return self.__virtual_address_space
    def get_pte_entries_per_process(self): return self.__pte_entries_per_process
    def get_page_table_entry_bits(self): return self.__page_table_entry_bits

    ## Cache
    def get_cache_size_kb(self): return self.__cache_size_kb
    def get_cache_size_bytes(self): return self.__cache_size_bytes
    def get_block_size_bytes(self): return self.__block_size_bytes
    def get_associativity(self): return self.__associativity
    def get_replacement_policy(self): return self.__replacement_policy
    def get_total_blocks(self): return self.__total_blocks
    def get_total_rows(self): return self.__total_rows
    def get_total_address_size_bits(self): return self.__total_address_size_bits
    def get_index_size_bits(self): return self.__index_size_bits
    def get_offset_size_bits(self): return self.__offset_size_bits
    def get_tag_size_bits(self): return self.__tag_size_bits
    def get_overhead_bits_per_block(self): return self.__overhead_bits_per_block
    def get_overhead_bits_total(self): return self.__overhead_bits_total
    def get_overhead_bytes_total(self): return self.__overhead_bytes_total
    def get_implementation_memory_bytes(self): return self.__implementation_memory_bytes
    def get_implementation_memory_kb(self): return self.__implementation_memory_kb
    def get_cost(self): return self.__cost

    ## Physical Memory
    def get_physical_memory_mb(self): return self.__physical_memory_mb
    def get_physical_memory_bytes(self): return self.__physical_memory_bytes
    def get_physical_page_number(self): return self.__physical_page_number

    ## Files
    def get_trace_file(self): return self.__trace_file

