import random
from CacheBlock import CacheBlock
from Instruction import Instruction

class CacheTable:
    def __init__(self, parameters):
        self.__parameters = parameters
        self.__cache_table = {
            i: [CacheBlock() for _ in range(self.__parameters.get_associativity())]
            for i in range(self.__parameters.get_total_rows())
        }

        self.rr_ptr = [0] * self.__parameters.get_total_rows()

        #statistics
        self.__total_accesses = 0
        self.__hits = 0
        self.__misses = 0
        self.__compulsory = 0
        self.__conflict = 0

        self.__instruction_bytes = 0
        self.__SrcDst_bytes = 0


    def is_hit(self, index, tag):

        for block in self.__cache_table[index]:
            if block.get_tag() == tag and block.is_valid():
                return True
        return False

    def is_compulsory_miss(self, index):
        for way in self.__cache_table[index]:
            if not way.is_valid():
                return True
        return False
    
    def is_conflict_miss(self, index, tag):
        if self.is_hit(index, tag):
            return False
        return all(way.is_valid() for way in self.__cache_table[index])


    def round_robin_replace(self, index, tag):
        victim_way = self.rr_ptr[index]
        self.rr_ptr[index] = (victim_way + 1) % self.__parameters.get_associativity()
        victim = self.__cache_table[index][victim_way]
        victim.set_valid(True)
        victim.set_tag(tag)

    def random_replace(self, index, tag):
        victim =  random.choice(self.__cache_table[index]) 
        victim.set_valid(True)
        victim.set_tag(tag)
        print(victim)



    def get_offset(self, address):
        offset_size = self.__parameters.get_offset_size_bits()
        return address & ((1 << offset_size) - 1)

    def get_index(self, address):
        offset_size = self.__parameters.get_offset_size_bits()
        index_size = self.__parameters.get_index_size_bits()
        return (address >> offset_size) & ((1 << index_size) - 1)

    def get_tag(self, address):
        offset_size = self.__parameters.get_offset_size_bits()
        index_size = self.__parameters.get_index_size_bits()
        return address >> ( offset_size + index_size)


    def access_cache(self, instruction:Instruction):

        self.__total_accesses += 1

        if instruction.get_instruction_type() == "instruction":
            self.__instruction_bytes += instruction.get_instruction_length()
        if instruction.get_instruction_type() == "data":
            self.__SrcDst_bytes += instruction.get_instruction_length()
       
        index = self.get_index(instruction.get_physical_address())
        tag = self.get_tag(instruction.get_physical_address())

        if self.is_hit(index, tag):
            self.__hits += 1
            return

        self.__misses += 1

        if self.is_compulsory_miss(index):
            self.__compulsory += 1

        if self.is_conflict_miss(index, tag):
            self.__conflict += 1

        if self.__parameters.get_replacement_policy() == "rr":
            self.round_robin_replace(index, tag)
        elif self.__parameters.get_replacement_policy() == "r":
            self.random_replace(index, tag)

    def get_total_accesses(self):
        return self.__total_accesses

    def get_instruction_bytes(self):
        return self.__instruction_bytes

    def get_SrcDst_bytes(self):
        return self.__SrcDst_bytes

    def get_total_accesses(self):
        return self.__total_accesses

    def get_hits(self):
        return self.__hits

    def get_misses(self):
        return self.__misses

    def get_compulsory(self):
        return self.__compulsory

    def get_conflict(self):
        return self.__conflict

    # --- CARLOS: Helper method for Unused Blocks ---
    def get_unused_blocks_count(self):
        """Counts the number of blocks in the cache that are NOT valid."""
        unused_count = 0
        for index in self.__cache_table:
            for way in self.__cache_table[index]:
                if not way.is_valid():
                    unused_count += 1
        return unused_count

