#!/bin/python
import sys

IMAGE_CONCEPT_LIST = '/Users/tianyux/Documents/775/project/repo/image_concepts/koalar.conceptids'
NOISEME_LIST = '/Users/tianyux/Documents/775/project/repo/audio_labels/noiseme.list'

# check for console parameters
if (len(sys.argv) < 2):
    print('Usage: %s sorted_output' % sys.argv[0])

# read in image concept list
image_concepts = []
try:
    f = open(IMAGE_CONCEPT_LIST, 'r')
    image_concepts = map(lambda x: x.strip(), f.readlines())
finally:
    f.close()

# read in noiseme list
noisemes = []
try:
    f = open(NOISEME_LIST, 'r')
    noisemes = map(lambda x: x.split('/')[-2], f.readlines())
finally:
    f.close()

try:
    f = open(sys.argv[1], 'r')
    curr_pair = None
    curr_sum_score = 0
    curr_cnt = 0
    c_id = None
    n_id = None

    for line in f:
        pair, score = line.split('\t')
        if pair != curr_pair:
            if curr_pair != None:
                # print '%f\t%s\t%s\t:\t%s' % (curr_sum_score / curr_cnt, curr_pair, image_concepts[c_id], noisemes[n_id])
                print '%s\t%s\t%f' % (curr_pair.split(':')[1], curr_pair.split(':')[0], curr_sum_score / curr_cnt)
            curr_pair = pair
            curr_sum_score = 0
            curr_cnt = 0
            c_id = int(pair.split(':')[0]) - 1
            n_id = int(pair.split(':')[1]) - 1
        curr_sum_score += float(score)
        curr_cnt += 1
    # print '%f\t%s\t%s\t:\t%s' % (curr_sum_score / curr_cnt, curr_pair, image_concepts[c_id], noisemes[n_id])
    print '%s\t%s\t%f' % (curr_pair.split(':')[1], curr_pair.split(':')[0], curr_sum_score / curr_cnt)
finally:
    f.close()