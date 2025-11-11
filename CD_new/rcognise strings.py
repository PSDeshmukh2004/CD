import re

def check_language(s):
    # Regex for a*
    if re.fullmatch(r"a*", s):
        return "String belongs to language a*"
    # Regex for a*b+
    elif re.fullmatch(r"a*b+", s):
        return "String belongs to language a*b+"
    else:
        return "String does not match any language"

if __name__ == "__main__":
    print("Enter strings to test (type 'exit' to stop):\n")
    while True:
        s = input("Input: ").strip()
        if s.lower() == "exit":
            print("\nProgram terminated.")
            break
        print("=>", check_language(s))
