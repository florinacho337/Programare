%stergeAux(L, N, M, R)
%stergeAux(i, i, i, o)
%sterge 1-ul, al 3-lea, al 7-lea ... element din lista L
%L - lista initiala
%N - intreg, pozitia curenta
%M - intreg, pozitia elementului care trebuie sters
%R - lista rezultat
stergeAux([], _, _, []).
stergeAux([_|T], N, N, Rez) :- N1 is N+1, M1 is (N+1) * 2 - 1, !, stergeAux(T, N1, M1, Rez).
stergeAux([H|T], N, M, [H|Rez]) :- N1 is N+1, stergeAux(T, N1, M, Rez).

%sterge(L, R)
%apelul principal al functiei de stergere
%L - lista initiala
%R - lista rezultat
sterge(L, R) :- stergeAux(L, 1, 1, R).
