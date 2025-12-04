# Maryna Korolova Part starts here >:) 
class SimulationInstructionsBuilder:
    def __init__(self):
        self.instructions: dict[str, List[Instruction]] = {}

    def build(self):
        return SimulationInstructions(self)

    def set_instructions(self, instructions):
        self.instructions = instructions
        return self

class SimulationInstructions:

    def __init__ (self, builder:SimulationInstructionsBuilder):
        self.__instructions: dict[str, List[Instruction]] = builder.instructions

    def get_instructions(self):
        return self.__instructions

    def get_total_instructions_count(self):
        total_instructions_count = 0
        for filename, instructions in  self.__instructions.items():
            for instruction in instructions:
                if instruction.get_instruction_type() == "instruction":
                    total_instructions_count += 1
        return total_instructions_count

    