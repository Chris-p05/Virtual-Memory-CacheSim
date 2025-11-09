import argparse
import math

class FileTracer:

    def __init__(self):
        self.data = []

    def parse_trace_file(self, filename):

        with open(filename, "r") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()

            if line.startswith("EIP"):

                match = re.search(r"EIP \((\d+)\): ([0-9a-fA-F]+)", line)
                if match:
                    length = int(match.group(1))     
                    addr = int(match.group(2), 16)   
                    self.data.append((addr, length))    

            elif line.startswith("dstM"):

                dst_match = re.search(r"dstM:\s*([0-9a-fA-F]+)\s+([0-9A-F\-]+)", line)
                if dst_match:
                    dst_addr = dst_match.group(1)
                    dst_data = dst_match.group(2)

        return self
    
    def print_config(self):
        print(f"Trace File:")
        for file in self.get_trace_file():
            print(f"\t{file}")
        print()
        print(f"***** Cache Input Parameters *****")
        print("{:<28}".format("Cache Size: ") + str(self.get_cache_size()) + " KB")
        print("{:<28}".format("Block Size: ") + str(self.get_block_size()) + " bytes")
        print("{:<28}".format("Associativity: ") + str(self.get_associativity()))
        print("{:<28}".format("Replacement Policy: ") + ("Round Robin" if self.get_replacement_policy() == 'rr' else "Random"))
        print("{:<28}".format("Physical Memory Size: ") + str(self.get_physical_memory()) + " MB")
        print("{:<28}".format("Physical Memory OS Usage: ") + str(self.get_physical_memory_os_usage()) + "%")
        print("{:<28}".format("Number of Instructions: ") + str(self.get_instructions()))

        src_match = re.search(r"srcM:\s*([0-9a-fA-F]+)\s+([0-9A-F\-]+)", line)
        if src_match:
                    src_addr = src_match.group(1)
                    src_data = src_match.group(2)
                    if src_addr != "00000000" and src_data != "--------":
                        self.data.append((int(src_addr, 16), 4)) 

    def get_cache_size(self):
        return self.__cache_size
        
    def get_block_size(self):
        return self.__block_size
    
    def get_associativity(self):
        return self.__associativity
    
    def get_replacement_policy(self):
        return self.__replacement_policy
    
    def get_physical_memory(self):
        return self.__physical_memory
    
    def get_physical_memory_os_usage(self):
        return self.__physical_memory_os_usage
    
    def get_instructions(self):
        return self.__instructions
    
    def get_trace_file(self):
        return self.__trace_file
    
    def get_virtual_address_space(self):
        return self.__virtual_address_space
    
    def get_page_table_entry_bits(self):
        """Size of page table entry (1 valid bit + physical page bits)"""
        PAGE_SIZE_KB = 4
        total_memory_kb = self.get_physical_memory() * 1024
        num_physical_pages = total_memory_kb // PAGE_SIZE_KB
        PPN_BITS = int(math.log2(num_physical_pages))
        return 1 + PPN_BITS 
    
    #Christopher Peters Part starts here >:) 

  # ---------- Cache Calculated Values ----------
    
    def get_cache_size_bytes(self):
        return self.get_cache_size() * 1024
    
    def get_total_blocks(self):
        return self.get_cache_size_bytes() // self.get_block_size()
    
    def get_total_rows(self):
        return self.get_total_blocks() // self.get_associativity()
    
    def get_index_size(self):
        return int(math.log2(self.get_total_rows()))
    
    def get_offset_size(self):
        return int(math.log2(self.get_block_size()))
    
    def get_physical_memory_bytes(self):
        return self.get_physical_memory() * 1024 * 1024
    
    def get_total_address_bits(self):
        return int(math.log2(self.get_physical_memory_bytes()))
    
    def get_tag_size(self):
        return self.get_total_address_bits() - self.get_index_size() - self.get_offset_size()
    
    def get_overhead_bits_per_block(self):
        return 1 + self.get_tag_size()
    
    def get_total_overhead_bits(self):
        return self.get_overhead_bits_per_block() * self.get_total_blocks()
    
    def get_overhead_bytes(self):
        return math.ceil(self.get_total_overhead_bits() / 8)
    
    def get_implementation_memory_bytes(self):
        return self.get_cache_size_bytes() + self.get_overhead_bytes()
    
    def get_implementation_memory_kb(self):
        return self.get_implementation_memory_bytes() / 1024
    
    def get_cost(self):
        return self.get_implementation_memory_kb() * 0.07
    
    # --------------- Print menu for Cache Calculated Values -----------------
    
    def print_cache_calculated_values(self):
        """Print the Cache Calculated Values section"""
        print("***** Cache Calculated Values *****")
        print(f"Total # Blocks:                  {self.get_total_blocks()}")
        print(f"Tag Size:                        {self.get_tag_size()} bits")
        print(f"Index Size:                      {self.get_index_size()} bits")
        print(f"Total # Rows:                    {self.get_total_rows()}")
        print(f"Overhead Size:                   {self.get_overhead_bytes()} bytes")
        print(f"Implementation Memory Size:      {self.get_implementation_memory_kb():.2f} KB ({self.get_implementation_memory_bytes()} bytes)")
        print(f"Cost:                            ${self.get_cost():.2f} @ $0.07 per KB")
        print()


    #Carlos Mejia Rosales Part starts here 🙁

            #Carlos Mejia Rosales Part starts here :(


  # ---------- Physical Memory Calculated Values ----------

    def print_physical_memory_calculations(self):
        """Calculates and prints the Physical Memory Calculated Values section."""
        PAGE_SIZE_KB = 4
        """Calculates and prints the Physical Memory Calculated Values section."""
        PAGE_SIZE_KB = 4             
        PTE_ENTRIES_PER_PROCESS = 524288

        physical_memory_mb = self.get_physical_memory()
        system_percent = self.get_physical_memory_os_usage() / 100.0
        num_trace_files = len(self.get_trace_file())


        total_memory_kb = physical_memory_mb * 1024
        num_physical_pages = total_memory_kb // PAGE_SIZE_KB      
        total_memory_kb = physical_memory_mb * 1024
        num_physical_pages = total_memory_kb // PAGE_SIZE_KB
        
        num_pages_for_system = int(num_physical_pages * system_percent)

        PPN_BITS = 18 
        VALID_BIT = 1
        size_of_pte_bits = PPN_BITS + VALID_BIT

        total_bits = PTE_ENTRIES_PER_PROCESS * num_trace_files * size_of_pte_bits
        total_ram_bytes = total_bits // 8
 

        print("\n *****Physical Memory Calculated Values*****")
        print(f"\nNumber of Physical Pages: {num_physical_pages:>20}")
        print(f"Number of Pages for System: {num_pages_for_system:>18} ")
        print(f"Size of Page Table Entry: {size_of_pte_bits:>20} bits ")
        print(f"Total RAM for Page Table(s): {total_ram_bytes:>15} bytes")

        total_bits = PTE_ENTRIES_PER_PROCESS * num_trace_files * size_of_pte_bits
        total_ram_bytes = total_bits // 8

        #print outputs 

        print("\n***** Physical Memory Calculated Values *****")
        print(f"\nNumber of Physical Pages: {num_physical_pages:>20}")
        print(f"Number of Pages for System: {num_pages_for_system:>18}        ({system_percent:.2f} * {num_physical_pages} = {num_pages_for_system} )")
        print(f"Size of Page Table Entry: {size_of_pte_bits:>20} bits        (1 valid bit, {PPN_BITS} for PhysPage)")
        print(f"Total RAM for Page Table(s): {total_ram_bytes:>15} bytes        ({PTE_ENTRIES_PER_PROCESS // 1024}K entries * {num_trace_files} .trc files * {size_of_pte_bits} / 8)")
