"""
Example of command line parsing. Accept the simple options of 
    -a  - sort the input lines in ascending order
    -d  - sort the input lines in descending order

To implement the following command

    python3 cl2 [-a|-d] file.txt

This is mainly to illustrate why you want a command line parser
to do most of the work for you.
"""
import sys

# default value of sort option and file to be sorted
order = "a"
infile = sys.stdin
filename = ""

# Note: there is a bug here, what if you give the option ""
for t in sys.argv:
    if t == '-a':
        order = "a"
    elif t == '-d':
        order = "d"
    elif t[0] == '-':
        print("Unknown option:", t)
    else:
        filename = t

# Open the file if it was provided on the command line
# Bug: what if the file does not exist>

infile=open(filename, "r" )

# fetch all the lines, preserving the '\n'
lines = infile.readlines()

# sort them in the order specified by the -a or -d option
descending = (order == "d")
sorted_lines = sorted(lines, reverse=descending)

# Print them out, getting rid of trailing whitespace and "\n"
for l in sorted_lines:
    l.rstrip()
    print(l)
