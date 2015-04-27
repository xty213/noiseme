#!/bin/python

import sys

# check for console parameters
if (len(sys.argv) < 2):
    print('Usage: %s sorted_output' % sys.argv[0])

# read correlations
f = open(sys.argv[1], 'r')
lines = f.readlines()
f.close()

# compute normalized scores based on ranking
cnt = 0.0
for line in lines:
    line_arr = line.split()
    print '%s\t%s\t%f' % (line_arr[0], line_arr[1], 1 - (cnt / len(lines)))
    cnt += 1
