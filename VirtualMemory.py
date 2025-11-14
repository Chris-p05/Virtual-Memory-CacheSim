import re
import math

from FileTracer import FileTracer

# Christopher Peters Part starts here >:) 
class VirtualMemory:
    print(" Virtual Memory Simulator for Milestone #2Handles page table management and address mapping")
    
    def __init__(self, physical_memory_mb, percent_system, trace_files):

        self.__physical_memory_mb = physical_memory_mb
        self.__percent_system = percent_system
        self.__trace_files = trace_files
        self.__page_size = 4096
        self.__page_tables = [{} for _ in range(len(trace_files))]
        self.__free_physical_pages = set()

        # Data for output statistics
        self.__virtual_pages_mapped = 0
        self.__page_table_hits = 0
        self.__pages_from_free = 0
        self.__total_page_faults = 0
        
        self.file_tracer = FileTracer()
        
        self._initialize_free_pages()
    
    def _initialize_free_pages(self):
        total_physical_pages = self.get_num_physical_pages()
        system_pages = self.get_num_system_pages()
        
        for page_num in range(system_pages, total_physical_pages):
            self.__free_physical_pages.add(page_num)
    
    def get_num_physical_pages(self):
        physical_memory_bytes = self.__physical_memory_mb * 1024 * 1024
        return physical_memory_bytes // self.__page_size
    
    def get_num_system_pages(self):
        return int(self.__percent_system / 100.0 * self.get_num_physical_pages())
    
    def get_pages_available_to_user(self):
        return self.get_num_physical_pages() - self.get_num_system_pages()
    
    def get_virtual_page_number(self, address):
        return address // self.__page_size
    
    def allocate_physical_page(self, process_id, virtual_page):
        if virtual_page in self.__page_tables[process_id]:
            self.__page_table_hits += 1
            return self.__page_tables[process_id][virtual_page]

        if len(self.__free_physical_pages) > 0:
            physical_page = self.__free_physical_pages.pop()
            self.__page_tables[process_id][virtual_page] = physical_page
            self.__pages_from_free += 1
            return physical_page
        else:
            self.__total_page_faults += 1
            return None

    def process_trace_files(self):
        for process_id, trace_file in enumerate(self.__trace_files):
            data = self.file_tracer.parse_trace_file(trace_file)
            for address, length, addr_type in data:
                virtual_page = self.get_virtual_page_number(address)
                self.__virtual_pages_mapped += 1
                self.allocate_physical_page(process_id, virtual_page)
                    
    def get_page_table_wasted_bytes(self, process_id, page_table_entry_bits):
        entries_per_table = 512 * 1024  
        used_entries = len(self.__page_tables[process_id])
        total_bytes_allocated = math.ceil((entries_per_table * page_table_entry_bits) / 8)
        used_bytes = math.ceil((used_entries * page_table_entry_bits) / 8)
        return total_bytes_allocated - used_bytes
    

    def print_virtual_memory_results(self):
        """Print Virtual Memory Simulation Results"""
        print(f"Virtual Pages Mapped:            {self.__virtual_pages_mapped}")
        print("------------------------------")
        print(f"Page Table Hits:                 {self.__page_table_hits} - the virtual page is already mapped in")
        print("                                 the page table - a hit!")
        print(f"Pages from Free:                 {self.__pages_from_free} - # times a virtual page is mapped to a")
        print("                                 physical page not currently in use")
        print(f"Total Page Faults:               {self.__total_page_faults} - # times when no physical page is available")
        print("                                 and must be swapped with one in use")
        print()