
#Carlos Mejia Rosales part starts here >:)
class PhysicalMemoryTable:

    def __init__(self, parameters):
        self.__parameters = parameters
        # all physical pages free except OS-reserved
        self.__free_pages = set(range(self.__parameters.get_physical_system_page_number(), self.__parameters.get_physical_page_number()))

    def get_free_page(self):
        if not self.__free_pages:
            return None
        return self.__free_pages.pop()

    def add_free_page(self, page_number):
        self.__free_pages.add(page_number)

    def get_free_page_count(self):
        return len(self.__free_pages)
    

