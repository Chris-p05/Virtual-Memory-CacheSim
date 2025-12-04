import math
from SimulationParameters import SimulationParameters
from PhysicalMemoryTable import PhysicalMemoryTable
from CacheTable import CacheTable

# Christopher Peters and Maryna Korolova Part starts here >:) 

class VirtualMemoryTable:
    def __init__(self, physical_memory:PhysicalMemoryTable, cache_table:CacheTable, parameters:SimulationParameters):
        self.__parameters = parameters
        self.__physical_memory_table = physical_memory
        self.__cache_table = cache_table

        # virtual_page -> physical_page mapping
        self.__victim_ptr = 0
        self.__virtual_memory_table = {}
        self.__used_page_table_entries = set()

        # statistics
        self.__virtual_pages_mapped = 0
        self.__page_table_hits = 0
        self.__pages_from_free = 0
        self.__total_page_faults = 0


    def get_physical_page(self, virtual_page):
        return self.__virtual_memory_table.get(virtual_page)

    def is_mapped(self, virtual_page):
        return virtual_page in self.__virtual_memory_table

    def map_virtual_to_physical(self, virtual_page, physical_page):
        self.__used_page_table_entries.add(virtual_page)
        self.__virtual_memory_table[virtual_page] = physical_page
        self.__physical_memory_table.assign_page(physical_page, virtual_page)

    def choose_victim_page(self):
        allocated = self.__physical_memory_table.get_allocated_pages()
        victim = allocated[self.__victim_ptr % len(allocated)]
        self.__victim_ptr += 1
        return victim

    def allocate_physical_page(self, instruction):
        virtual_page = instruction.get_virtual_pages_number()
        self.__virtual_pages_mapped += 1

        if self.is_mapped(virtual_page):
            self.__page_table_hits += 1
            physical_page = self.get_physical_page(virtual_page)
            instruction.set_physical_page_number(physical_page)
            return

        free_physical_page = self.__physical_memory_table.get_free_page()
        if free_physical_page is not None:
            self.__pages_from_free += 1
            self.map_virtual_to_physical(virtual_page, free_physical_page)
            instruction.set_physical_page_number(free_physical_page)
            return


        self.__total_page_faults += 1
        victim_physical_page = self.choose_victim_page()
        victim_virtual_page = self.__physical_memory_table.get_owner(victim_physical_page)

        # Unmap victim virtual page
        if victim_virtual_page in self.__virtual_memory_table:
            del self.__virtual_memory_table[victim_virtual_page]

        # Invalidate cache entries belonging to this physical page

        self.__cache_table.invalidate_physical_page(victim_physical_page)

        # Reuse the victim page
        self.map_virtual_to_physical(virtual_page, victim_physical_page)
        instruction.set_physical_page_number(victim_physical_page)

    def get_virtual_pages_mapped(self):
        return self.__virtual_pages_mapped

    def get_page_table_hits(self):
        return self.__page_table_hits

    def get_pages_from_free(self):
        return self.__pages_from_free

    def get_total_page_faults(self):
        return self.__total_page_faults

    def get_used_page_table_entries(self):
        return len(self.__used_page_table_entries)
    
    def get_used_page_table_entries_percentage(self):
        return (self.get_used_page_table_entries() /  self.__parameters.get_pte_entries_per_process()) * 100 if  self.__parameters.get_pte_entries_per_process() > 0 else 0

    def get_page_table_wasted_bytes(self):
        return ( self.__parameters.get_pte_entries_per_process() - self.get_used_page_table_entries()) * self.__parameters.get_page_table_entry_bits() //8
