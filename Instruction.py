class Instruction:

    def __init__(self, virtual_address, instruction_length, instruction_type, parameters):
        self.__virtual_address = virtual_address
        self.__virtual_page_number = None
        self.__physical_address = None
        self.__physical_page_number = None
        self.__tag = None
        self.__index = None
        self.__offset = None
        self.__instruction_length = instruction_length
        self.__instruction_type = instruction_type
        self.__parameters: SimulationParameters = parameters


    def get_virtual_address(self): return self.__virtual_address
    def get_instruction_length(self): return self.__instruction_length
    def get_instruction_type(self): return self.__instruction_type

    def get_physical_page_number(self): return self.__physical_page_number
    def set_physical_page_number(self, physical_page_number): self.__physical_page_number = physical_page_number

    def get_virtual_pages_number(self): 
        if self.__virtual_page_number is None:
            self.__virtual_page_number = self.address_to_page_number(self.__virtual_address)
        return self.__virtual_page_number
        
    def get_physical_address(self):
        if self.__physical_address is None:
             self.__physical_address = self.page_number_to_address(self.__physical_page_number, self.get_offset())
        return self.__physical_address

    def get_tag(self): 
        if self.__tag is None:
            self.__tag = self.find_tag(self.get_physical_address())
        return self.__tag
           
    def get_index(self): 
        if self.__index is None:
            self.__index = self.find_index(self.get_physical_address())
        return self.__index

    def get_offset(self): 
        if self.__offset is None:
            self.__offset = self.find_offset( self.__virtual_address)
        return self.__offset

    def address_to_page_number(self, address):
        return address // self.__parameters.get_page_size()
    
    def page_number_to_address(self, page_number, offset):
        return page_number * self.__parameters.get_page_size() + offset

    def find_offset(self, address):
        offset_size = self.__parameters.get_offset_size_bits()
        return address & ((1 << offset_size) - 1)

    def find_index(self, address):
        offset_size = self.__parameters.get_offset_size_bits()
        index_size = self.__parameters.get_index_size_bits()
        return (address >> offset_size) & ((1 << index_size) - 1)

    def find_tag(self, address):
        offset_size = self.__parameters.get_offset_size_bits()
        index_size = self.__parameters.get_index_size_bits()
        return address >> ( offset_size + index_size)

