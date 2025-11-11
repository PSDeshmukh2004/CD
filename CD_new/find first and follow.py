# Simulate FIRST and FOLLOW of a Grammar

productions = {}
non_terminals = []
terminals = []

firsts = {}
follows = {}

# Function to compute FIRST set
def first(symbol):
    if symbol in terminals:
        return set(symbol)
    elif symbol == '#':
        return set('#')

    result = set()
    for prod in productions.get(symbol, []):
        if prod == '#':
            result.add('#')
        else:
            for i in range(len(prod)):
                sym = prod[i]
                sym_first = first(sym)
                result |= (sym_first - set('#'))
                if '#' not in sym_first:
                    break
                if i == len(prod) - 1:
                    result.add('#')
    return result

# Function to compute FOLLOW set
def follow(symbol):
    result = set()
    if symbol == start_symbol:
        result.add('$')

    for nt in productions:
        for prod in productions[nt]:
            for i in range(len(prod)):
                if prod[i] == symbol:
                    if i + 1 < len(prod):
                        result |= (first(prod[i + 1]) - set('#'))
                        if '#' in first(prod[i + 1]):
                            result |= follow(nt)
                    else:
                        if nt != symbol:
                            result |= follow(nt)
    return result


if __name__ == "__main__":
    n = int(input("Enter number of productions: "))
    print("Enter productions (use # for epsilon, use | for alternation):")
    for _ in range(n):
        inp = input().strip()
        lhs, rhs = inp.split("->")
        rhs_alternatives = rhs.split("|")
        productions[lhs] = rhs_alternatives
        if lhs not in non_terminals:
            non_terminals.append(lhs)
        for alt in rhs_alternatives:
            for ch in alt:
                if not ch.isupper() and ch != '#':
                    if ch not in terminals:
                        terminals.append(ch)
                elif ch.isupper():
                    if ch not in non_terminals:
                        non_terminals.append(ch)

    start_symbol = list(productions.keys())[0]

    # Compute FIRST sets
    for nt in non_terminals:
        firsts[nt] = first(nt)

    # Compute FOLLOW sets
    for nt in non_terminals:
        follows[nt] = follow(nt)

    # Print FIRST sets
    print("\nFIRST sets:")
    for nt in non_terminals:
        print(f"FIRST({nt}) = {{ {', '.join(sorted(firsts[nt]))} }}")

    # Print FOLLOW sets
    print("\nFOLLOW sets:")
    for nt in non_terminals:
        print(f"FOLLOW({nt}) = {{ {', '.join(sorted(follows[nt]))} }}")
