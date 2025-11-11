TSIZE = 128
table = [[0] * TSIZE for _ in range(100)]
terminal = [0] * TSIZE
nonterminal = [0] * 26

class Production:
    def __init__(self, s=""):
        self.str = s
        self.len = len(s)

pro = []
no_pro = 0

first = [[0] * TSIZE for _ in range(26)]
follow = [[0] * TSIZE for _ in range(26)]
first_rhs = [[0] * TSIZE for _ in range(100)]

def isNT(c):
    return 'A' <= c <= 'Z'

def readFromFile(filename="text.txt"):
    global no_pro
    with open(filename, "r") as f:
        lines = f.readlines()

    for buffer in lines:
        buffer = buffer.strip()
        if not buffer:
            continue
        print(buffer)
        j = 0
        nonterminal[ord(buffer[0]) - ord('A')] = 1
        current = ""
        for i, ch in enumerate(buffer):
            if ch == '|':
                pro.append(Production(current))
                no_pro += 1
                current = buffer[:3]  # Copy "A->"
            else:
                current += ch
                if not isNT(ch) and ch not in "-|>":
                    terminal[ord(ch)] = 1
        pro.append(Production(current))
        no_pro += 1

def add_FIRST_A_to_FOLLOW_B(A, B):
    for i in range(TSIZE):
        if chr(i) != '^':
            follow[ord(B) - 65][i] |= first[ord(A) - 65][i]

def add_FOLLOW_A_to_FOLLOW_B(A, B):
    for i in range(TSIZE):
        if chr(i) != '^':
            follow[ord(B) - 65][i] |= follow[ord(A) - 65][i]

def FOLLOW():
    for _ in range(no_pro):
        for k in range(26):
            if not nonterminal[k]:
                continue
            nt = chr(k + 65)
            for p in pro:
                for j in range(3, p.len):
                    if nt == p.str[j]:
                        x = j + 1
                        while x < p.len:
                            sc = p.str[x]
                            if isNT(sc):
                                add_FIRST_A_to_FOLLOW_B(sc, nt)
                                if first[ord(sc) - 65][ord('^')]:
                                    x += 1
                                    continue
                            else:
                                follow[ord(nt) - 65][ord(sc)] = 1
                            break
                        if x == p.len:
                            add_FOLLOW_A_to_FOLLOW_B(p.str[0], nt)

def add_FIRST_A_to_FIRST_B(A, B):
    for i in range(TSIZE):
        if chr(i) != '^':
            first[ord(B) - 65][i] |= first[ord(A) - 65][i]

def FIRST():
    for _ in range(no_pro):
        for p in pro:
            for j in range(3, p.len):
                sc = p.str[j]
                if isNT(sc):
                    add_FIRST_A_to_FIRST_B(sc, p.str[0])
                    if first[ord(sc) - 65][ord('^')]:
                        continue
                else:
                    first[ord(p.str[0]) - 65][ord(sc)] = 1
                break
            else:
                first[ord(p.str[0]) - 65][ord('^')] = 1

def add_FIRST_A_to_FIRST_RHS__B(A, B):
    for i in range(TSIZE):
        if chr(i) != '^':
            first_rhs[B][i] |= first[ord(A) - 65][i]

def FIRST_RHS():
    for _ in range(no_pro):
        for i, p in enumerate(pro):
            for j in range(3, p.len):
                sc = p.str[j]
                if isNT(sc):
                    add_FIRST_A_to_FIRST_RHS__B(sc, i)
                    if first[ord(sc) - 65][ord('^')]:
                        continue
                else:
                    first_rhs[i][ord(sc)] = 1
                break
            else:
                first_rhs[i][ord('^')] = 1

def print_results():
    print("\n")
    for i in range(no_pro):
        if i == 0 or pro[i-1].str[0] != pro[i].str[0]:
            c = pro[i].str[0]
            print(f"FIRST OF {c}: ", end="")
            for j in range(TSIZE):
                if first[ord(c) - 65][j]:
                    print(chr(j), end=" ")
            print()

    print("\n")
    for i in range(no_pro):
        if i == 0 or pro[i-1].str[0] != pro[i].str[0]:
            c = pro[i].str[0]
            print(f"FOLLOW OF {c}: ", end="")
            for j in range(TSIZE):
                if follow[ord(c) - 65][j]:
                    print(chr(j), end=" ")
            print()

    print("\n")
    for i in range(no_pro):
        print(f"FIRST OF {pro[i].str}: ", end="")
        for j in range(TSIZE):
            if first_rhs[i][j]:
                print(chr(j), end=" ")
        print()

def main():
    readFromFile()
    follow[ord(pro[0].str[0]) - 65][ord('$')] = 1
    FIRST()
    FOLLOW()
    FIRST_RHS()
    print_results()

if __name__ == "__main__":
    main()
