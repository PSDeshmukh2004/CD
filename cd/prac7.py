# Operator Precedence Parsing in Python 

def operator_precedence_parsing():
    # Input
    n = int(input("Enter the number of terminals: "))
    ter = input("Enter the terminals (no spaces): ").strip()

    # Initialize operator precedence table
    opt = [["" for _ in range(n)] for _ in range(n)]
    print("\nEnter the table values:")
    for i in range(n):
        for j in range(n):
            opt[i][j] = input(f"Enter the value for {ter[i]} {ter[j]}: ").strip()

    # Display the table
    print("\n**** OPERATOR PRECEDENCE TABLE ****")
    print("\t", end="")
    for i in range(n):
        print(ter[i], end="\t")
    print()
    for i in range(n):
        print(ter[i], end="\t")
        for j in range(n):
            print(opt[i][j], end="\t")
        print()

    # Input string
    ip = input("\nEnter the input string (append $ at end): ").strip()

    # Initialize stack and input
    stack = ['$']
    i = 0

    print("\nSTACK\t\t\tINPUT STRING\t\t\tACTION\n")
    print("".join(stack).ljust(20), ip.ljust(20), end="\t")

    while i < len(ip):
        # Get top terminal from stack (rightmost terminal)
        top_terminal = None
        for sym in reversed(stack):
            if sym in ter:
                top_terminal = sym
                break

        if top_terminal is None:
            print("\nError: No terminal found in stack.")
            break

        # Find indices in precedence table
        try:
            col = ter.index(top_terminal)
            row = ter.index(ip[i])
        except ValueError:
            print("\nError: Unknown terminal encountered.")
            break

        relation = opt[col][row]

        # ACCEPT condition
        if stack == ['$'] and ip[i] == '$':
            print("String is accepted")
            break

        # SHIFT operation
        if relation in ['<', '=']:
            stack.append(relation)
            stack.append(ip[i])
            print(f"Shift {ip[i]}")
            i += 1

        # REDUCE operation
        elif relation == '>':
            # Reduce until '<' is found
            while stack and stack[-1] != '<':
                stack.pop()
            if stack and stack[-1] == '<':
                stack.pop()  # remove '<'
            print("Reduce")

        else:
            print("\nString is not accepted (invalid relation)")
            break

        # Show stack + remaining input after each step
        print("".join(stack).ljust(20), ip[i:].ljust(20), end="\t")

    print()


# Run program
if __name__ == "__main__":
    operator_precedence_parsing()
