#!/bin/python
import sys

w1 = 0.2
w2 = 0.2
w3 = 0.6

# check for console parameters
if (len(sys.argv) < 4):
    print('Usage: %s input1 input2 input3' % sys.argv[0])

f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'r')
f3 = open(sys.argv[3], 'r')

lines1 = f1.readlines()
lines2 = f2.readlines()
lines3 = f3.readlines()

d = {}

for line in lines1:
    arr = line.split('\t')
    if (arr[0], arr[1]) not in d:
        d[(arr[0], arr[1])] = 0
    d[(arr[0], arr[1])] += float(arr[2]) * w1

for line in lines2:
    arr = line.split('\t')
    if (arr[0], arr[1]) not in d:
        d[(arr[0], arr[1])] = 0
    d[(arr[0], arr[1])] += float(arr[2]) * w2

for line in lines3:
    arr = line.split('\t')
    if (arr[0], arr[1]) not in d:
        d[(arr[0], arr[1])] = 0
    d[(arr[0], arr[1])] += float(arr[2]) * w3

res = []
for nid, cid in d.keys():
    res.append((nid, cid, d[(nid, cid)]))
res.sort(key=lambda x:x[2], reverse=True)

for nid, cid, score in res:
    print "%s\t%s\t%f" % (nid, cid, score)