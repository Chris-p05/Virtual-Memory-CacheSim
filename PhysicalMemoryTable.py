# Carlos Part
class PhysicalMemoryTable:

    def __init__(self, parameters):
        self.__parameters = parameters
        self.__free_pages = set(range(self.__parameters.get_physical_system_page_number(), self.__parameters.get_physical_page_number()))
        self.__owner = {page: None for page in self.__free_pages} # physical_page -> virtual_page (or None)

    def get_free_page(self):
        if not self.__free_pages:
            return None
        return self.__free_pages.pop()

    def add_free_page(self, page_number):
        self.__free_pages.add(page_number)
        self.__owner[page_number] = None

    def get_free_page_count(self):
        return len(self.__free_pages)
    
    def assign_page(self, physical_page, virtual_page):
        self.__owner[physical_page] = virtual_page

    def get_owner(self, physical_page):
        return self.__owner.get(physical_page)

    def get_allocated_pages(self):
        return [physical_page for physical_page, virtual_page in self.__owner.items() if virtual_page is not None]

    def reset_memory(self):
        self.__free_pages = set(range(self.__parameters.get_physical_system_page_number(), self.__parameters.get_physical_page_number()))
        self.__owner = {page: None for page in self.__free_pages}