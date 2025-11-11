import keyword
import re

# Read Python source file
filename = input("Enter Python source code filename: ")
with open(filename, "r") as f:
    code = f.read()

# Define token groups
keywords = set(keyword.kwlist)
operators = set("+-*/%=><!&|^~")
special_symbols = set("(){}[]:;,.")

# Containers
found_keywords = []
identifiers = []
numbers = []
found_operators = []
found_symbols = []

# Split code into tokens (words + symbols)
tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+|==|!=|<=|>=|[+\-*/%><=(){}[\]:;,.]", code)

for token in tokens:
    if token in keywords:
        found_keywords.append(token)
    elif token.isidentifier():
        identifiers.append(token)
    elif token.isdigit():
        numbers.append(token)
    elif token in operators:
        found_operators.append(token)
    elif token in special_symbols:
        found_symbols.append(token)

# Print results
print("\nTokens:")
print("\nKeywords:")
for k in found_keywords:
    print(k)

print("\nIdentifiers:")
for i in identifiers:
    print(i)

print("\nNumbers:")
for n in numbers:
    print(n)

print("\nOperators:")
for o in found_operators:
    print(o)

print("\nSpecial Symbols:")
for s in found_symbols:
    print(s)
