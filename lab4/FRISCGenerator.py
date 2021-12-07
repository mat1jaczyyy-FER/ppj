#!/usr/bin/env python3
# Dominik Matijaca 0036524568

def flatten(x):
    return sum(x, [])

from sys import stdin, exit

i = ""
prev = None

def read():
    global i, prev
    prev = i
    i = ""
    while not i:
        i = next(stdin, "kraj").strip()

    return prev

read()
read()

def match(x):
    global i
    return any(filter(i.startswith, x))

def error(x):
    print("err", x[0], x[1])
    exit(0)

vars = [[["0", "rez"]]]

def var_filter(x):
    return filter(lambda j: x[1] == j[1], flatten(vars))

def offset(x):
    all = flatten(vars)
    
    for i in range(len(all) - 1, -1, -1):
        if all[i][1] == x[1]:
            return f"(R5 + 0{0x4 * i:0X})"
    
    error(x)

def format(x, l=""):
    return f"{l}\t{x}"

def write(x, l=""):
    print(format(x, l))

def writemany(x):
    for i in x:
        write(i)

def E():
    read()
    o = [flatten(T()), []]

    read()
    d = {
        "OP_PLUS": "ADD",
        "OP_MINUS": "SUB"
    }
    if match(d.keys()):
        op = d[i.split()[0]]
        read()
        o[0][0:0], o[1][0:0] = E()
        o[1][0:0] = [
            "POP R0", # zamijenjene R0 i R1
            "POP R1", # radi asocijativnosti
            f"{op} R0, R1, R2",
            "PUSH R2"
        ]

    else:
        read()
    
    return o

md_used = {
    "MUL": False,
    "DIV": False
}

def T():
    global md_used
    read()
    o = [P(), []]

    read()
    d = {
        "OP_PUTA": "MUL",
        "OP_DIJELI": "DIV"
    }
    if match(d.keys()):
        op = d[i.split()[0]]
        read()
        o[0][0:0], o[1][0:0] = T()
        o[1][0:0] = [
            f"CALL {op}"
        ]
        md_used[op] = True

    else:
        read()
    
    return o

def P():
    o = []
    read()

    if i.startswith("BROJ"):
        o.extend([
            f"MOVE %D {i.split()[2]}, R0",
            "PUSH R0"
        ])
        read()
    
    elif i.startswith("IDN"):
        o.extend([
            f"LOAD R0, {offset(i.split()[1:3])}",
            "PUSH R0"
        ])
        read()

    elif i.startswith("OP_PLUS"):
        read()
        o.extend(P())

    elif i.startswith("OP_MINUS"):
        read()
        o.extend(P())
        o.extend([
            "POP R0",
            "MOVE 0, R1",
            "SUB R1, R0, R0",
            "PUSH R0"
        ])

    elif i.startswith("L_ZAGRADA"):
        read()
        o.extend(flatten(E()))
        read()
    
    return o

def assignment():
    read()
    read()

    writemany(flatten(E()))

    writemany([
        "POP R0",
        f"STORE R0, {offset(var)}"
    ])

loop_levels = []
loops = []

writemany([
    "MOVE 40000, R7",
    "MOVE 3C000, R5"
])

while True:
    if i == "kraj":
        break

    if i.startswith("KR_AZ"):
        del vars[-1]
        read()

    elif i.startswith("IDN"):
        var = i.split()[1:3]

        if prev.startswith("<naredba_pridruzivanja>"):
            if not any(var_filter(var)):
                vars[-1].append(var)
            
            assignment()
        
        elif prev.startswith("KR_ZA"):
            vars.append([])
            vars[-1].append(var)

            assignment()

            write("", f"L{len(loops)}")

            loop = []
            loop.extend([
                f"LOAD R0, {offset(var)}",
                "ADD R0, 1, R0",
                f"STORE R0, {offset(var)}"
            ])

            read()
            loop.extend(flatten(E()))

            loop.extend([
                f"LOAD R0, {offset(var)}",
                "POP R1",
                "CMP R0, R1",
                f"JP_SLE L{len(loops)}"
            ])

            loop_levels.append(len(loops))
            loops.append(loop)

    elif prev.startswith("KR_AZ"):
        writemany(loops[loop_levels[-1]])
        del loop_levels[-1]

        read()

    else:
        read()

writemany([
    "LOAD R6, (R5)",
    "HALT"
])

if md_used["MUL"] or md_used["DIV"]:
    write("MOVE 0, R6", "MD_SGN")
    write("XOR R0, 0, R0")
    write("JP_P MD_TST1")
    write("XOR R0, -1, R0")
    write("ADD R0, 1, R0")
    write("MOVE 1, R6")
    write("XOR R1, 0, R1", "MD_TST1")
    write("JP_P MD_SGNR")
    write("XOR R1, -1, R1")
    write("ADD R1, 1, R1")
    write("XOR R6, 1, R6")
    write("RET", "MD_SGNR")

    write("POP R4", "MD_INIT")
    write("POP R3")
    write("POP R0") # zamijenjene R0 i R1
    write("POP R1") # radi asocijativnosti
    write("CALL MD_SGN")
    write("MOVE 0, R2")
    write("PUSH R4")
    write("RET")

    write("XOR R6, 0, R6", "MD_RET")
    write("JP_Z MD_RET1")
    write("XOR R2, -1, R2")
    write("ADD R2, 1, R2")
    write("POP R4", "MD_RET1")
    write("PUSH R2")
    write("PUSH R3")
    write("PUSH R4")
    write("RET")

if md_used["MUL"]:
    write("CALL MD_INIT", "MUL")
    write("XOR R1, 0, R1")
    write("JP_Z MUL_RET")
    write("SUB R1, 1, R1")
    write("ADD R2, R0, R2", "MUL_1")
    write("SUB R1, 1, R1")
    write("JP_NN MUL_1")
    write("CALL MD_RET", "MUL_RET")
    write("RET")

if md_used["DIV"]:
    write("CALL MD_INIT", "DIV")
    write("XOR R1, 0, R1")
    write("JP_Z DIV_RET")
    write("ADD R2, 1, R2", "DIV_1")
    write("SUB R0, R1, R0")
    write("JP_NN DIV_1")
    write("SUB R2, 1, R2")
    write("CALL MD_RET", "DIV_RET")
    write("RET")
