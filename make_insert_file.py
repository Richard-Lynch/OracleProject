#!/usr/local/bin/python3
import sys
with open("person_inserts.csv") as f:
    lis = [line.split() for line in f]

for l in lis:
    print(l)

sys.exit()
