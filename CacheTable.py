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

    def is_hit(self, index, tag):
        return any(block.get_tag() == tag and block.is_valid() for block in self.__cache_table[index])

    def is_compulsory_miss(self, index, tag):
        return all(not block.is_valid() for block in self.__cache_table[index]) 

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
        else:
            self.__SrcDst_bytes += instruction.get_instruction_length()

        start_address = instruction.get_physical_address()
        length = instruction.get_instruction_length() #in bytes 
        end_address = start_address + length - 1

        block_size = self.__parameters.get_block_size_bytes() #in bytes 
        tag = instruction.get_tag()
        index = instruction.get_index()
        offset = instruction.get_offset()


        start_block = start_address // block_size
        end_block = end_address // block_size
        blocks_accessed = end_block - start_block + 1

        # print("Instruction param (binary):")
        # print(f"start_addr  {start_address:032b}")
        # print(f"tag         {tag:0{tag.bit_length()}b}")
        # print(f"index       {index:0{index.bit_length()}b}")
        # print(f"offset      {offset:0{offset.bit_length()}b}")
        # print("block_size ", block_size)
        # print("start_block ", start_block)
        # print("end_block ", end_block)
        # print(f"length      {length}")
        # print(f"end_addr    {end_address:032b}")
        # print(f"access_block_number  {blocks_accessed}")
      

        for block in range(start_block, end_block + 1):

            block_address = block * block_size
            index = instruction.find_index(block_address)
            tag = instruction.find_tag(block_address)

            # print(f"block_address  {block_address:032b}")
            # print(f"tag         {tag:0{tag.bit_length()}b}")
            # print(f"index       {index:0{index.bit_length()}b}")

            self.__total_accesses += 1
            if self.is_hit(index, tag):
                self.__hits += 1
            else:
                self.__misses += 1
                if self.is_compulsory_miss(index, tag): self.__compulsory += 1
                if self.is_conflict_miss(index, tag): self.__conflict += 1
                # Replacement policy
                if self.__parameters.get_replacement_policy() == "rr":
                    self.round_robin_replace(index, tag)
                else:
                    self.random_replace(index, tag)

            # print("Hit: ",  self.__hits)
            # print("Miss: ", self.__misses)

        #print()


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


