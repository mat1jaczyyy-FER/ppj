#!/usr/bin/env python3
# Dominik Matijaca 0036524568

from sys import stdin, exit

vars = [[]]
def var_filter(x):
    return filter(lambda j: x[1] == j[1], sum(vars, []))

prev = None

for i in stdin:
    i = i.strip()

    if not i:
        continue

    if prev == None:
        prev = i
        continue

    if i.startswith("KR_AZ"):
        del vars[-1]

    elif i.startswith("IDN"):
        var = i.split()[1:3]

        if prev.startswith("<naredba_pridruzivanja>"):
            if not any(var_filter(var)):
                vars[-1].append(var)
        
        elif prev.startswith("KR_ZA"):
            vars.append([])
            vars[-1].append(var)
        
        else:
            f = list(var_filter(var))
            if not f or var[0] == f[-1][0]:
                print("err", var[0], var[1])
                exit(0)

            print(var[0], f[-1][0], var[1])
    
    prev = i
