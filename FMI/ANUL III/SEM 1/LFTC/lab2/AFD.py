from collections import defaultdict

class State:
    def __init__(self, description, is_accept_state=False):
        self.description = description  
        self.is_accept_state = is_accept_state 
        self.transitions = defaultdict(list)

    def add_transition(self, symbol, state):
        """Adauga o tranzitie pentru simbolul dat spre o alta stare."""
        self.transitions[symbol].append(state)

    def get_next_state(self, symbol):
        """Returneaza urmatoarea stare pentru un simbol (doar pentru AFD)"""
        return self.transitions[symbol][0] if symbol in self.transitions and len(self.transitions[symbol]) == 1 else None

    def __repr__(self):
        return f"State({self.description}, is_accept_state={self.is_accept_state})"


class StateMachine:
    def __init__(self, description):
        self.description = description  
        self.start_state = None  
        self.states = {} 
        self.alphabet = set()  

    def set_start_state(self, state_name):
        """Seteaza starea de start a automatului."""
        self.start_state = self.states.get(state_name)

    def add_state(self, state_name, is_accept_state=False):
        """Adauga o stare noua in automat."""
        state = State(state_name, is_accept_state)
        self.states[state_name] = state

    def add_transition(self, from_state_name, symbol, to_state_name):
        """Adauga o tranzitie intre doua stari."""
        if from_state_name in self.states and to_state_name in self.states:
            from_state = self.states[from_state_name]
            to_state = self.states[to_state_name]
            from_state.add_transition(symbol, to_state)
            self.alphabet.add(symbol)  

    def is_deterministic(self):
        """Verifica daca automatul este determinist."""
        for state in self.states.values():
            for _, transitions in state.transitions.items():
                if len(transitions) > 1:
                    return False
        return True

    def check_sequence(self, sequence):
        """Verifica daca secventa este acceptata de automat (pentru AFD)."""
        if not self.is_deterministic():
            raise ValueError("Automatul nu este determinist.")
        
        current_state = self.start_state
        for symbol in sequence:
            if symbol not in self.alphabet:
                return False  
            next_state = current_state.get_next_state(symbol)
            if next_state is None:
                return False
            current_state = next_state
        return current_state.is_accept_state

    def longest_prefix(self, sequence):
        """Determina cel mai lung prefix acceptat de automat (pentru AFD)."""
        if not self.is_deterministic():
            raise ValueError("Automatul nu este determinist.")
        
        current_state = self.start_state
        longest_prefix = ""
        current_prefix = ""

        for symbol in sequence:
            if symbol in self.alphabet and current_state.get_next_state(symbol):
                current_state = current_state.get_next_state(symbol)
                current_prefix += symbol
                if current_state.is_accept_state:
                    longest_prefix = current_prefix
            else:
                break
        return longest_prefix if longest_prefix else 'ε' if self.start_state.is_accept_state else None

    def load_from_file(self, filename):
        """Incarca automatul finit dintr-un fisier specificat."""
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
        
        # Procesare alfabet de stari
        states = lines[0].split(', ')
        for state in states:
            self.add_state(state)
        
        # Procesare alfabet de intrare
        symbols = lines[1].split(', ')
        self.alphabet = set(symbols)

        # Setare stare initiala
        self.set_start_state(lines[2].strip())

        # Setare stari finale
        final_states = lines[3].split(', ')
        for state in final_states:
            self.states[state].is_accept_state = True

        # Procesare tranzitii
        for transition in lines[4:]:
            from_state, to_state, symbol = transition.split(', ')
            self.add_transition(from_state, symbol, to_state)

    def load_from_input(self):
        """Citeste automatul finit de la tastatura."""
        print("Introduceti multimea starilor separate prin virgula:")
        states = input().split(', ')
        for state in states:
            self.add_state(state)
        
        print("Introduceti alfabetul (simboluri separate prin virgula):")
        symbols = input().split(', ')
        self.alphabet = set(symbols)
        
        print("Introduceti starea initiala:")
        self.set_start_state(input().strip())
        
        print("Introduceti multimea starilor finale separate prin virgula:")
        final_states = input().split(', ')
        for state in final_states:
            self.states[state].is_accept_state = True
        
        print("Introduceti tranzitiile (stare_initiala, stare_finala, simbol):")
        print("Pentru a opri introducerea tranzitiilor, tastati 'stop'")
        while True:
            transition = input()
            if transition.lower() == 'stop':
                break
            from_state, to_state, symbol = transition.split(', ')
            self.add_transition(from_state, symbol, to_state)