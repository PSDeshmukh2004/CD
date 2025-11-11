class Node:
    def __init__(self, id_num):
        self.id_num = id_num
        self.st_val = 0  # Final state (0 or 1)
        self.link0 = None
        self.link1 = None


def simulate_dfa():
    vst_arr = []
    a = []

    print("=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=")
    count = int(input("Enter the number of states in the m/c: "))

    # Create states
    q = [Node(i) for i in range(count)]

    # Define transitions and final states
    for i in range(count):
        print(f"State Machine::{i}")

        posi = int(input("Next State if i/p is 0: "))
        q[i].link0 = q[posi]

        posi = int(input("Next State if i/p is 1: "))
        q[i].link1 = q[posi]

        q[i].st_val = int(input("Is the state final state (0/1)? "))

    # Set start state
    posi = int(input("Enter the Initial State of the m/c: "))
    start = q[posi]

    print("=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=")

    while True:
        print("=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=")
        j = int(input("Perform String Check (0/1): "))

        if j == 0:
            print("Exiting DFA simulation.")
            break

        ptr = start
        n = input("Enter the string of inputs (0s and 1s): ")

        a = [int(ch) for ch in n if ch in ('0', '1')]

        print("The visited States of the m/c are:", end="")
        i = 0
        while i < len(a):
            vst_arr.append(ptr.id_num)

            if a[i] == 0:
                ptr = ptr.link0
            elif a[i] == 1:
                ptr = ptr.link1
            else:
                print("\nINCORRECT INPUT")
                return 1

            print(f"[{vst_arr[i]}]", end="")
            i += 1

        print()
        print(f"Present State: {ptr.id_num}")
        print("String Status:", end=" ")

        if ptr.st_val == 1:
            print("String Accepted")
        else:
            print("String Not Accepted")

    return 0


# Main function
if __name__ == "__main__":
    result = simulate_dfa()
    if result != 0:
        print("DFA simulation encountered an error.")
