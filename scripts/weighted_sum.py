#!/bin/python

w1 = 0.2
w2 = 0.2
w3 = 0.6

f1 = open("normalized_5000/1.txt", 'r')
f2 = open("normalized_5000/2.txt", 'r')
f3 = open("normalized_5000/3.txt", 'r')

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