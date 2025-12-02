from VirtualMemoryTable import VirtualMemoryTable
from CacheTable import CacheTable
from Tracer import Tracer
from SimulationParameters import SimulationParameters
import math
from SimulationInstructions import SimulationInstructions

class Simulation:
    def __init__(self):
        self.__parameters: SimulationParameters = Tracer().get_simulation_parameters()
        self.__instructions: SimulationInstructions = Tracer().get_simulation_instructions()
        self.__virtual_memory_tables: dict[str, VirtualMemoryTable] = {}
        self.__cache_table = CacheTable(self.__parameters)
        self.__program_output = ""

    def simulate_virtual_memory(self):
        for filename, instructions in  self.__instructions.get_instructions().items():
            virtual_memory_table = VirtualMemoryTable(self.__parameters)
            for instruction in instructions:
                virtual_memory_table.allocate_physical_page(instruction)
            self.__virtual_memory_tables[filename] = virtual_memory_table


    def simulate_cache(self):
        for filename, instructions in  self.__instructions.get_instructions().items():
            for instruction in instructions:
                 self.__cache_table.access_cache(instruction)

    def start(self):
        self.simulate_virtual_memory()
        self.simulate_cache()

    def get_program_output_m1(self):
        self.__program_output += "Cache Simulator - CS 3853 - Team #7\n\n"

        # Input Parameters
        self.__program_output += "Trace File:\n"
        for file in self.__parameters.get_trace_file():
            self.__program_output += f"\t{file}\n"

        self.__program_output += "\n"
        self.__program_output += "***** Cache Input Parameters *****\n\n"
        self.__program_output += "{:<32}".format("Cache Size: ") + str(self.__parameters.get_cache_size_kb()) + " KB\n"
        self.__program_output += "{:<32}".format("Block Size: ") + str(self.__parameters.get_block_size_bytes()) + " bytes\n"
        self.__program_output += "{:<32}".format("Associativity: ") + str(self.__parameters.get_associativity()) + "\n"
        self.__program_output += "{:<32}".format("Replacement Policy: ") + ("Round Robin\n" if self.__parameters.get_replacement_policy() == 'rr' else "Random\n")
        self.__program_output += "{:<32}".format("Physical Memory: ") + str(self.__parameters.get_physical_memory_mb()) + " MB\n"
        self.__program_output += "{:<32}".format("Percent Memory Used by System: ") + str(self.__parameters.get_physical_memory_os_usage()) + "%\n"
        self.__program_output += "{:<32}".format("Instructions / Time Slice: ") + str(self.__parameters.get_instruction_number()) + "\n"
        self.__program_output += "\n"

        # Cache Calculated Values
        self.__program_output += "***** Cache Calculated Values *****\n\n"
        self.__program_output += "{:<32}".format("Total # Blocks: ") + str(self.__parameters.get_total_blocks()) + "\n"
        self.__program_output += "{:<32}".format("Tag Size: ") + str(self.__parameters.get_tag_size_bits()) + " bits\n"
        self.__program_output += "{:<32}".format("Index Size: ") + str(self.__parameters.get_index_size_bits()) + " bits\n"
        self.__program_output += "{:<32}".format("Total # Rows: ") + str(self.__parameters.get_total_rows()) + "\n"
        self.__program_output += "{:<32}".format("Overhead Size: ") + str(self.__parameters.get_overhead_bytes_total()) + " bytes\n"
        self.__program_output += "{:<32}".format("Implementation Memory Size: ") + f"{self.__parameters.get_implementation_memory_kb():.2f} KB ({self.__parameters.get_implementation_memory_bytes()} bytes)\n"
        self.__program_output += "{:<32}".format("Cost: ") + f"${self.__parameters.get_cost():.2f} @ $0.07 per KB\n"
        self.__program_output += "\n"

        # Physical Memory Calculated Values
        self.__program_output += "\n***** Physical Memory Calculated Values *****\n\n"
        self.__program_output += "{:<32}".format("Number of Physical Pages: ") + str(self.__parameters.get_physical_page_number()) + "\n"
        self.__program_output += "{:<32}".format("Number of Pages for System: ") + str(self.__parameters.get_physical_system_page_number()) + "\n"
        self.__program_output += "{:<32}".format("Size of Page Table Entry: ") + str(self.__parameters.get_page_table_entry_bits()) + " bits\n"
        self.__program_output += "{:<32}".format("Total RAM for Page Table(s): ") + str(self.__parameters.get_total_ram_for_page_tables_bytes()) + " bytes\n"
       
        return self.__program_output

    def get_program_output_m2(self):
        self.__program_output += "\n***** VIRTUAL MEMORY SIMULATION RESULTS *****\n\n"
        self.__program_output += "{:<32}".format("Physical Pages Used By SYSTEM: ") +  str(self.__parameters.get_physical_system_page_number()) + "\n"
        self.__program_output += "{:<32}".format("Pages Available to User: ") + str(self.__parameters.get_physical_user_page_number()) + "\n"
        self.__program_output += "\n"
        self.__program_output += "{:<32}".format("Virtual Pages Mapped: ") + str(sum(table.get_virtual_pages_mapped() for table in self.__virtual_memory_tables.values())) + "\n"
        self.__program_output += "\t------------------------------\n"
        self.__program_output += "{:<32}".format("\tPage Table Hits: ") + str(sum(table.get_page_table_hits() for table in self.__virtual_memory_tables.values())) + "\n"
        self.__program_output += "{:<32}".format("\tPages from Free: ") + str(sum(table.get_pages_from_free() for table in self.__virtual_memory_tables.values())) + "\n"
        self.__program_output += "{:<32}".format("\tTotal Page Faults: ") + str(sum(table.get_total_page_faults() for table in self.__virtual_memory_tables.values())) + "\n"
        self.__program_output += "\n"
        self.__program_output += "Page Table Usage Per Process:\n"
        self.__program_output += "------------------------------\n"
        for filename, table in self.__virtual_memory_tables.items():
            self.__program_output += f"[0] {filename}:\n"
            self.__program_output += "{:<32}".format("\tUsed Page Table Entries: ") + str(table.get_used_page_table_entries()) + f" ({table.get_used_page_table_entries_percentage():.6f}%)\n"
            self.__program_output += "{:<32}".format("\tPage Table Wasted: ") + str(table.get_page_table_wasted_bytes()) + " bytes\n"
            self.__program_output += "\n"
        
        return self.__program_output
            
    def get_program_output_m3(self):
        # --- CARLOS: Statistics Calculation Logic ---
        
        # 1. Gather basic stats from CacheTable
        total_accesses = self.__cache_table.get_total_accesses()
        hits = self.__cache_table.get_hits()
        misses = self.__cache_table.get_misses()
        
        # 2. Calculate Rates
        hit_rate = (hits / total_accesses * 100) if total_accesses > 0 else 0
        miss_rate = 100.0 - hit_rate
        
        block_size = self.__parameters.get_block_size_bytes()
        reads_per_block = math.ceil(block_size / 4)
        miss_penalty_cycles = reads_per_block * 4
        
        total_page_faults = sum(table.get_total_page_faults() for table in self.__virtual_memory_tables.values())
        
        # Total Cycles 
        total_cycles = (hits * 1) + \
                       (misses * miss_penalty_cycles) + \
                       (total_page_faults * 100) + \
                       (self.__total_instruction_count * 2) + \
                       (self.__total_data_access_count * 1)
                       
        cpi = total_cycles / self.__total_instruction_count if self.__total_instruction_count > 0 else 0
        
        # 4. Calculate Unused Cache Space
        unused_blocks = self.__cache_table.get_unused_blocks_count()
        total_blocks = self.__parameters.get_total_blocks()
        
        bytes_per_block_entry = self.__parameters.get_block_size_bytes() + (self.__parameters.get_overhead_bits_per_block() / 8)
        
        unused_kb = (unused_blocks * bytes_per_block_entry) / 1024
        total_cache_kb = self.__parameters.get_implementation_memory_kb()
        
        waste_percent = (unused_kb / total_cache_kb * 100) if total_cache_kb > 0 else 0
        total_cost = self.__parameters.get_cost()
        waste_cost = (waste_percent / 100) * total_cost

        # --- Generating Output ---

        self.__program_output += "\n***** CACHE SIMULATION RESULTS *****\n\n"
        self.__program_output += "{:<32}".format("Total Cache Accesses: ") +  str(total_accesses) + "\n"
        self.__program_output += "{:<32}".format("Total Cache Accesses: ") +  str(self.__cache_table.get_total_accesses()) + " (" + str(self.__cache_table.get_addresses_accesses()) + " addresses)" + "\n"
        self.__program_output += "{:<32}".format("--- Instruction Bytes: ") + str(self.__cache_table.get_instruction_bytes()) + "\n"
        self.__program_output += "{:<32}".format("--- SrcDst Bytes: ") + str(self.__cache_table.get_SrcDst_bytes()) + "\n"

        self.__program_output += "{:<32}".format("Cache Hits: ") + str(hits) + "\n"
        self.__program_output += "{:<32}".format("Cache Misses: ") + str(misses) + "\n"
        self.__program_output += "{:<32}".format("--- Compulsory Misses: ") + str(self.__cache_table.get_compulsory()) + "\n"
        self.__program_output += "{:<32}".format("--- Conflict Misses: ") + str(self.__cache_table.get_conflict()) + "\n"

        self.__program_output += "\n\n***** ***** CACHE SIMULATION RESULTS ***** *****\n\n"
        self.__program_output += "{:<32}".format("Hit Rate: ") + f"{hit_rate:.4f}%" + "\n"
        self.__program_output += "{:<32}".format("Miss Rate: ") + f"{miss_rate:.4f}%" + "\n"
        self.__program_output += "{:<32}".format("CPI: ") + f"{cpi:.2f} Cycles/Instruction ({int(total_cycles)})" + "\n"
        
        self.__program_output += "{:<32}".format("Unused Cache Space: ") + \
                                 f"{unused_kb:.2f} KB / {total_cache_kb:.2f} KB = {waste_percent:.2f}% Waste: ${waste_cost:.2f}/chip" + "\n"
                                 
        self.__program_output += "{:<32}".format("Unused Cache Blocks: ") + f"{unused_blocks} / {total_blocks}" + "\n"
        self.__program_output += "{:<32}".format("Hit Rate: ") + str(self.__cache_table.get_hit_rate()) + "%\n"
        self.__program_output += "{:<32}".format("Miss Rate: ") + str(self.__cache_table.get_miss_rate()) + "%\n"
        self.__program_output += "{:<32}".format("CPI: ") + str(00000) + "\n"
        self.__program_output += "{:<32}".format("Unused Cache Space: ") + str(00000) + "\n"
        self.__program_output += "{:<32}".format("Unused Cache Blocks: ") + str(0000) + "\n"

        return self.__program_output