import re

# Maryna Korolova part starts here :)
class FileTracer:

    def __init__(self):
        self.data = []

    def parse_trace_file(self, filename):
        try:

            with open(filename, "r") as file:
                lines = file.readlines()
            for line in lines:
                line = line.strip()
                self.parse_trace_line(line)
            return self.data
        
        except FileNotFoundError:
            
            print(f"Warning: Trace file '{filename}' not found!")
            return []

    def parse_trace_line(self, line):

        if line.startswith("EIP"):

            match = re.search(r"EIP \((\d+)\): ([0-9a-fA-F]+)", line)
            if match:
                length = int(match.group(1))     
                addr = int(match.group(2), 16)   
                self.data.append((addr, length, 'instruction'))    

        elif line.startswith("dstM"):

            dst_match = re.search(r"dstM:\s*([0-9a-fA-F]+)\s+([0-9A-F\-]+)", line)
            if dst_match:
                dst_addr = int(dst_match.group(1), 16)
                dst_data = dst_match.group(2)

                if dst_addr != 0 and dst_data != "--------":
                    self.data.append((dst_addr, 4, 'data')) 

            src_match = re.search(r"srcM:\s*([0-9a-fA-F]+)\s+([0-9A-F\-]+)", line)
            if src_match:
                src_addr = int(src_match.group(1), 16)
                src_data = src_match.group(2)
                if src_addr != 0 and src_data != "--------":
                    self.data.append((src_addr, 4, 'data'))

