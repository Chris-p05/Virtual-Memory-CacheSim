from FileTracer import FileTracer


def main():
        print("\nCache Simulator - CS 3853 - Team #7\n")
        tracer = FileTracer()
        tracer.load()
        tracer.print_config()        

if __name__ == "__main__":
        main()