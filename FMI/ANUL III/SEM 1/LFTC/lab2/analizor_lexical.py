import re
from AFD import StateMachine

class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class OrderedLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.nodes = []  

    def insert(self, value):
        index = self.index_of(value)
        if index != -1:
            return index  

        new_node = Node(value)
        self.nodes.append(new_node)  

        if self.head is None:  
            self.head = self.tail = new_node
        else:
            current = self.head
            prev_node = None

            while current and current.value < value:
                prev_node = current
                current = current.next

            if current is None:  
                prev_node.next = new_node
                new_node.prev = prev_node
                self.tail = new_node
            elif prev_node is None: 
                new_node.next = self.head
                self.head.prev = new_node
                self.head = new_node
            else:  
                prev_node.next = new_node
                new_node.prev = prev_node
                new_node.next = current
                if current:
                    current.prev = new_node

        self.size += 1
        return self.size - 1 

    def index_of(self, value):
        for i, node in enumerate(self.nodes):
            if node.value == value:
                return i
        return -1  

    def get_links(self):
        result = []
        for node in self.nodes:
            prev_index = self.index_of(node.prev.value) if node.prev else None
            next_index = self.index_of(node.next.value) if node.next else None
            result.append((node.value, prev_index, next_index))
        return result

    def to_list_in_order(self):
        return [node.value for node in self.nodes]
    
    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.nodes = []

# Liste pentru FIP și tabelele de simboluri
fip = []
ts_identifiers = OrderedLinkedList()
ts_constants = OrderedLinkedList()

# Dicționar pentru tokeni și coduri
token_codes = {}

# AFD-uri pentru identificatori și numere
afd_identificatori = StateMachine("AFD pentru Identificatori")
afd_identificatori.load_from_file("afd_identificatori.txt")

afd_intregi = StateMachine("AFD pentru Constante Întregi")
afd_intregi.load_from_file("afd_intregi.txt")

afd_reale = StateMachine("AFD pentru Constante Reale")
afd_reale.load_from_file("afd_reale.txt")

# Funcție pentru încărcarea codurilor din fișierul 'coduri_token.txt'
def load_token_codes(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            token, code = line.strip().split()
            token_codes[token] = int(code)

# Funcția principală de analiză lexicală
def analyze(file_path):
    global fip, ts_identifiers, ts_constants
    with open(file_path, 'r') as file:
        lines = file.readlines()

    line_number = 0
    processed_tokens = []
    operators_and_separators = ['+=', '-=', '/=', '*=', '%=', '>>', '<<', '==', '!=', '<=', '>=', '--', '++', '>', '<', '+', '-', '*', '/', '%', '=', '(', ')', '{', '}', ';', ',']
    keywords = ['if', 'while', 'return', 'int', 'float', 'cin', 'cout']

    for line in lines:
        line_number += 1
        line = line.strip()  # Înlăturăm spațiile de la început și sfârșit

        while line:
            longest_int_prefix = afd_intregi.longest_prefix(line) or ""
            longest_real_prefix = afd_reale.longest_prefix(line) or ""
            longest_id_prefix = afd_identificatori.longest_prefix(line) or ""
            longest_prefix = max(longest_int_prefix, longest_real_prefix, longest_id_prefix, key=len)

            if len(longest_prefix) > 0: 
                if len(longest_id_prefix) == len(longest_prefix):
                # Verificăm dacă prefixul este un token cunoscut
                    found_token = False
                    for token in keywords:
                        if line.startswith(token):
                            processed_tokens.append((token, None))
                            line = line[len(token):].strip()  # Eliminăm token-ul recunoscut din linie
                            found_token = True
                            break
                    
                    if found_token:
                        continue

                    if longest_id_prefix[0].isalpha():
                        index = ts_identifiers.insert(longest_id_prefix)
                        processed_tokens.append(("ID", index))
                        line = line[len(longest_id_prefix):].strip()
                        continue
                    else:
                        print(f"Eroare lexicală: identificator invalid '{longest_id_prefix}' pe linia {line_number}.")
                        return
                elif len(longest_prefix) == len(longest_int_prefix) or len(longest_prefix) == len(longest_real_prefix):
                    index = ts_constants.insert(longest_prefix)
                    processed_tokens.append(("CONST", index))
                    line = line[len(longest_prefix):].strip() 
                    continue
            else:
                # Verificăm dacă prefixul este un operator sau separator
                found_operator = False
                for op in operators_and_separators:
                    if line.startswith(op):
                        processed_tokens.append((op, None))
                        line = line[len(op):].strip()
                        found_operator = True
                        break

                if found_operator:
                    continue

                # Dacă niciunul dintre cazuri nu se potrivește, avem un token necunoscut
                unknown_token = line.split()[0] if line.split() else line
                print(f"Eroare lexicală: token necunoscut '{unknown_token}' pe linia {line_number}.")
                return

    # Actualizăm FIP în funcție de tokenii procesați
    for token, ts_index in processed_tokens:
        if token == "ID":
            fip.append((0, ts_index))  # Codul 0 pentru identificatori
        elif token == "CONST":
            fip.append((1, ts_index))  # Codul 1 pentru constante
        else:
            fip.append((token_codes[token], ''))  # Codurile pentru tokenii predefiniți

    # Salvăm FIP și tabelele de simboluri
    save_fip("FIP.txt")
    save_ts("TS_identifiers.txt", ts_identifiers)
    save_ts("TS_constants.txt", ts_constants)

    print("Analiza lexicală a fost finalizată cu succes.")
    fip.clear()
    ts_identifiers.clear()
    ts_constants.clear()


# Funcție pentru salvarea FIP
def save_fip(file_name):
    with open(file_name, 'w') as file:
        file.write("")
        for entry in fip:
            if entry[1] == '':
                file.write(f"{entry[0]}\n")
            else:
                file.write(f"{entry[0]} {entry[1]}\n")

# Funcție pentru salvarea tabelului de simboluri cu legăturile dintre noduri
def save_ts(file_name, ts):
    with open(file_name, 'w') as file:
        file.write("")
        for i, (value, prev, next_) in enumerate(ts.get_links()):
            file.write(f"{i}: {value}, prev: {prev}, next: {next_}\n")

# Funcția principală
def main():
    try:
        load_token_codes('coduri_token.txt')
    except FileNotFoundError:
        print("Fișierul 'coduri_token.txt' nu a fost găsit.")
        return

    default_path = "/home/florin/Documents/GitHub/Programare/FMI/ANUL III/SEM 1/LFTC/lab1/2/"

    while True:

        program = input("Enter the program name (or x to exit): ")
        if program == 'x':
            break
        file_path = default_path + program

        try:
            analyze(file_path)
        except FileNotFoundError:
            print(f"Fișierul {file_path} nu a fost găsit.")

if __name__ == "__main__":
    main()
