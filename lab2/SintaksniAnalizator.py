#!/usr/bin/env python3
# Dominik Matijaca 0036524568

from sys import stdin, exit

i = ""

def match(*x):
    global i
    return any(filter(i.startswith, x))

def must(*x):
    global i
    if not match(x):
        print("err", i)
        exit(0)

def read():
    global i
    old = i
    i = ""
    while not i:
        i = next(stdin, "kraj").strip()

    return old

read()

output = []
level = 0
cnt = 0

def write(x):
    global level, cnt

    output.append(" " * level + x)
    cnt += 1

def eat():
    write(read())

def push(x):
    global level, cnt

    write(f"<{x}>")
    level += 1
    cnt = 0

def pop():
    global level, cnt

    if cnt == 0:
        write("$")

    level -= 1

def E():
    push("E")
    T()

    push("E_lista")
    if match("OP_PLUS", "OP_MINUS"):
        eat()
        E()

    pop()
    pop()

def T():
    push("T")
    P()

    push("T_lista")
    if match("OP_PUTA", "OP_DIJELI"):
        eat()
        T()

    pop()
    pop()

def P():
    push("P")

    must("OP_PLUS", "OP_MINUS", "IDN", "BROJ", "L_ZAGRADA")

    if match("OP_PLUS", "OP_MINUS"):
        eat()
        P()
    
    elif match("IDN", "BROJ"):
        eat()
    
    elif match("L_ZAGRADA"):
        eat()
        E()
        must("D_ZAGRADA")
        eat()

    pop()

def lista_naredbi():
    push("lista_naredbi")

    if match("IDN", "OP_PRIDRUZI", "KR_ZA"):
        push("naredba")
        must("IDN", "KR_ZA")

        if match("IDN"):
            idn = read()

            must("OP_PRIDRUZI")
            push("naredba_pridruzivanja")

            write(idn)
            eat()

            E()
            pop()

        elif match("KR_ZA"):
            push("za_petlja")
            eat()

            must("IDN")
            eat()

            must("KR_OD")
            eat()

            E()
            
            must("KR_DO")
            eat()

            E()
            lista_naredbi()
            
            must("KR_AZ")
            eat()
            pop()

        pop()
        lista_naredbi()

    pop()

push("program")
lista_naredbi()
pop()

for l in output:
    print(l)
