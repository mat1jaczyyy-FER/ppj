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
    if i.startswith("OP_PLUS"):
        read()
        o[0][0:0], o[1][0:0] = E()
        o[1][0:0] = [
            "POP R0",
            "POP R1",
            "ADD R0, R1, R2",
            "PUSH R2"
        ]

    elif i.startswith("OP_MINUS"):
        read()
        o[0][0:0], o[1][0:0] = E()
        o[1][0:0] = [
            "POP R0",
            "POP R1",
            "SUB R0, R1, R2",
            "PUSH R2"
        ]

    else:
        read()
    
    return o

def T():
    read()
    o = [P(), []]

    read()
    if i.startswith("OP_PUTA"):
        read()
        o[0][0:0], o[1][0:0] = T()
        o[1][0:0] = [
            "CALL MUL"
        ]

    elif i.startswith("OP_DIJELI"):
        read()
        o[0][0:0], o[1][0:0] = T()
        o[1][0:0] = [
            "LOAD R0, (R7)",
            "LOAD R1, (R7 + 4)",
            "STORE R0, (R7 + 4)",
            "STORE R1, (R7)",
            "CALL DIV"
        ]

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
        ...
    
    return o
    
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
            
            read()
            read()

            writemany(flatten(E()))

            writemany([
                "POP R0",
                f"STORE R0, {offset(var)}"
            ])
        
        elif prev.startswith("KR_ZA"):
            vars.append([])
            vars[-1].append(var)

            read()
            read()

            for o in flatten(E()):
                write(o)

            writemany([
                "POP R0",
                f"STORE R0, {offset(var)}"
            ])

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

# multiplication algorithm
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
write("POP R1")
write("POP R0")
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

write("CALL MD_INIT", "MUL")
write("XOR R1, 0, R1")
write("JP_Z MUL_RET")
write("SUB R1, 1, R1")
write("ADD R2, R0, R2", "MUL_1")
write("SUB R1, 1, R1")
write("JP_NN MUL_1")
write("CALL MD_RET", "MUL_RET")
write("RET")

write("CALL MD_INIT", "DIV")
write("XOR R1, 0, R1")
write("JP_Z DIV_RET")
write("ADD R2, 1, R2", "DIV_1")
write("SUB R0, R1, R0")
write("JP_NN DIV_1")
write("SUB R2, 1, R2")
write("CALL MD_RET", "DIV_RET")
write("RET")
