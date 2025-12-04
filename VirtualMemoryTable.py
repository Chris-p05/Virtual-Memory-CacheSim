import math
from SimulationParameters import SimulationParameters
from PhysicalMemoryTable import PhysicalMemoryTable

# Christopher Peters and Maryna Korolova Part starts here >:) 

class VirtualMemoryTable:
    def __init__(self, physical_memory_table:PhysicalMemoryTable, parameters:SimulationParameters):
        self.__parameters = parameters
        self.__virtual_memory_table = {} # virtual page_number -> physical_page_number
        self.__physical_memory_table = physical_memory_table #PhysicalMemoryTable(self.__parameters)

        #satistic
        self.__virtual_pages_mapped = 0
        self.__page_table_hits = 0
        self.__pages_from_free = 0
        self.__total_page_faults = 0


    def get_physical_page(self, virtual_page):
        return self.__virtual_memory_table.get(virtual_page)

    def map_virtual_to_physical(self, virtual_page, physical_page):
        self.__virtual_memory_table[virtual_page] = physical_page

    def is_mapped(self, virtual_page):
        return virtual_page in self.__virtual_memory_table

    def allocate_physical_page(self, instruction):
        virtual_page = instruction.get_virtual_pages_number()
        physical_page = None

        self.__virtual_pages_mapped += 1
        if self.is_mapped(virtual_page):
            self.__page_table_hits += 1
            physical_page = self.get_physical_page(virtual_page)

        else:

            if self.__physical_memory_table.get_free_page_count() > 0:
                self.map_virtual_to_physical(virtual_page, self.__physical_memory_table.get_free_page())
                self.__pages_from_free += 1
                physical_page = self.get_physical_page(virtual_page)

            else:
                self.__total_page_faults += 1

        instruction.set_physical_page_number(physical_page)

    def get_virtual_pages_mapped(self):
        return self.__virtual_pages_mapped

    def get_page_table_hits(self):
        return self.__page_table_hits

    def get_pages_from_free(self):
        return self.__pages_from_free

    def get_total_page_faults(self):
        return self.__total_page_faults

    def get_used_page_table_entries(self):
        return len(self.__virtual_memory_table)
    
    def get_used_page_table_entries_percentage(self):
        return (self.get_used_page_table_entries() /  self.__parameters.get_pte_entries_per_process()) * 100 if  self.__parameters.get_pte_entries_per_process() > 0 else 0

    def get_page_table_wasted_bytes(self):
        return ( self.__parameters.get_pte_entries_per_process() - self.get_used_page_table_entries()) * self.__parameters.get_page_table_entry_bits() //8