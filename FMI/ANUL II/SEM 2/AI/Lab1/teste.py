import math
from timeit import default_timer as timer
from ex1 import ultimul_cuvant, ultimul_cuvant_ai
from ex10 import index_max, index_max_ai
from ex2 import distanta, distanta_ai
from ex3 import produs_scalar, produs_scalar_ai
from ex4 import cuvinte_o_data, cuvinte_o_data_ai
from ex5 import valoare_duplicata, valoare_duplicata_ai
from ex6 import element_majoritar, element_majoritar_ai
from ex7 import al_k_lea_cel_mai_mare, al_k_lea_cel_mai_mare_ai
from ex8 import genereaza_binar, genereaza_binar_ai
from ex9 import suma_submatrice_main, suma_submatrice_main_ai


class Teste:
    def testeaza(self):
        print("Timpi exercitiul 1:")
        print("Timp algoritm uman: " + str(self.__teste_main(ultimul_cuvant, self.__teste1)))
        print("Timp algoritm AI: " + str(self.__teste_main(ultimul_cuvant_ai, self.__teste1)))

        print("Timpi exercitiul 2:")
        print("Timp algoritm uman: " + str(self.__teste_main(distanta, self.__teste2)))
        print("Timp algoritm AI: " + str(self.__teste_main(distanta_ai, self.__teste2)))

        print("Timpi exercitiul 3:")
        print("Timp algoritm uman: " + str(self.__teste_main(produs_scalar, self.__teste3)))
        print("Timp algoritm AI: " + str(self.__teste_main(produs_scalar_ai, self.__teste3)))

        print("Timpi exercitiul 4:")
        print("Timp algoritm uman: " + str(self.__teste_main(cuvinte_o_data, self.__teste4)))
        print("Timp algoritm AI: " + str(self.__teste_main(cuvinte_o_data_ai, self.__teste4)))

        print("Timpi exercitiul 5:")
        print("Timp algoritm uman: " + str(self.__teste_main(valoare_duplicata, self.__teste5)))
        print("Timp algoritm AI: " + str(self.__teste_main(valoare_duplicata_ai, self.__teste5)))

        print("Timpi exercitiul 6:")
        print("Timp algoritm uman: " + str(self.__teste_main(element_majoritar, self.__teste6)))
        print("Timp algoritm AI: " + str(self.__teste_main(element_majoritar_ai, self.__teste6)))

        print("Timpi exercitiul 7:")
        print("Timp algoritm uman: " + str(self.__teste_main(al_k_lea_cel_mai_mare, self.__teste7)))
        print("Timp algoritm AI: " + str(self.__teste_main(al_k_lea_cel_mai_mare_ai, self.__teste7)))

        print("Timpi exercitiul 8:")
        print("Timp algoritm uman: " + str(self.__teste_main(genereaza_binar, self.__teste8)))
        print("Timp algoritm AI: " + str(self.__teste_main(genereaza_binar_ai, self.__teste8)))

        print("Timpi exercitiul 9:")
        print("Timp algoritm uman: " + str(self.__teste_main(suma_submatrice_main, self.__teste9)))
        print("Timp algoritm AI: " + str(self.__teste_main(suma_submatrice_main_ai, self.__teste9)))

        print("Timpi exercitiul 10:")
        print("Timp algoritm uman: " + str(self.__teste_main(index_max, self.__teste10)))
        print("Timp algoritm AI: " + str(self.__teste_main(index_max_ai, self.__teste10)))

        print("Teste finalizate cu succes!")

    # functie generala de test
    # teste_main(functie, dataset)
    # functie - functie de testat
    # dataset - functie care contine toate testele pentru un anumit exercitiu
    # returns: numarul de milisecunde in care au fost executate toate testele
    def __teste_main(self, functie, dataset):
        start_time = timer()
        dataset(functie)
        end_time = timer()

        return end_time - start_time

    # teste ex1
    def __teste1(self, functie):
        assert functie("Ana are mere rosii si galbene") == "si"
        assert functie("") == ""
        assert functie("corp corect") == "corp"
        assert functie("voluntar voluntari") == "voluntari"

    # teste ex2
    def __teste2(self, functie):
        assert functie([1, 5], [4, 1]) == 5.0
        assert functie([1, 2, 3], [2, 3, 4]) is False
        assert functie([0, 0], [0, 0]) == 0.0
        assert functie([0, 1], [1, 0]) == math.sqrt(2)
        assert functie([], []) is False

    # tete ex3
    def __teste3(self, functie):
        assert functie([0, 0], [0, 0]) == 0
        assert functie([1, 2, 0, 0, 4], [1, 0, 0, 2, 1, 5]) is False
        assert functie([1, 2, 0, 0, 4], [1, 0, 0, 2, 1]) == 5
        assert functie([1, 0, 2, 0, 3], [1, 2, 0, 3, 1]) == 4
        assert functie([], []) == 0

    # teste ex4
    def __teste4(self, functie):
        assert functie("ana are ana are mere rosii ana") == ['mere', 'rosii']
        assert functie("ana are mere") == ['ana', 'are', 'mere']
        assert functie("unu doi unu unu trei doi") == ['trei']
        assert functie("unu doi unu unu trei doi trei") == []

    # teste ex5
    def __teste5(self, functie):
        assert functie([1, 2, 3, 4, 2]) == 2
        assert functie([1, 2, 3, 4, 5]) is False
        assert functie([1, 1, 1, 3, 2]) is False
        assert functie([1, 2, 3, 4, 5, 6, 7, 8, 9, 1]) == 1

    # teste ex6
    def __teste6(self, functie):
        assert functie([2, 8, 7, 2, 2, 5, 2, 3, 1, 2, 2]) == 2
        assert functie([1, 2, 3, 4, 5, 3, 2, 5, 3, 2, 6, 8]) is False
        assert functie([]) is False
        assert functie([1, 2, 1, 4, 1, 5, 3, 1, 1, 6, 1]) == 1

    # teste ex7
    def __teste7(self, functie):
        assert functie([7, 4, 6, 3, 9, 1], 2) == 7
        assert functie([1, 2], 3) is False
        assert functie([1, 2, 10, 7, 3, 8], 6) == 1
        assert functie([7, 4, 6, 3, 9, 1], 1) == 9

    # teste ex8
    def __teste8(self, functie):
        assert functie(4) == "1 10 11 100"
        assert functie(1) == "1"
        assert functie(0) == ""

    # teste ex9
    def __teste9(self, functie):
        assert functie([[0, 2, 5, 4, 1],
                        [4, 8, 2, 3, 7],
                        [6, 3, 4, 6, 2],
                        [7, 3, 1, 8, 3],
                        [1, 5, 7, 9, 4]], [[[1, 1], [3, 3]], [[2, 2], [4, 4]]]) == [38, 44]
        assert functie([[0, 2, 5, 4],
                        [4, 8, 2, 3]], [[[0, 0], [1, 1]], [[0, 1], [1, 2]]]) == [14, 17]

        assert functie([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]], [[[0, 0], [1, 1]], [[1, 1], [2, 2]], [[3, 3], [4, 4]]]) == [12, 28, False]
        assert functie([[0, 2, 5, 4, 1, 0, 9],
                        [4, 8, 2, 3, 7, 6, 5],
                        [6, 3, 4, 6, 2, 1, 8],
                        [7, 3, 1, 8, 3, 2, 4],
                        [1, 5, 7, 9, 4, 2, 3]], [[[1, 1], [3, 3]], [[4, 4], [4, 4]]]) == [38, 4]

    # teste ex10
    def __teste10(self, functie):
        assert functie([[0, 0, 0, 1, 1],
                        [0, 1, 1, 1, 1],
                        [0, 0, 1, 1, 1]]) == 1
        assert functie([[0, 0, 0],
                        [0, 0, 1],
                        [0, 0, 1]]) == 1
        assert functie([[0, 0],
                        [0, 0]]) == -1
        assert functie([[1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 1, 1, 1],
                        [0, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 1, 1]]) == 0
