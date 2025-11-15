from CacheValuesCalculator import CacheValuesCalculator

class FreePhysicalMemoryPageTable:

    def __init__(self):
        self.cache_values_calculator = CacheValuesCalculator()
        self.page_size = 4096
        self.total_pages =  262144  # total physical pages
        self.system_pages_count = 196608 # system reserved pages

        # all physical pages free except OS-reserved
        self.free_pages = set(range(self.system_pages_count, self.total_pages))

    def allocate_page(self):
        """Return a free physical page or None if no free pages left."""
        if not self.free_pages:
            return None
        return self.free_pages.pop()

    def free_page(self, page_number):
        """Add page back to free set."""
        self.free_pages.add(page_number)

    def get_free_page_count(self):
        return len(self.free_pages)
    
        #Carlos Martinez part starts here >:)
    def get_num_physical_pages(self):
        physical_memory_bytes = self.cache_values_calculator.get_physical_memory_bytes() * 1024 * 1024
        return physical_memory_bytes // self.cache_values_calculator.get_page_size()
    
    def get_num_system_pages(self):
        return int(self.cache_values_calculator.get_physical_memory_os_usage() / 100.0 * self.get_num_physical_pages())
    
    def get_pages_available_to_user(self):
        return self.get_num_physical_pages() - self.get_num_system_pages()
    # Carlos Martinez part ends here >:)
