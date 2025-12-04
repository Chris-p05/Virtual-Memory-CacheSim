from Simulation import Simulation

# Christopher Peters and Maryna Korolova and Carlos Part starts here >:) 

def main():
        sim = Simulation ()
        sim.start()
        
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
                config_str += sim.get_program_output_m1()
        
        if milestone_number == '2':
                print(f"Running Simulation Milestone 2 for Simulation {simulation_number}...")
                sim.get_program_output_m1()
                config_str += sim.get_program_output_m2()
        if milestone_number == '3':
                print(f"Running Simulation Milestone 3 for Simulation {simulation_number}...")
                sim.get_program_output_m1()
                sim.get_program_output_m2()
                config_str += sim.get_program_output_m3()

        with open(f"sim/Team_07_Sim_{simulation_number}_M#{milestone_number}.txt", "w") as file:
                file.write(config_str)

if __name__ == "__main__":
        main()