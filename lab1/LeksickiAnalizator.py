#!/usr/bin/env python3
# Dominik Matijaca 0036524568

from sys import stdin

def flatten(x):
    return sum(x, [])

math = {
    "=": "OP_PRIDRUZI",
    "+": "OP_PLUS",
    "-": "OP_MINUS",
    "*": "OP_PUTA",
    "/": "OP_DIJELI",
    "(": "L_ZAGRADA",
    ")": "R_ZAGRADA"
}

keywords = {
    "za": "KR_ZA",
    "od": "KR_OD",
    "do": "KR_DO",
    "az": "KR_AZ"
}

cnt = 0

for line in stdin:
    cnt += 1

    line = line.strip().split("//")[0].strip().split()
    
    if not len(line):
        continue

    for op in math.keys():
        line = [i for i in flatten([flatten([[j, op] for j in i.split(op)])[:-1] for i in line]) if len(i)]

    for i in line:
        if i in math:
            op = math[i]
        if i in keywords:
            op = keywords[i]
        elif i[0].isalpha():
            op = "IDN"
        elif i[0].isnumeric():
            op = "BROJ"
        
        print(f"{op} {cnt} {i}")