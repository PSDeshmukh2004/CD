def main():
    state = 0
    count = 0

    print("\nThe string must begin with 'a' and terminate with 'b'")
    print("The Grammar Is:")
    print("\tS -> aS\n\tS -> Sb\n\tS -> ab")

    string = input("Enter the string to be checked: ")

    while count < len(string):
        ch = string[count]

        if state == 0:
            if ch == 'a':
                state = 1
            else:
                state = 3  # Invalid
        elif state == 1:
            if ch == 'a':
                state = 1
            elif ch == 'b':
                state = 2
            else:
                state = 3
        elif state == 2:
            if ch == 'b':
                state = 2
            else:
                state = 3
        else:
            break  # Invalid state

        count += 1
        if state == 3:
            break

    if state == 2:
        print("\nString is accepted\n")
    else:
        print("\nString is not accepted\n")


if __name__ == "__main__":
    main()
