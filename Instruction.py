class Instruction:
    def __init__(self, virtual_address, instruction_length, instruction_type):
        self.__virtual_address = virtual_address
        self.__physical_address = 0
        self.__instruction_length = instruction_length
        self.__instruction_type = instruction_type  

    def get_virtual_address(self):
        return self.__virtual_address

    def get_instruction_length(self):
        return self.__instruction_length

    def get_instruction_type(self):
        return self.__instruction_type

    def get_physical_address(self):
        return self.__physical_address
    
    def set_physical_address(self, physical_address):
        self.__physical_address = physical_address