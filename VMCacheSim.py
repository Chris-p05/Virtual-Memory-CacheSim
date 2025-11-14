from FileTracer import FileTracer
from VirtualMemory import VirtualMemory
from linecache import cache
from CacheValuesCalculator import CacheValuesCalculator

def simulation_milestone_1():
        cache_values_calculator = CacheValuesCalculator()
        cache_values_calculator.load()
        config_str = cache_values_calculator.get_program_output()
        print("Enter the simulation number: ")
        simulation_number = input()
        with open(f"./sim/Team_07_Sim_{simulation_number}_M#1.txt", "w") as file:
                file.write(config_str)

        print("MILESTONE #2: -Virtual Memory Simulation Results")

        vm = VirtualMemory(
                physical_memory_mb=cache_values_calculator.get_physical_memory(),
                percent_system=cache_values_calculator.get_physical_memory_os_usage(),
                trace_files=cache_values_calculator.get_trace_file()
        )

        vm.process_trace_files()
        vm.print_virtual_memory_results()#cache_values_calculator.get_page_table_entry_bits())

def main():
        simulation_milestone_1()

if __name__ == "__main__":
        main()