from AFD import StateMachine

defaultPath = "/home/florin/Documents/GitHub/Programare/FMI/ANUL III/SEM 1/LFTC/lab2/"

def display_menu():
    print("\n=== Meniu Automat Finit Determinist ===")
    print("1. Afișează informații despre automat")
    print("2. Testează o secvență")
    print("3. Determină cel mai lung prefix acceptat")
    print("4. Ieșire")
    return input("Alegeți o opțiune (1-4): ")

def display_info_menu(automaton):
    print("\n=== Meniu Informații Automat ===")
    print("1. Afișează alfabetul automatului")
    print("2. Afișează starea inițială")
    print("3. Afișează stările și tranzițiile")
    print("4. Afișează stările finale")
    print("5. Înapoi la meniul principal")
    option = input("Alegeți o opțiune (1-5): ")
    
    if option == '1':
        # Afișează alfabetul automatului
        print("Alfabetul automatului:", automaton.alphabet)
        
    elif option == '2':
        # Afișează starea inițială
        start_state = automaton.start_state.description if automaton.start_state else "Nedefinită"
        print("Starea inițială:", start_state)
        
    elif option == '3':
        # Afișează stările și tranzițiile
        print("Stările și tranzițiile:")
        for state_name, state in automaton.states.items():
            print(f"  {state_name} (Accept State: {state.is_accept_state})")
            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    print(f"    {state_name} --{symbol}--> {next_state.description}")
        
    elif option == '4':
        # Afișează stările finale
        accept_states = [state.description for state in automaton.states.values() if state.is_accept_state]
        print("Stările finale:", ", ".join(accept_states) if accept_states else "Niciuna")
    
    elif option == '5':
        # Înapoi la meniul principal
        return
    else:
        print("Opțiune invalidă. Vă rugăm să alegeți o opțiune validă.")

def main():
    # Inițializare automat
    automaton = StateMachine("AFD pentru constante intregi")

    # Încărcare automat fie din fișier, fie de la tastatură
    try:
        automaton.load_from_file(defaultPath + 'activitate1-2.txt')
        print("Automatul a fost încărcat cu succes din fișier.")
    except FileNotFoundError:
        print("Fișierul specificat nu a fost găsit. Încercăm citirea de la tastatură.")
        automaton.load_from_input()
    
    # Meniu interactiv
    while True:
        option = display_menu()
        
        if option == '1':
            # Afișare informații despre automat cu submeniu
            display_info_menu(automaton)
        
        elif option == '2':
            # Testează o secvență
            seq = input("Introduceți o secvență de simboluri pentru testare: ")
            try:
                result = automaton.check_sequence(seq)
                print(f"Secvența '{seq}' este acceptată de automat: {result}")
            except ValueError as e:
                print(f"Eroare: {e}")
        
        elif option == '3':
            # Determină cel mai lung prefix acceptat
            seq = input("Introduceți o secvență de simboluri pentru determinarea prefixului: ")
            try:
                prefix = automaton.longest_prefix(seq)
                print(f"Cel mai lung prefix acceptat pentru secvența '{seq}' este: '{prefix}'")
            except ValueError as e:
                print(f"Eroare: {e}")
        
        elif option == '4':
            # Ieșire din program
            print("Ieșire din program. La revedere!")
            break
        
        else:
            print("Opțiune invalidă. Vă rugăm să alegeți o opțiune validă.")

if __name__ == "__main__":
    main()
