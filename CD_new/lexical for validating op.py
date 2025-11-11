# Simulating lexical analyzer for validating operators

# Operator dictionary
operators = {
    # Arithmetic operators
    "+": ("Arithmetic", "Addition"),
    "-": ("Arithmetic", "Subtraction"),
    "*": ("Arithmetic", "Multiplication"),
    "/": ("Arithmetic", "Division"),
    "%": ("Arithmetic", "Modulus"),

    # Logical operators
    "&&": ("Logical", "Logical AND"),
    "||": ("Logical", "Logical OR"),
    "==": ("Logical", "Equal to"),
    "!=": ("Logical", "Not equal to"),
    ">": ("Logical", "Greater than"),
    "<": ("Logical", "Less than"),
    ">=": ("Logical", "Greater than or equal to"),
    "<=": ("Logical", "Less than or equal to"),

    # Bitwise operators
    "&": ("Bitwise", "Bitwise AND"),
    "|": ("Bitwise", "Bitwise OR"),
    "^": ("Bitwise", "Bitwise XOR"),
    "~": ("Bitwise", "Bitwise NOT"),
    "<<": ("Bitwise", "Left shift"),
    ">>": ("Bitwise", "Right shift"),
}

def validate_operator(op):
    if op in operators:
        op_type, op_name = operators[op]
        print(f"=> '{op}' is a VALID operator")
        print(f"   Type: {op_type}")
        print(f"   Name: {op_name}\n")
    else:
        print(f"=> '{op}' is NOT a valid operator\n")

if __name__ == "__main__":
    print("Enter operator to validate (type 'exit' to quit):\n")
    while True:
        op = input("Input: ").strip()
        if op.lower() == "exit":
            print("\nProgram terminated.")
            break
        validate_operator(op)
