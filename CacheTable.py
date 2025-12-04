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

    def round_robin_replace(self, index, tag):
        victim_way = self.rr_ptr[index]
        self.rr_ptr[index] = (victim_way + 1) % self.__parameters.get_associativity()
        victim = self.__cache_table[index][victim_way]
        victim.set_valid()
        victim.set_tag(tag)

    def random_replace(self, index, tag):
        victim =  random.choice(self.__cache_table[index]) 
        victim.set_valid()
        victim.set_tag(tag)

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
            else:
                self.__misses += 1
                self.__cycles += 4 * self.__parameters.get_block_size_bytes() / 4
                
                if self.is_conflict_miss(index, tag):
                    self.__conflict += 1
                else:
                    self.__compulsory += 1

                # Replacement policy
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

    # --- CARLOS: Helper method for Unused Blocks ---
    def get_unused_blocks_count(self):
        """Counts the number of blocks in the cache that are NOT valid."""
        unused_count = 0
        for index in self.__cache_table:
            for way in self.__cache_table[index]:
                if not way.is_valid():
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