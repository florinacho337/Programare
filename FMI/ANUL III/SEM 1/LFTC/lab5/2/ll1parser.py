class LL1Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.stack = []
        self.expression = []

    def load_expression(self, fip_path):
        with open(f"2/{fip_path}", "r") as file:
            for line in file:
                self.expression.append(line.split()[0])

    def parse(self, fip_path):
        self.load_expression(fip_path)
        # Initialize the stack and input
        self.stack = [self.grammar.start_symbol]
        input_tokens = list(self.expression) + ["$"]
        used_rules = []

        while self.stack:
            top = self.stack.pop()
            current_token = input_tokens[0]

            if top in self.grammar.terminals or top == "$":
                # Match terminal or end of input
                if top == current_token:
                    input_tokens.pop(0)
                else:
                    return False, used_rules
            elif top in self.grammar.non_terminals:
                # Non-terminal: apply rule from parse table
                production = self.grammar.parse_table.get((top, current_token))
                if production:
                    rule_index = self.grammar.get_rule_index(top, production)
                    used_rules.append(rule_index)

                    # Push production onto stack in reverse order
                    if production != ["ε"]:  # Skip ε productions
                        self.stack.extend(reversed(production))
                else:
                    return False, used_rules
            else:
                return False, used_rules

        return True, used_rules
