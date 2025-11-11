# Predictive Parsing Table Construction in Python

# Grammar definitions
prol = ["S", "A", "A", "B", "B", "C", "C"]
pror = ["A", "Bb", "Cd", "aB", "@", "Cc", "@"]
prod = ["S->A", "A->Bb", "A->Cd", "B->aB", "B->@", "C->Cc", "C->@"]
first = ["abcd", "ab", "cd", "a@", "@", "c@", "@"]
follow = ["$", "$", "$", "a$", "b$", "c$", "d$"]

# Parsing table initialization
table = [[" " for _ in range(6)] for _ in range(5)]

# Function to map symbols to table indices
def numr(c):
    mapping = {
        'S': 0, 'A': 1, 'B': 2, 'C': 3,
        'a': 0, 'b': 1, 'c': 2, 'd': 3, '$': 4
    }
    return mapping.get(c, 2)

# Main logic
print("The following grammar is used for Parsing Table:\n")
for p in prod:
    print(p)

# Fill table based on FIRST sets
for i in range(7):
    for ch in first[i]:
        if ch != '@':
            table[numr(prol[i][0]) + 1][numr(ch) + 1] = prod[i]

# Fill table based on FOLLOW sets (for epsilon productions)
for i in range(7):
    if len(pror[i]) == 1 and pror[i][0] == '@':
        for ch in follow[i]:
            table[numr(prol[i][0]) + 1][numr(ch) + 1] = prod[i]

# Fill header rows/columns
table[0][0] = " "
table[0][1:] = ["a", "b", "c", "d", "$"]
table[1][0], table[2][0], table[3][0], table[4][0] = "S", "A", "B", "C"

# Display the predictive parsing table
print("\nPredictive Parsing Table:")
print("--------------------------------------------------------")
for i in range(5):
    for j in range(6):
        print(f"{table[i][j]:<10}", end="")
        if j == 5:
            print("\n--------------------------------------------------------")
