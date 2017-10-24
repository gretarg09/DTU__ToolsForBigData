#!/usr/bin/env python

import sys

# mapper 

for line in sys.stdin:
    words = line.split()
    for word in words:
        print "%s\t%d" % (word,1)
        
#cat file.txt | ./mapper.py | sort | ./reducer.py