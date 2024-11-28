nonterminals = []
terminals = []
start = ''
rules = []

with open("activitate.txt", "r") as f:
    activitate = f.read().splitlines()
    for line in activitate:
        rules.append(line)
        for char in line:
            if char == '-' or char == '>' or char == ' ':
                continue
            if start == '':
                start = char
            if char.isupper() and char not in nonterminals:
                nonterminals.append(char)
            if not char.isupper() and char != 'ε' and char not in terminals:
                terminals.append(char)
    
print("Nonterminals: ", nonterminals)
print("Terminals: ", terminals)
print("Production rules: ")
for rule in rules:
    print(rule)
print("Start symbol: ", start)