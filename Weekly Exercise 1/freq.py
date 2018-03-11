import sys
import argparse
import string

parser = argparse.ArgumentParser(
    description='Text frequency analysis',
    formatter_class=argparse.RawTextHelpFormatter,
    )

parser.add_argument("--sort",
    help="""\
byfreq - (default) sort by decreasing frequency.
         Matching frequency is resolved by word in
         increasing lexicographical order.
byword - sort by word in increasing lexicographical order
""",
    nargs='?',
    choices=['byfreq', 'byword'],
    default='byfreq',
    dest="sort")

parser.add_argument("-ignore-case", "--ignore-case", #sample output had both --ignore-case and -ignore-case examples
    help="ignore upper/lower case when doing all actions.",
    action="store_true",
    dest="ignore_case")

parser.add_argument("--remove-punct",
    help='''\
remove all punctuation characters in a word,
preserving only the alphanumeric characters
        ''',
    action="store_true",
    dest="remove_punct")

parser.add_argument("infile",
    help="file to be sorted, stdin if omitted",
    nargs="?",
    type=argparse.FileType('r'),
    default=sys.stdin)

args = parser.parse_args()

to_sort = {}
# fetch all the lines
for line in args.infile:
    line = line.replace("\n","") #on my machince carriage return was becoming an issue. Took out for all cases even though not considered puncutation with curses.ascii.ispunct("\r")
    if args.remove_punct:
        #Removes the punctuation of line
        for c in string.punctuation:
            line = line.replace(c,"")
    if args.ignore_case:
        line = line.lower()
    for word in line.split(" "):
        if word in to_sort:
            to_sort[word]+=1
        else:
            to_sort[word] = 1



if '' in to_sort:
    del to_sort[''] # some how got a blank in there. Just gonna delete in.


print('{:15}{:15}{}'.format("Word","Count","Frequency"))
print('{:15}{:15}{}'.format("____","_____","_________"))

sum_of_words = sum(to_sort.values())

if args.sort == 'byword':
    to_sort_list = sorted(to_sort, key=lambda sortit: sortit[0])
    for x in to_sort_list:
        ratio = to_sort[x]/sum_of_words
        print('{:15}{:3}{:19.2f}'.format(x,to_sort[x],ratio))

if args.sort == 'byfreq':
    to_sort_list = sorted(to_sort, key=to_sort.get, reverse = True)
    for x in (to_sort_list):
        ratio = to_sort[x]/sum_of_words
        print('{:15}{:3}{:19.2f}'.format(x,to_sort[x],ratio))
