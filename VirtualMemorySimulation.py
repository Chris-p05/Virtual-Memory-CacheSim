from FileTracer import FileTracer
from CacheValuesCalculator import CacheValuesCalculator
from VirtualMemoryPageTable import VirtualMemoryPageTable
from FreePhysicalMemoryPageTable import FreePhysicalMemoryPageTable

# Christopher Peters and Maryna Korolova Part starts here >:) 
class VirtualMemorySimulation:
    
    def __init__(self):
        self.__cache_values_calculator = CacheValuesCalculator()
        self.__file_tracer = FileTracer()
        self.__free_physical_memory_pages_table = FreePhysicalMemoryPageTable()
        self.__virtual_memory_page_tables = [VirtualMemoryPageTable() for _ in range(len(self.__cache_values_calculator.get_trace_file()))]

        # Data for output statistics
        self.__virtual_pages_mapped = 0
        self.__page_table_hits = 0
        self.__pages_from_free = 0
        self.__total_page_faults = 0

        self.__program_output = ""

        self.load()
        
    def get_virtual_pages_mapped(self):
        return self.__virtual_pages_mapped\
        
    def get_page_table_hits(self):
        return self.__page_table_hits
    
    def get_pages_from_free(self):
        return self.__pages_from_free
    
    def get_total_page_faults(self):
        return self.__total_page_faults

    def get_virtual_page_number(self, address):
        return address // self.__cache_values_calculator.get_page_size()

    def allocate_physical_page(self, process_id, virtual_page):
        if self.__virtual_memory_page_tables[process_id].is_mapped(virtual_page):
            self.__page_table_hits += 1
            return self.__virtual_memory_page_tables[process_id].get_physical_page(virtual_page)

        if self.__free_physical_memory_pages_table.get_free_page_count() > 0:
            self.__virtual_memory_page_tables[process_id].map_virtual_to_physical(virtual_page, self.__free_physical_memory_pages_table.get_free_page())
            self.__pages_from_free += 1
            return self.__virtual_memory_page_tables[process_id].get_physical_page(virtual_page)
        else:
            self.__total_page_faults += 1
            return None

    def load(self):
        for process_id, trace_file in enumerate(self.__cache_values_calculator.get_trace_file()):
            self.__virtual_memory_page_tables[process_id].set_process_name(f"{trace_file}")
            data = self.__file_tracer.parse_trace_file(trace_file)
            for address, length, addr_type in data:
                virtual_page = self.get_virtual_page_number(address)
                self.__virtual_pages_mapped += 1
                self.allocate_physical_page(process_id, virtual_page)

    def get_program_output(self):
        self.__program_output += "\n***** VIRTUAL MEMORY SIMULATION RESULTS *****\n\n"
        self.__program_output += "{:<32}".format("Physical Pages Used By SYSTEM: ") +  str(self.__cache_values_calculator.get_number_system_pages()) + "\n"
        self.__program_output += "{:<32}".format("Pages Available to User: ") + str(self.__cache_values_calculator.get_number_available_to_user_pages()) + "\n"
        self.__program_output += "\n"
        self.__program_output += "{:<32}".format("Virtual Pages Mapped: ") + str(self.get_virtual_pages_mapped()) + "\n"
        self.__program_output += "\t------------------------------\n"
        self.__program_output += "{:<32}".format("\tPage Table Hits: ") + str(self.get_page_table_hits()) + "\n"
        self.__program_output += "{:<32}".format("\tPages from Free: ") + str(self.get_pages_from_free()) + "\n"
        self.__program_output += "{:<32}".format("\tTotal Page Faults: ") + str(self.get_total_page_faults()) + "\n"
        self.__program_output += "\n"
        self.__program_output += "Page Table Usage Per Process:\n"
        self.__program_output += "------------------------------\n"
        for index, table in enumerate(self.__virtual_memory_page_tables):
            self.__program_output += f"[{index}] {table.get_process_name()}:\n"
            self.__program_output += "{:<32}".format("\tUsed Page Table Entries: ") + str(table.get_used_page_table_entries()) + f" ({table.get_used_page_table_entries_percentage():.6f}%)\n"
            self.__program_output += "{:<32}".format("\tPage Table Wasted: ") + str(table.get_page_table_wasted_bytes()) + " bytes\n"
            self.__program_output += "\n"
            
        return self.__program_output

    def print_virtual_memory_results(self):
        print("***** VIRTUAL MEMORY SIMULATION RESULTS *****\n")
        print("{:<32}".format("Physical Pages Used By SYSTEM: ") + str(self.__cache_values_calculator.get_number_system_pages()) + "\n")
        print("{:<32}".format("Pages Available to User: ") + str(self.__cache_values_calculator.get_number_available_to_user_pages()) + "\n")
        print("{:<32}".format("Virtual Pages Mapped: ") + str(self.get_virtual_pages_mapped()))
        print("------------------------------")
        print("{:<32}".format("Page Table Hits: ") + str(self.get_page_table_hits()))
        print("{:<32}".format("Pages from Free: ") + str(self.get_pages_from_free()))
        print("{:<32}".format("Total Page Faults: ") + str(self.get_total_page_faults()))
        print()
        print("Page Table Usage Per Process:")
        print("------------------------------")
        for index, table in enumerate(self.__virtual_memory_page_tables):
            print(f"[{index}] {table.get_process_name()}:\n")
            print("{:<32}".format("\tUsed Page Table Entries: ") + str(table.get_used_page_table_entries()) + f" ({table.get_used_page_table_entries_percentage():.6f}%)\n")
            print("{:<32}".format("\tPage Table Wasted: ") + str(table.get_page_table_wasted_bytes()) + " bytes")
            print()