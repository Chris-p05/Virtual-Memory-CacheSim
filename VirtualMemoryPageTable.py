import math
from CacheValuesCalculator import CacheValuesCalculator

# Christopher Peters and Maryna Korolova Part starts here >:) 

class VirtualMemoryPageTable:
    def __init__(self):
        self.__process_name = ""
        self.cache_values_calculator = CacheValuesCalculator()
        self.__page_table = {} # virtual page_number -> physical_page_number
        self.__page_table_entry_bits = 19  # bits per page table entry

    def set_process_name(self, name):
        self.__process_name = name

    def get_process_name(self): 
        return self.__process_name

    def get_physical_page(self, virtual_page):
        return self.__page_table.get(virtual_page)

    def map_virtual_to_physical(self, virtual_page, physical_page):
        self.__page_table[virtual_page] = physical_page

    def is_mapped(self, virtual_page):
        return virtual_page in self.__page_table

    def get_page_size(self):
        return self.cache_values_calculator.get_page_size()

    def get_used_page_table_entries(self):
        return len(self.__page_table)
    
    def get_page_table_entries(self):
        return 2 ** (self.cache_values_calculator.get_virtual_address_space() - int(math.log2(self.cache_values_calculator.get_page_size())))

    def get_used_page_table_entries_percentage(self):
        return (self.get_used_page_table_entries() /  self.get_page_table_entries()) * 100 if  self.get_page_table_entries() > 0 else 0

    def get_page_table_wasted_bytes(self):
        return ( self.get_page_table_entries() - self.get_used_page_table_entries()) * (self.__page_table_entry_bits // 8)