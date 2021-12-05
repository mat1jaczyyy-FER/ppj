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

asoc_pushing = False
asoc_pushes = [[]]
asoc_ops = [[]]

loop_levels = []
loop = []
write_loop = False

def write_raw(x):
    global asoc_pushing, asoc_pushes, asoc_ops, loop
    if len(asoc_pushes) > 1:
        if asoc_pushing:
            asoc_pushes[-1].append(x)
        else:
            asoc_ops[-1].append(x)
    elif write_loop:
        loop[-1].append(x)
    else:
        print(x)

def write(x, l=""):
    write_raw(f"{l}\t{x}")

write("MOVE 40000, R7")
write("MOVE 3C000, R5")

def E():
    global asoc_pushing, asoc_pushes, asoc_ops
    asoc_pushes.append([])

    read()
    T()
    asoc_pushes[-1] += asoc_ops[-1]
    asoc_ops[-1].clear()

    asoc_pushing = False
    read()
    if i.startswith("OP_PLUS"):
        read()
        E()
        asoc_ops.append([])
        write("POP R0")
        write("POP R1")
        write("ADD R0, R1, R2")
        write("PUSH R2")
        asoc_ops[-2] = asoc_ops[-1] + asoc_ops[-2]
        del asoc_ops[-1]

    elif i.startswith("OP_MINUS"):
        read()
        E()
        asoc_ops.append([])
        write("POP R0")
        write("POP R1")
        write("SUB R0, R1, R2")
        write("PUSH R2")
        asoc_ops[-2] = asoc_ops[-1] + asoc_ops[-2]
        del asoc_ops[-1]

    else:
        read()

    asoc_pushes[-2] = asoc_pushes[-1] + asoc_pushes[-2]
    del asoc_pushes[-1]

    #print("asoc_pushes", asoc_pushes)
    #print("asoc_ops", asoc_ops)

def T():
    global asoc_pushing, asoc_pushes, asoc_ops
    asoc_pushes.append([])

    read()
    P()

    asoc_pushing = False
    read()
    if i.startswith("OP_PUTA"):
        read()
        T()
        asoc_ops.append([])
        write("CALL MUL")
        asoc_ops[-2] = asoc_ops[-1] + asoc_ops[-2]
        del asoc_ops[-1]

    elif i.startswith("OP_DIJELI"):
        read()
        T()
        asoc_ops.append([])
        write("LOAD R0, (R7)")
        write("LOAD R1, (R7 + 4)")
        write("STORE R0, (R7 + 4)")
        write("STORE R1, (R7)")
        write("CALL DIV")
        asoc_ops[-2] = asoc_ops[-1] + asoc_ops[-2]
        del asoc_ops[-1]

    else:
        read()

    asoc_pushes[-2] = asoc_pushes[-1] + asoc_pushes[-2]
    del asoc_pushes[-1]

    #print("asoc_pushes", asoc_pushes)
    #print("asoc_ops", asoc_ops)

def P():
    global asoc_pushing
    read()

    if i.startswith("BROJ"):
        asoc_pushing = True
        write(f"MOVE %D {i.split()[2]}, R0")
        write(f"PUSH R0")
        read()
    
    elif i.startswith("IDN"):
        asoc_pushing = True
        write(f"LOAD R0, {offset(i.split()[1:3])}")
        write(f"PUSH R0")
        read()

    elif i.startswith("OP_PLUS"):
        read()
        P()

    elif i.startswith("OP_MINUS"):
        read()
        P()
        write(f"POP R0")
        write(f"MOVE 0, R1")
        write(f"SUB R1, R0, R0")
        write(f"PUSH R0")
    
    elif i.startswith("L_ZAGRADA"):
        ...

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
            E()

            for o in asoc_pushes[0]:
                write_raw(o)

            for o in asoc_ops[0]:
                write_raw(o)

            asoc_pushes[0].clear()
            asoc_ops[0].clear()

            write("POP R0")
            write(f"STORE R0, {offset(var)}")
        
        elif prev.startswith("KR_ZA"):
            vars.append([])
            vars[-1].append(var)

            read()
            read()
            E()

            for o in asoc_pushes[0]:
                write_raw(o)

            for o in asoc_ops[0]:
                write_raw(o)

            asoc_pushes[0].clear()
            asoc_ops[0].clear()

            write("POP R0")
            write(f"STORE R0, {offset(var)}")

            write("", f"L{len(loop)}")
            loop_levels.append(len(loop))
            loop.append([])
            write_loop = True

            write(f"LOAD R0, {offset(var)}")
            write("ADD R0, 1, R0")
            write(f"STORE R0, {offset(var)}")

            read()
            E()

            for o in asoc_pushes[0]:
                write_raw(o)

            for o in asoc_ops[0]:
                write_raw(o)

            asoc_pushes[0].clear()
            asoc_ops[0].clear()

            write(f"LOAD R0, {offset(var)}")
            write("POP R1")
            write("CMP R0, R1")
            write(f"JP_SLE L{len(loop) - 1}")

            write_loop = False

    elif prev.startswith("KR_AZ"):
        for o in loop[loop_levels[-1]]:
            write_raw(o)
        
        del loop_levels[-1]
        read()

    else:
        read()

write("LOAD R6, (R5)")
write("HALT")

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
