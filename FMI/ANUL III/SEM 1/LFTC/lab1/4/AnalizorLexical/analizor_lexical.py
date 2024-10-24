import re

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

# Liste pentru FIP și tabelele de simboluri
fip = []
ts_identifiers = OrderedLinkedList()
ts_constants = OrderedLinkedList()

# Dicționar pentru tokeni și coduri
token_codes = {}

# Regex-uri pentru validare corectă
identifier_regex = r"^[a-zA-Z_]\w{0,254}$"  # Identificatori de maxim 255 caractere
number_regex = r"^-?\d+(\.\d+)?$"           # Constante numerice valide (int sau float)

# Funcție pentru încărcarea codurilor din fișierul 'coduri_token.txt'
def load_token_codes(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            token, code = line.strip().split()
            token_codes[token] = int(code)

# Funcție de tokenizare - separăm tokenii
def tokenize(line):
    # Regex care separă orice este delimitat de spații, operatori și separatori
    token_pattern = r'([a-zA-Z0-9\._\-]+|\+\+|\-\-|[+\-*/%]=?|>>|<<|==|!=|<=|>=|<|>|=|[;,(){}])'   
    tokens = re.findall(token_pattern, line)
    return tokens

# Funcția principală de analiză lexicală
def analyze(file_path):
    global fip, ts_identifiers, ts_constants
    with open(file_path, 'r') as file:
        lines = file.readlines()

    line_number = 0
    processed_tokens = []

    for line in lines:
        line_number += 1
        tokens = tokenize(line.strip())  # Extragem tokenii
        for token in tokens:
            if token in token_codes:
                # Adăugăm tokenii predefiniți pentru a-i procesa ulterior în FIP
                processed_tokens.append((token, None))  # None pentru a indica că nu este ID sau CONST
            elif re.match(identifier_regex, token):
                index = ts_identifiers.insert(token)  # Inserăm identificatorii în lista legată
                processed_tokens.append(("ID", index))   # Stocăm în lista de tokeni procesați
            elif re.match(number_regex, token):
                index = ts_constants.insert(token)  # Inserăm constantele în lista legată
                processed_tokens.append(("CONST", index))  # Stocăm în lista de tokeni procesați
            else:
                # Token necunoscut
                print(f"Eroare lexicală: token necunoscut '{token}' pe linia {line_number}.")
                return

    for token, ts_index in processed_tokens:
        if token == "ID":
            fip.append((0, ts_index))  # Codul 0 pentru identificatori
        elif token == "CONST":
            fip.append((1, ts_index))  # Codul 1 pentru constante
        else:
            fip.append((token_codes[token], ''))  # Codurile pentru tokenii predefiniți

    # Salvăm FIP și TS
    save_fip("FIP.txt")
    save_ts("TS_identifiers.txt", ts_identifiers)
    save_ts("TS_constants.txt", ts_constants)

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
