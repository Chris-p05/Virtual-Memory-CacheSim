import argparse
import math

#Christopher's part
def main():

    parser = argparse.ArgumentParser(description = 'VM Cache Simulator >:)')

    parser.add_argument('-s', '--cache-size', type = int,required = True)

    parser.add_argument('-b','--block-size', type = int, required= True)

    parser.add_argument('-a','--associativty', type = int, required = True)


    print(f"*****Cache Calculated Values*****")
    print(f"Total # Blocks: ")
    print(f"Tag Size: ")
    print(f"Index Size:")
    print(f"Total # Rows")
    print(f"Cost: ")
    print()

if __name__ == '__main__':
    main()