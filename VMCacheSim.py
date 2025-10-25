from linecache import cache
from CacheValuesCalculator import CacheValuesCalculator

def simulation_milestone_1():
        cache_values_calculator = CacheValuesCalculator()
        cache_values_calculator.load()
        config_str = cache_values_calculator.get_program_output()
        print("Enter the simulation number: ")
        simulation_number = input()
        with open(f"Team_07_Sim_{simulation_number}_M#1.txt", "w") as file:
                file.write(config_str)

def main():
        simulation_milestone_1()

if __name__ == "__main__":
        main()