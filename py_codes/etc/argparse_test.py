#Using argparse library to handle all the parsing of complicated strings of command-line arguments
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n")
args = parser.parse_args()

for _ in range(int(args.n)):
    print("Tech")


# Using sys library and command-line arguements to print out tech a specified number(n) amount of times
"""
import sys

if len(sys.argv) == 1:
    print("Tech")
elif len(sys.argv) == 3 and sys.argv[1] == "-n":
    n = int(sys.argv[2])
    for _ in range(n):
        print("Tech")
else:
    print("usage: argparse.py [-n NUMBER]")
"""
