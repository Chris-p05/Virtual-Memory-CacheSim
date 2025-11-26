from CacheValuesCalculator import CacheValuesCalculator

#Carlos Mejia Rosales part starts here >:)
class FreePhysicalMemoryPageTable:

    def __init__(self):
        self.cache_values_calculator = CacheValuesCalculator()
        # all physical pages free except OS-reserved
        self.free_pages = set(range(self.cache_values_calculator.get_number_system_pages(), self.cache_values_calculator.get_number_physical_pages()))

    def get_free_page(self):
        if not self.free_pages:
            return None
        return self.free_pages.pop()

    def add_free_page(self, page_number):
        self.free_pages.add(page_number)

    def get_free_page_count(self):
        return len(self.free_pages)
    

