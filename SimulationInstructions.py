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

    