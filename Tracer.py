import argparse
import math
import re
from  Instruction import Instruction
from SimulationParameters import SimulationParametersBuilder 
from SimulationInstructions import  SimulationInstructionsBuilder

class Tracer:
    def __init__(self):
        self.parsed_arg = None

    def load(self):

        parser = argparse.ArgumentParser(description = 'VM Cache Simulator')

        parser.add_argument(
            '-s', 
            '--cache-size',
            type = int,
            choices = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096],
            required = True
        )
        parser.add_argument(
            '-b',
            '--block-size',
            type = int,
            choices = [8, 16, 32, 64],
            required= True
        )
        parser.add_argument(
            '-a',
            '--associativity',
            type = int,
            choices = [2, 4, 8, 16],
            required = True
        )
        parser.add_argument(
            '-r',
            '--replacement-policy',
            type = str,
            choices = ["r", "rr"],
            required = True
        )
        parser.add_argument(
            '-p',
            '--physical-memory',
            type = int,
            choices=[128, 256, 512, 1024, 2048, 4096],
            required = True
        )
        parser.add_argument(
            '-u',
            '--physical-memory-os-usage',
            type = int,
            choices=range(1, 101),
            required = True
        )
        parser.add_argument(
            '-n',
            '--instructions',
            type = int,
            required = True
        )
        parser.add_argument(
            '-f',
            '--trace-files',
            action='append',
            type=str,
            required=True,
            help='Specify 1-3 trace files'
        )

        if not (1 <= len(parser.parse_args().trace_files) <= 3):
            parser.error("argument -f/--trace-file: must be given between 1 and 3 times")

        self.parsed_arg = parser.parse_args()


    def parse_trace_line(self, line, data, parameters):



        if line.startswith("EIP"):

            match = re.search(r"EIP \((\d+)\): ([0-9a-fA-F]+)", line)
            if match:
                length = int(match.group(1))     
                address = int(match.group(2), 16)   
                data.append(Instruction(address, length, 'instruction', parameters))    

        elif line.startswith("dstM"):

            dst_match = re.search(r"dstM:\s*([0-9a-fA-F]+)\s+([0-9a-fA-F\-]+)", line)
            if dst_match:
                dst_addr = int(dst_match.group(1), 16)
                dst_data = dst_match.group(2)

                if dst_addr != 0 and dst_data != "--------":
                    data.append(Instruction(dst_addr, 4, 'data', parameters)) 

            src_match = re.search(r"srcM:\s*([0-9a-fA-F]+)\s+([0-9a-fA-F\-]+)", line)
            if src_match:
                src_addr = int(src_match.group(1), 16)
                src_data = src_match.group(2)
                if src_addr != 0 and src_data != "--------":
                    data.append( Instruction(src_addr, 4, 'data', parameters))

    def parse_trace_file(self, filenames):
        self.load()
        parameters = self.get_simulation_parameters()
        instructions: dict[str, List[Instruction]] = {}
        for filename in filenames:
            data = []
            try:
                with open(filename, "r") as file:
                    for line in file:
                        self.parse_trace_line(line.strip(), data, parameters)
                instructions[filename] = data
            except FileNotFoundError:
                print(f"Warning: Trace file '{filename}' not found!")
                return {}
        return instructions

    def get_simulation_parameters(self):
        self.load()
        return ( 
            SimulationParametersBuilder()
            .set_arg(self.parsed_arg)
            .build()
        )

    def get_simulation_instructions(self):
        self.load()
        return ( 
            SimulationInstructionsBuilder()
            .set_instructions(self.parse_trace_file(self.parsed_arg.trace_files))
            .build()
        )
