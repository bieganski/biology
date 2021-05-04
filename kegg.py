#!/usr/bin/env python3
from Bio.KEGG import REST
from Bio.KEGG import Enzyme

file = open("entries", "r")

lines = file.readlines()
lines = list(map(str.strip, lines))
from pprint import pprint


for line in lines:
    request = REST.kegg_get(line)
    a = request.read()
    open("temp.txt", "w").write(a)
    records = Enzyme.parse(open("temp.txt"))
    try:
        record = list(records)[0]
    except:
        print(f"nie udalo sie znalezc {line}")
        continue

    res = ""
    for x in record.name:
        res += x

    # to make it work you need to add parsing description in biopython
    record.description = "DUMMY"

    print(line, res, record.description) # record.classname, record.sysname)
    # pprint(vars(record))
    # print(dir(record))
    # break
