#!/bin/python
import sys

# filter_list = ['23', '24', '31', '19', '6', '13', '27']
filter_list = []

if (len(sys.argv) != 2):
    print('Usage: %s sorted_output' % sys.argv[0])

try:
    f = open(sys.argv[1], 'r')
    curr_pair = None
    curr_sum_score = 0

    for line in f:
        pair, score = line.split('\t')
        if pair != curr_pair:
            if curr_pair != None and curr_pair.split(':')[1] not in filter_list:
                print '%f\t%s' % (curr_sum_score, curr_pair)
            curr_pair = pair
            curr_sum_score = 0
        curr_sum_score += float(score)
    print '%f\t%s' % (curr_sum_score, curr_pair)
finally:
    f.close()