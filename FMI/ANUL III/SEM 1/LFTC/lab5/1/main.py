from ll1parser import LL1Parser
from grammar import Grammar

def main():
    grammar = Grammar("S")

    grammar.read_rules_from_file("1/grammar.txt")

    if not grammar.verify_ll1_applicability():
        print("The grammar is not suitable for LL(1) parsing.")
        return
    
    grammar.compute_first()
    grammar.compute_follow()
    grammar.build_parse_table()

    parser = LL1Parser(grammar)

    expression = input("Enter the input expression: ")

    success, rule_indexes = parser.parse(expression)

    if success:
        print(f"The expression '{expression}' is accepted by the grammar.")
        print("Indexes of the rules used in parsing:")
        print(rule_indexes)
    else:
        print(f"The expression '{expression}' is not accepted by the grammar.")

if __name__ == "__main__":
    main()
