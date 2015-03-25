#!/bin/python
import sys

if (len(sys.argv) < 2):
    print('Usage: %s sorted_output' % sys.argv[0])

try:
    f = open(sys.argv[1], 'r')
    curr_pair = None
    curr_sum_score = 0
    curr_cnt = 0

    for line in f:
        pair, score = line.split('\t')
        if pair != curr_pair:
            if curr_pair != None:
                print '%f\t%s' % (curr_sum_score / curr_cnt, curr_pair)
            curr_pair = pair
            curr_sum_score = 0
            curr_cnt = 0
        curr_sum_score += float(score)
        curr_cnt += 1
    print '%f\t%s' % (curr_sum_score / curr_cnt, curr_pair)
finally:
    f.close()