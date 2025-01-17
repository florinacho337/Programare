import re

class Grammar:
    def __init__(self, start_symbol=None, terminals=None, non_terminals=None):
        self.terminals = terminals or []
        self.non_terminals = non_terminals or []
        self.rules = {}  # Map non-terminal -> list of productions
        self.start_symbol = start_symbol or ""
        self.first = {}
        self.follow = {}
        self.parse_table = {}
        self.rule_list = []  # Array to store all production rules as (non-terminal, production)
        self.rule_index = {}  # Map rule to its index (1-based)
        self.tokens = {}  # Map token to its index (1-based)

    def load_tokens(self):
        with open("2/coduri_token.txt", "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                token, id = line.split()
                token = token.strip()
                id = id.strip()
                self.tokens[token] = id

    def add_rule(self, non_terminal, production):
        if non_terminal not in self.rules:
            self.rules[non_terminal] = []
        self.rules[non_terminal].append(production)

        # Save the rule and assign an index
        rule_id = len(self.rule_list) + 1  # Index is 1-based
        self.rule_list.append((non_terminal, production))
        self.rule_index[(non_terminal, tuple(production))] = rule_id

    def read_rules_from_file(self, file_path):
        self.load_tokens()
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line or "::=" not in line:
                    continue 

                non_terminal, productions = line.split("::=")
                productions = productions.split("|")
                non_terminal = non_terminal.strip()
                productions = [p.strip().split() for p in productions]

                if not self.non_terminals:
                    self.start_symbol = non_terminal

                if non_terminal not in self.non_terminals:
                    self.non_terminals.append(non_terminal)

                for production in productions:
                    for idx, symbol in enumerate(production):
                        if symbol in self.tokens:
                            production[idx] = self.tokens[symbol]
                        if re.match(r"<.*>", symbol) and symbol not in self.non_terminals:
                            self.non_terminals.append(symbol)
                        elif symbol and symbol not in self.terminals and symbol not in self.non_terminals:
                            self.terminals.append(self.tokens[symbol])
                            
                    if not production:
                        production = ["ε"]

                    self.add_rule(non_terminal, production)

        print("Terminals:", self.terminals)
        print("Non-terminals:", self.non_terminals)
        print("Rules:")
        for non_terminal, productions in self.rules.items():
            for production in productions:
                print(f"{non_terminal} -> {' '.join(production)}")

    def get_rule_index(self, non_terminal, production):
        """
        Returns the index of the given rule (non-terminal, production).
        """
        return self.rule_index.get((non_terminal, tuple(production)))

    def get_production_rules_with_indexes(self):
        """
        Returns a list of production rules with their indexes.
        """
        return [(idx + 1, non_terminal, production) for idx, (non_terminal, production) in enumerate(self.rule_list)]

    def verify_ll1_applicability(self):
        errors = []
        for non_terminal, productions in self.rules.items():
            for production in productions:
                if production[0] == non_terminal:
                    errors.append(f"Error: Grammar has left recursion for non-terminal '{non_terminal}'")
                    break;

        for non_terminal, productions in self.rules.items():
            prefixes = set()
            for production in productions:
                if production[0] in prefixes:
                    errors.append(f"Error: Grammar is not left-factored for non-terminal '{non_terminal}'")
                    break;
                prefixes.add(production[0])

        if errors:
            for error in errors:
                print(error)
            return False
        return True

    def compute_first(self):
        self.first = {symbol: set() for symbol in self.non_terminals}
        changed = True

        while changed:
            changed = False
            for non_terminal, productions in self.rules.items():
                for production in productions:
                    for symbol in production:
                        current_first = self.first[non_terminal]
                        if symbol == "ε":  # If the symbol is epsilon
                            if "ε" not in current_first:
                                current_first.add("ε")
                                changed = True
                            break
                        elif symbol in self.terminals:  # If the symbol is a terminal
                            if symbol not in current_first:
                                current_first.add(symbol)
                                changed = True
                            break
                        elif symbol in self.non_terminals:  # If the symbol is a non-terminal
                            new_first = self.first[symbol] - {"ε"}
                            if not new_first.issubset(current_first):
                                current_first.update(new_first)
                                changed = True
                            if "ε" not in self.first[symbol]:
                                break
                        else:
                            raise ValueError(f"Unexpected symbol '{symbol}' in production.")

                    # If all symbols in the production can derive epsilon, add epsilon
                    else:
                        if "ε" not in self.first[non_terminal]:
                            self.first[non_terminal].add("ε")
                            changed = True

    def compute_follow(self):
        self.follow = {symbol: set() for symbol in self.non_terminals}
        self.follow[self.start_symbol].add("$")  # Start symbol gets end-of-input marker
        changed = True

        while changed:
            changed = False
            for non_terminal, productions in self.rules.items():
                for production in productions:
                    for i, symbol in enumerate(production):
                        if symbol in self.non_terminals:  # Only compute FOLLOW for non-terminals
                            follow_target = self.follow[symbol]
                            next_symbols = production[i + 1:]

                            if next_symbols:
                                first_of_next = set()

                                for s in next_symbols:
                                    if s == "ε":  # Skip epsilon
                                        continue
                                    elif s in self.terminals:  # If it's a terminal, add it to FIRST directly
                                        first_of_next.add(s)
                                        break
                                    elif s in self.non_terminals:  # If it's a non-terminal, add its FIRST set
                                        first_of_next.update(self.first[s])
                                        if "ε" not in self.first[s]:
                                            break
                                    else:
                                        raise ValueError(f"Unexpected symbol '{s}' in production.")

                                # Handle epsilon in the first set of next_symbols
                                if "ε" in first_of_next:
                                    first_of_next.remove("ε")
                                    if not self.follow[non_terminal].issubset(follow_target):
                                        follow_target.update(self.follow[non_terminal])
                                        changed = True

                                # Update the FOLLOW set of the current non-terminal
                                if not first_of_next.issubset(follow_target):
                                    follow_target.update(first_of_next)
                                    changed = True
                            else:  # If there are no symbols after the current symbol
                                if not self.follow[non_terminal].issubset(follow_target):
                                    follow_target.update(self.follow[non_terminal])
                                    changed = True

    def build_parse_table(self):
        self.parse_table = {}

        for non_terminal, productions in self.rules.items():
            for production in productions:
                first_set = set()

                # Compute the FIRST set for the production
                for symbol in production:
                    if symbol in self.terminals:  # If the symbol is a terminal, add it directly
                        first_set.add(symbol)
                        break
                    elif symbol in self.non_terminals:  # If it's a non-terminal, add its FIRST set
                        first_set.update(self.first[symbol])
                        if "ε" not in self.first[symbol]:  # Stop if ε is not in the FIRST set
                            break
                    elif symbol == "ε":  # Handle explicit epsilon
                        first_set.add("ε")
                        break
                    else:
                        raise ValueError(f"Unexpected symbol '{symbol}' in production.")

                # Handle epsilon in the FIRST set
                if "ε" in first_set:
                    first_set.remove("ε")  # Epsilon isn't added as a terminal
                    follow_set = self.follow[non_terminal]
                    for terminal in follow_set:  # Add FOLLOW(non_terminal) for ε
                        if (non_terminal, terminal) in self.parse_table:
                            raise ValueError(f"Grammar is not LL(1): Conflict at ({non_terminal}, {terminal}).")
                        self.parse_table[(non_terminal, terminal)] = production

                # Fill the parse table for terminals in the FIRST set
                for terminal in first_set:
                    if (non_terminal, terminal) in self.parse_table:
                        raise ValueError(f"Grammar is not LL(1): Conflict at ({non_terminal}, {terminal}).")
                    self.parse_table[(non_terminal, terminal)] = production

        # Display the parse table
        print("Parse table:")
        for key, value in self.parse_table.items():
            print(f"{key}: {value}")
