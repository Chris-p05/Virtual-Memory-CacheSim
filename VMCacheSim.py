from FileTracer import FileTracer
from VirtualMemory import VirtualMemory


def main():
        print("\nCache Simulator - CS 3853 - Team #7\n")
        tracer = FileTracer()
        tracer.load()
        tracer.print_config()        

        tracer.print_config() 
        tracer.print_cache_calculated_values()      
        tracer.print_physical_memory_calculations()


        tracer.print_config() 
        tracer.print_cache_calculated_values()   
        tracer.print_physical_memory_calculations()

        #milestone 2  

        print("\nMILESTONE #2: -Virtual Memory Simulation Results")

        vm = VirtualMemory(
                physical_memory_mb=tracer.get_physical_memory(),
                percent_system=tracer.get_physical_memory_os_usage(),
                trace_files=tracer.get_trace_file()
    )

        vm.process_trace_files()
        vm.print_virtual_memory_results(tracer.get_page_table_entry_bits())
if __name__ == "__main__":
        main()