def detect_comments(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    in_multiline = False

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        # Check for single-line comment
        if line.startswith("#"):
            print(f"There is a single-line comment on line {line_number}")

        # Detect multi-line comments (''' or """)
        if "'''" in line or '"""' in line:
            if not in_multiline:
                in_multiline = True
                print(f"There is a multi-line comment on line {line_number}")
            else:
                in_multiline = False
                print(f"There is a multi-line comment on line {line_number}")
                
if __name__ == "__main__":
    filename = input("Enter Python source filename: ")
    detect_comments(filename)