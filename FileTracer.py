import re

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

                    if dst_addr != "00000000" and dst_data != "--------":
                        self.data.append((int(dst_addr, 16), 4)) 

                src_match = re.search(r"srcM:\s*([0-9a-fA-F]+)\s+([0-9A-F\-]+)", line)
                if src_match:
                    src_addr = src_match.group(1)
                    src_data = src_match.group(2)
                    if src_addr != "00000000" and src_data != "--------":
                        self.data.append((int(src_addr, 16), 4)) 

        return self.data
