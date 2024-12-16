start = ''
nonterminals = []
accesible = {}
rules = []

# Citirea regulilor din fisierul activitate.txt
with open("activitate.txt", "r") as f:
    activitate = f.read().splitlines()
    for line in activitate:
        if "->" in line:
            left, right = line.split("->")
            left = left.strip()
            right = right.strip()

            if start == '':
                start = left[0]

            if left not in nonterminals:
                nonterminals.append(left)
                accesible[left] = False

            for char in right:
                if char.isupper() and char not in nonterminals:
                    nonterminals.append(char)
                    accesible[char] = False

            rules.append((left, right))

# Marcăm simbolurile accesibile pornind de la simbolul de start
def mark_accessible(symbol):
    accesible[symbol] = True
    for left, right in rules:
        if left == symbol:
            for char in right:
                if char.isupper() and not accesible[char]:
                    mark_accessible(char)

mark_accessible(start)

# Determinăm simbolurile inaccesibile
inaccessible = [symbol for symbol in nonterminals if not accesible[symbol]]

if (inaccessible):
    print("Simboluri inaccesibile:", ", ".join(inaccessible))
else:
    print("Nu are simboluri inaccesibile.")
