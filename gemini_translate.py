import re
from parse_latest_date import parse_latest_date
# python 


def main():
    flag, input_file, output_file = parse_latest_date()
    print (f"flag: {flag}")
    print (f"input_file: {input_file}")
    print (f"output_file: {output_file}")
    if flag == False: 
        return 
    



if __name__ == "__main__":
    main()