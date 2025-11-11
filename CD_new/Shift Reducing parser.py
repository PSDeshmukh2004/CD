def shift_reduce_parser(input_string):
    print("GRAMMAR RULES:")
    grammar = {
        "E": ["E + E", "E * E", "( E )", "id"]
    }

    for lhs, rhs_list in grammar.items():
        for rhs in rhs_list:
            print(f"{lhs} → {rhs}")
    print("\nSHIFT-REDUCE PARSING PROCESS:")
    print("Stack\t\tInput\t\tAction")

    stack = []
    input_buffer = input_string.split()
    input_buffer.append('$')  # end marker

    while True:
        print(f"{' '.join(stack):10}\t{' '.join(input_buffer):15}", end='')

        # Accept condition
        if stack == ['E'] and input_buffer[0] == '$':
            print("ACCEPT")
            break

        # Try to reduce
        reduced = False
        for lhs, rhs_list in grammar.items():
            for rhs in rhs_list:
                rhs_symbols = rhs.split()
                if len(stack) >= len(rhs_symbols) and stack[-len(rhs_symbols):] == rhs_symbols:
                    for _ in rhs_symbols:
                        stack.pop()
                    stack.append(lhs)
                    print(f"Reduce by {lhs} → {rhs}")
                    reduced = True
                    break
            if reduced:
                break

        # If reduced, continue to allow chained reductions
        if reduced:
            continue

        # If not reduced, shift next input symbol
        if input_buffer:
            symbol = input_buffer.pop(0)
            if symbol == '$':
                print("ERROR: Invalid String")
                break
            stack.append(symbol)
            print("Shift")
        else:
            print("ERROR: Input exhausted")
            break


# --- MAIN PROGRAM ---
expr = input("Enter input string (use spaces, e.g., id + id * id): ")
shift_reduce_parser(expr)
