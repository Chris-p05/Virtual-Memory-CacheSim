from FileTracer import FileTracer
from VirtualMemorySimulation import VirtualMemorySimulation
from linecache import cache
from CacheValuesCalculator import CacheValuesCalculator

def simulation_milestone_1():
        cache_values_calculator = CacheValuesCalculator()
        return cache_values_calculator.get_program_output()

def simulation_milestone_2():
        virtual_memory_simulation = VirtualMemorySimulation()
        return virtual_memory_simulation.get_program_output()


def main():
        print("Enter the simulation number: ")
        simulation_number = input()
        print("Enter the milestone number: ")
        milestone_number = input()

        config_str = ''

        if milestone_number not in ['1', '2', '3']:
                print("Invalid milestone number. Please enter 1, 2, or 3.")
                return
        if milestone_number == '1':
                print(f"Running Simulation Milestone 1 for Simulation {simulation_number}...")
                config_str += simulation_milestone_1()
        
        if milestone_number == '2':
                print(f"Running Simulation Milestone 2 for Simulation {simulation_number}...")
                config_str += simulation_milestone_1()
                config_str += simulation_milestone_2()
        if milestone_number == '3':
                print(f"Running Simulation Milestone 3 for Simulation {simulation_number}...")
                config_str += simulation_milestone_1()
                config_str += simulation_milestone_2()
                # Add the function call for milestone 3 here when implemented

        with open(f"./sim/Team_07_Sim_{simulation_number}_M#{milestone_number}.txt", "w") as file:
                file.write(config_str)

if __name__ == "__main__":
        main()