import re
import math

from FileTracer import FileTracer
from CacheValuesCalculator import CacheValuesCalculator
from VirtualMemoryPageTable import VirtualMemoryPageTable
from FreePhysicalMemoryPageTable import FreePhysicalMemoryPageTable

# Christopher Peters Part starts here >:) 
class VirtualMemory:
    
    def __init__(self):
        self.__cache_values_calculator = CacheValuesCalculator()
        self.__free_physical_memory_pages_table = FreePhysicalMemoryPageTable()
        self.__virtual_memory_page_tables = [VirtualMemoryPageTable() for _ in range(len(self.__cache_values_calculator.get_trace_file()))]

        # Data for output statistics
        self.__virtual_pages_mapped = 0
        self.__page_table_hits = 0
        self.__pages_from_free = 0
        self.__total_page_faults = 0
        
        self.file_tracer = FileTracer()

    def get_virtual_page_number(self, address):
        return address // self.__cache_values_calculator.get_page_size()

    def allocate_physical_page(self, process_id, virtual_page):
        if self.__virtual_memory_page_tables[process_id].is_mapped(virtual_page):
            self.__page_table_hits += 1
            return self.__virtual_memory_page_tables[process_id].get_physical_page(virtual_page)

        if self.__free_physical_memory_pages_table.get_free_page_count() > 0:
            self.__virtual_memory_page_tables[process_id].map_virtual_to_physical(virtual_page, self.__free_physical_memory_pages_table.allocate_page)
            self.__pages_from_free += 1
            return self.__virtual_memory_page_tables[process_id].get_physical_page(virtual_page)
        else:
            self.__total_page_faults += 1
            return None

    def process_trace_files(self):
        for process_id, trace_file in enumerate(self.__cache_values_calculator.get_trace_file()):
            data = self.file_tracer.parse_trace_file(trace_file)
            for address, length, addr_type in data:
                virtual_page = self.get_virtual_page_number(address)
                self.__virtual_pages_mapped += 1
                self.allocate_physical_page(process_id, virtual_page)

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
        print("Page Table Usage Per Process:")
        print("------------------------------")
        for table in self.__virtual_memory_page_tables:
            print(f"Used Page Table Entries: {table.get_used_page_table_entries()} ( {table.get_used_page_table_entries_percentage():.6f}%)")
            #print(f"Total Page Table Entries: {table.get_page_table_entries()}")
            print(f"Page Table Wasted: {table.get_page_table_wasted_bytes()} bytes")
            print()