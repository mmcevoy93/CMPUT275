"""
Example of command line parsing using argparse

See
https://docs.python.org/3/howto/argparse.html
and
https://docs.python.org/3/library/argparse.html#module-argparse

"""
import sys
import argparse

# This parameter
#   formatter_class=argparse.RawTextHelpFormatter,
# is needed for long option descriptions

parser = argparse.ArgumentParser(
    description='Sort a text file.',
    formatter_class=argparse.RawTextHelpFormatter,
    )

# Note: for optional arguments, you should always use the "dest="
# parameter to define the name of the variable to set. This is because
# the names of optional parameters often change while you are developing
# the program.

parser.add_argument("-d", "--descending",
    help="sort in descending order, default is ascending",
    action="store_true",
    dest="sort_descending")

parser.add_argument("-w", "--words",
    help="break lines into individual words",
    action="store_true",
    dest="break_into_words")

# Dummy param to illustrate key value options
parser.add_argument("--dummy",
    help="""\
Unused option:
one - do something weird
two - (default) do something strange
""",
    nargs='?',
    choices=['one', 'two'],
    default='two',
    dest="dummy")


# This describes the optional position argument that, if present
# is the name of a file to process, and if missing sets the input
# to stdin.

parser.add_argument("infile",
    help="file to be sorted, stdin if omitted",
    nargs="?",
    type=argparse.FileType('r'),
    default=sys.stdin)

args = parser.parse_args()

# We don't get this far unless the arguments have been parsed,
# and infile opened if specified.

print("The dummy option is", args.dummy)

# list of things, lines or words, to sort
to_sort = []

# fetch all the lines
for line in args.infile:
    if args.break_into_words:
        # strip leading and trailing whitespace, split into tokens
        to_sort += line.strip().split()
    else:
        # just strip trailing whitespace
        to_sort.append(line.rstrip())

sorted_lines = sorted(to_sort, reverse=args.sort_descending)

# Print them out
for l in sorted_lines:
    print(l)
