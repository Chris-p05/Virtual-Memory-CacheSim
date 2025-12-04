import random
from CacheBlock import CacheBlock
from Instruction import Instruction

# Maryna Korolova Part starts here >:) 

class CacheTable:
    def __init__(self, parameters):
        self.__parameters = parameters

        self.__cache_table = {
            i: [CacheBlock() for _ in range(self.__parameters.get_associativity())]
            for i in range(self.__parameters.get_total_rows())
        }

        self.rr_ptr = [0] * self.__parameters.get_total_rows()
        self.__seen_blocks = set()

        #statistics
        self.__addresses_accesses = 0
        self.__total_accesses = 0
        self.__hits = 0
        self.__misses = 0
        self.__compulsory = 0
        self.__conflict = 0

        self.__instruction_bytes = 0
        self.__SrcDst_bytes = 0
        self.__cycles = 0

    def is_hit(self, index, tag):
        for block in self.__cache_table[index]:
            if block.get_tag() == tag and block.is_valid():
                return True
        return False

    def is_conflict_miss(self, index, tag):
        return all(block.is_valid() for block in self.__cache_table[index]) and tag not in [block.get_tag() for block in self.__cache_table[index]]

    def is_compulsory_miss(self, block):
        return block not in self.__seen_blocks

    def round_robin_replace(self, index, tag):
        victim_way = self.rr_ptr[index]
        self.rr_ptr[index] = (victim_way + 1) % self.__parameters.get_associativity()
        victim = self.__cache_table[index][victim_way]
        victim.set_valid()
        victim.set_tag(tag)

    def random_replace(self, index, tag):
        victim_way = random.randrange(self.__parameters.get_associativity())
        victim = self.__cache_table[index][victim_way]
        victim.set_valid()
        victim.set_tag(tag)

    def find_empty_way_index(self, index):
        for way, block in enumerate(self.__cache_table[index]):
            if not block.is_valid():
                return way
        return None

    def insert_into_way(self, index, tag, way):
        block = self.__cache_table[index][way]
        block.set_tag(tag)
        block.set_valid()

    def invalidate_physical_page(self, physical_page_number):

        print("Address to invalidate:  ", f"0x{physical_page_number:X}", f"| {physical_page_number:016b}")
        page_size = self.__parameters.get_page_size()
        start_address = physical_page_number * page_size
        end_address = start_address + page_size - 1

        for block_address in range(start_address, end_address + 1, self.__parameters.get_block_size_bytes()):

            offset_size = self.__parameters.get_offset_size_bits()
            index_size = self.__parameters.get_index_size_bits()
            index =  (block_address >> offset_size) & ((1 << index_size) - 1)
            tag   = block_address >> ( offset_size + index_size)

            for block in self.__cache_table[index]:
                if block.is_valid() and block.get_tag() == tag:
                    block.reset_valid()

    def access_cache(self, instruction: Instruction):
        self.__addresses_accesses += 1

        if instruction.get_instruction_type() == "instruction":
            self.__instruction_bytes += instruction.get_instruction_length()
            self.__cycles += 2
        else:
            self.__SrcDst_bytes += instruction.get_instruction_length()
            self.__cycles += 1

        start_address = instruction.get_physical_address()
        length = instruction.get_instruction_length() #in bytes 
        end_address = start_address + length - 1

        start_block = start_address // self.__parameters.get_block_size_bytes() #in bytes 
        end_block = end_address // self.__parameters.get_block_size_bytes() #in bytes 

        for block in range(start_block, end_block + 1):

            block_address = block * self.__parameters.get_block_size_bytes() #in bytes 
            index = instruction.find_index(block_address)
            tag = instruction.find_tag(block_address)

            self.__total_accesses += 1

            if self.is_hit(index, tag):
                self.__hits += 1
                self.__cycles += 1
                continue 

            self.__misses += 1
            self.__cycles += 4 * self.__parameters.get_block_size_bytes() / 4

            if self.is_compulsory_miss(block):
                
                self.__seen_blocks.add(block)

            if self.is_conflict_miss(index, tag):
                self.__conflict += 1
            else:
                self.__compulsory += 1

            way = self.find_empty_way_index(index)
            if way is not None:
                self.insert_into_way(index, tag, way)
            else:
                if self.__parameters.get_replacement_policy() == "rr":
                    self.round_robin_replace(index, tag)
                    
                else:
                    self.random_replace(index, tag)
    
    def get_total_accesses(self):
        return self.__total_accesses

    def get_instruction_bytes(self):
        return self.__instruction_bytes

    def get_SrcDst_bytes(self):
        return self.__SrcDst_bytes

    def get_hits(self):
        return self.__hits

    def get_misses(self):
        return self.__misses

    def get_compulsory(self):
        return self.__compulsory

    def get_conflict(self):
        return self.__conflict
        
    def get_addresses_accesses(self):
        return self.__addresses_accesses

    def get_hit_rate(self):
        return (self.__hits / self.__total_accesses * 100) if self.__total_accesses > 0 else 0
    
    def get_miss_rate(self):
        return (self.__misses / self.__total_accesses * 100) if self.__total_accesses > 0 else 0

    # Carlos Part
    def get_unused_blocks_count(self):
        unused_count = 0
        for index in self.__cache_table:
            for block in self.__cache_table[index]:
                if not block.is_valid() and block.get_tag() is None:
                    unused_count += 1
        return unused_count

    def get_unused_kb(self):
        return (self.get_unused_blocks_count() * (self.__parameters.get_block_size_bytes() + (self.__parameters.get_overhead_bits_per_block() / 8))) / 1024

    def get_waste_percent(self):
        return (self.get_unused_kb() / self.__parameters.get_implementation_memory_kb() * 100) if self.__parameters.get_implementation_memory_kb() > 0 else 0

    def get_waste_cost(self):
        return (self.get_waste_percent() / 100) * self.__parameters.get_cost()

    def get_total_cycles(self):
        return self.__cycles

