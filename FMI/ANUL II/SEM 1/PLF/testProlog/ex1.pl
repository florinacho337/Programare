%Sa se scrie un predicat care intoarce diferenta a doua multimi.

membru(E, [E|_]).
membru(E, [_|T]) :- membru(E, T).

diferenta([], _, []).
diferenta([H|T], L, Rez) :- membru(H, L), !, diferenta(T, L, Rez).
diferenta([H|T], L, [H|Rez]) :- diferenta(T, L, Rez).

%Sa se scrie un predicat care adauga intr-o lista dupa fiecare element par valoarea 1

adaugaUnu([], []).
adaugaUnu([H|T], [H,1|Rez]) :- H mod 2 =:= 0, adaugaUnu(T, Rez).
adaugaUnu([H|T], [H|Rez]) :- H mod 2 =\= 0, adaugaUnu(T, Rez).

%Sa se scrie un predicat care determina cel mai mic multiplu comun al elementelor unei liste formate din nr intregi

cmmmc(_, _, N, N, N).
cmmmc(A, B, N, M, Rez) :- N < M, N1 is N+A, cmmmc(A, B, N1, M, Rez).
cmmmc(A, B, N, M, Rez) :- N > M, M1 is M+B, cmmmc(A, B, N, M1, Rez).

cmmmc_lista([], 0).
cmmmc_lista([E], E).
cmmmc_lista([H|T], Rez) :- cmmmc_lista(T, Rez1), !, cmmmc(H, Rez1, H, Rez1, Rez).

%Sa se scrie un predicat care adauga dupa 1-ul, al 2-lea, al 4-lea, al 8-lea... element al unei liste o valoare v data

adaugaValoare([], _, _, _, []).
adaugaValoare([H|T], V, N, M, [H|Rez]) :- N =\= M, N1 is N+1, adaugaValoare(T, V, N1, M, Rez).
adaugaValoare([H|T], V, N, N, [H, V|Rez]) :- N1 is N+1, M1 is N*2, adaugaValoare(T, V, N1, M1, Rez).

adaugaPrincipal(L, V, R) :- adaugaValoare(L, V, 1, 1, R).

%Sa se scrie un predicat care transforma o lista intr-o multime, in ordinea primei aparitii. [1,2,3,1,2] -> [1,2,3]
%Se va folosi functia membru de la prima problema!!!

transformaLista([], _, []).
transformaLista([H|T], L, Rez) :- membru(H, L), !, transformaLista(T, L, Rez).
transformaLista([H|T], L, [H|Rez]) :- transformaLista(T, [H|L], Rez).

transformaPrincipal(L, R) :- transformaLista(L, [], R).

%Sa se scrie o functie care descompune o lista de numere intr-o lista de forma [lista-nr-pare lista-nr-imp]
%si va intoarce si numarul de elemente pare si impare

creeazaListaSiNumara([], _, 0, []).
creeazaListaSiNumara([H|T], C, N1, [H|Rez]) :- H mod 2 =:= C, !, creeazaListaSiNumara(T, C, N, Rez), N1 is N+1.
creeazaListaSiNumara([_|T], C, N, Rez) :- creeazaListaSiNumara(T, C, N, Rez).

descompuneLista(L, P, I, [R1|[R2]]) :- creeazaListaSiNumara(L, 0, P, R1), creeazaListaSiNumara(L, 1, I, R2).

%Sa se scrie un predicat care substituie intr-o lista un element printr-o alta lista (sau un element prin altul
%daca L este element)

substituieElement([], _, _, []).
substituieElement([H|T], H, L, [L|R]) :- substituieElement(T, H, L, R).
substituieElement([H|T], E, L, [H|R]) :- H =\= E, substituieElement(T, E, L, R).

%Sa se elimine elementul de pe pozitia a n-a a unei liste liniare

eliminaElement([], _, []).
eliminaElement([_|T], 1, T) :- !.
eliminaElement([H|T], N, [H|Rez]) :- N1 is N-1, eliminaElement(T, N1, Rez).

%Sa se scrie un predicat care elimina toate aparitiile unui atom dintr-o lista

eliminaAtom([], _, []).
eliminaAtom([H|T], H, Rez) :- !, eliminaAtom(T, H, Rez).
eliminaAtom([H|T], E, [H|Rez]) :- eliminaAtom(T, E, Rez).

%Definiti un predicat care, dintr-o lista de atomi, produce o lista de perechi %(atom n), unde atom apare de n ori in lista initiala. numar([1,2,1,2,1,3,1], X) %-> X = [[1, 4], [2, 2], [3, 1]] 
%Se va folosi functia membru de la prima problema!!!

nrAparitii([], _, 0).
nrAparitii([H|T], H, Rez) :- !, nrAparitii(T, H, Rez1), Rez is Rez1+1.
nrAparitii([_|T], E, Rez) :- nrAparitii(T, E, Rez).

numarAux([], _, []).
numarAux([H|T], C, Rez) :- membru(H, C), !, numarAux(T, C, Rez).
numarAux([H|T], C, [[H, N]|Rez]) :- nrAparitii(T, H, N1), N is N1+1, numarAux(T, [H|C], Rez).

numar(L, R) :- numarAux(L, [], R).

%Sa se scrie un predicat care elimina intr-o lista toate numerele care se repeta

eliminaRepetateAux([], _, []).
eliminaRepetateAux([H|T], L, [H|Rez]) :- nrAparitii(H, L, 1), !, eliminaRepetateAux(T, L, Rez). 
eliminaRepetateAux([_|T], L, Rez) :- eliminaRepetateAux(T, L, Rez).

eliminaRepetate(L, R) :- eliminaRepetateAux(L, L, R).

%Sa se elimine toate aparitiile elementului maxim dintr-o lista de nr intregi
%Se va folosi functia eliminaAtom(Lista, Atom, Rez)!!!

maxim([], 0).
maxim([E], E).
maxim([H|T], H) :- maxim(T, R), H > R.
maxim([H|T], R) :- maxim(T, R), !, H =< R.

eliminaMaxim(L, R) :- maxim(L, M), eliminaAtom(L, M, R).

%Sa se scrie un predicat care intoarce reuniunea a doua multimi
%Se foloseste functia membru(Element, Lista)

reuniune(L, [], L).
reuniune(L, [H|T], R) :- membru(H, L), !, reuniune(T, L, R).
reuniune(L, [H|T], [H|R]) :- reuniune(T, L, R).

%Sa se scrie un predicat care, primind o lista, intoarce multimea tuturor
%perechilor din lista. [a,b,c,d] -> [[a,b], [a,c], [a,d], [b,c], [b,d], [c,d]]

formeazaPerechi(_, [], [], []).
formeazaPerechi(E, [E1], [H|T], [[E, E1]|R]) :- formeazaPerechi(H, T, T, R).
formeazaPerechi(E, [H|T], L, [[E,H]|Rez]) :- formeazaPerechi(E, T, L, Rez).

perechi([H|T], R) :- formeazaPerechi(H, T, T, R).

%Sa se scrie un predicat care testeaza daca o lista e multime
%Se va folosi nrAparitii(Lista, Elem, Rez)

testeazaMultime([_]).
testeazaMultime([H|T]) :- nrAparitii(T, H, R), R =:= 0, testeazaMultime(T).

%Sa se scrie un predicat care elimina primele 3 aparitii ale unui element
%intr-o lista. Daca elementul apare mai putin de 3 ori, se va elimina de cate
%ori apare

eliminaDeNOri([], _, _, []).
eliminaDeNOri([H|T], H, 1, T) :- !.
eliminaDeNOri([H|T], H, N, Rez) :- !, N1 is N-1, eliminaDeNOri(T, H, N1, Rez).
eliminaDeNOri([H|T], E, N, [H|Rez]) :- eliminaDeNOri(T, E, N, Rez).

eliminaDeTreiOri(L, E, Rez) :- eliminaDeNOri(L, E, 3, Rez).

%Sa se scrie un predicat care intoarce intersectia a doua multimi
%Se va folosi functia membru(Elem, Lista)

intersectie(_, [], []).
intersectie(L, [H|T], [H|R]) :- membru(H, L), !, intersectie(T, L, R).
intersectie(L, [_|T], R) :- intersectie(T, L, R).

%Sa se construiasca lista (m, ..., n), adica multimea numerelor intregi din
%intervalul [M,N]

adaugaElemente(M, M, [M]) :- !.
adaugaElemente(M, N, [M|Rez]) :- M1 is M+1, adaugaElemente(M1, N, Rez).

%Sa se construiasca sublista (lm,..,ln) a listei (l1,..,lk)

construiesteSublista([H|_], _, N, N, [H]).
construiesteSublista([_|T], M, N, V, R) :- V < M, V1 is V+1, construiesteSublista(T, M, N, V1, R).
construiesteSublista([H|T], M, N, V, [H|R]) :- V >= M, V1 is V+1, construiesteSublista(T, M, N, V1, R).

%Sa se scrie un predicat care transforma o lista intr-o multime, in ordinea ultimei aparitii.
%[1,2,3,1,2] -> [3,1,2]
%Se va folosi functia nrAparitii(Lista, Elem, Rez)

transformaLista2([], []).
transformaLista2([H|T], [H|R]) :- nrAparitii(T, H, 0), !, transformaLista2(T, R).
transformaLista2([_|T], R) :- transformaLista2(T, R).

%Sa se scrie un predicat care verifica daca o lista formata din nr intregi are aspect de vale

vale([_], 0).
vale([H1, H2|T], 1) :- H1>H2, vale([H2|T], 1).
vale([H1, H2|T], _) :- H1<H2, vale([H2|T], 0).

valePrincipal([H1, H2|T]) :- H1>H2, vale([H1,H2|T], 1).

%Sa se calculeza suma alternanta a elementelor unei liste

insumeaza([], _, R, R).
insumeaza([H|T], 1, C, R) :- C1 is C-H, insumeaza(T, 0, C1, R).
insumeaza([H|T], 0, C, R) :- C1 is C+H, insumeaza(T, 1, C1, R).

sumaAlternanta(L, R) :- insumeaza(L, 0, 0, R).

%Sa se scrie un predicat care testeaza egalitatea a doua multimi, fara sa se faca apel la
%diferenta a doua multimi. Se va folosi nrAparitii(Lista, Elem, Rez) si membru(Elem, Lista)

testeazaMultimiAux([], _, _).
testeazaMultimiAux([H|T], L, M) :- membru(H, M), !, nrAparitii(L, H, R1), nrAparitii(M, H, R2), R1 =:= R2, testeazaMultimiAux(T, L, M).

testeazaMultimi(M1, M2) :- testeazaMultimiAux(M1, M1, M2).

%Sa se scrie un predicat care se va satisface daca o lista are numar par de elemente si va esua
%in caz contrar, fara sa se numere elementele listei

parAux([], 0).
parAux([_|T], 1) :- parAux(T, 0).
parAux([_|T], 0) :- parAux(T, 1).

par(L) :- parAux(L, 0).

%Definiti un predicat care determina suma a doua numere scrise in reprezentare de lista

lungime([], 0).
lungime([_|T], R) :- lungime(T, R1), R is R1+1.

sumaNR([], [], 0, []).
sumaNR([], [], 1, [1]).
sumaNR([H|T], [], C, [H1|R]) :- 
	H1 is (H+C) mod 10,
	C1 is (H+C) div 10,
       	sumaNR(T, [], C1, R).
sumaNR([H1|T1], [H2|T2], C, [H3|Rez]) :- 
	H3 is (H1+H2+C) mod 10, 
	C1 is (H1+H2+C) div 10, 
	sumaNR(T1, T2, C1, Rez).
sumaNR([H1|T1], [H2|T2], C, [H3|Rez]) :- 
	H3 is (H1+H2+C) mod 10, 
	C1 is (H1+H2+C) div 10, 
	sumaNR(T1, T2, C1, Rez).

inverseazaLista([], C, C).
inverseazaLista([H|T], C, R) :- inverseazaLista(T, [H|C], R).

sumaNRMain(L1, L2, R) :- 
	lungime(L1, R1), 
	lungime(L2, R2), R1>=R2,
	inverseazaLista(L1, [], IL1),	
	inverseazaLista(L2, [], IL2), 
	sumaNR(IL1, IL2, 0, IR), !,
	inverseazaLista(IR, [], R).
sumaNRMain(L1, L2, R) :-
	inverseazaLista(L1, [], IL1), 
        inverseazaLista(L2, [], IL2), 
        sumaNR(IL2, IL1, 0, IR), !,
        inverseazaLista(IR, [], R).

%Sa se interclaseze fara pastrarea dublurilor doua liste sortate

interclaseaza(L1, [], L1).
interclaseaza([], L2, L2).
interclaseaza([H1|T1], [H2|T2], [H1|R]) :- H1 < H2, interclaseaza(T1, [H2|T2], R).
interclaseaza([H1|T1], [H2|T2], [H2|R]) :- H1 > H2, interclaseaza([H1|T1], T2, R).
interclaseaza([H1|T1], [H2|T2], [H1|R]) :- H1 =:= H2, interclaseaza(T1, T2, R).

%Definiti un predicat care determina produsul unui numar reprezentat cifra cu cifra intr-o lista cu o anumita cifra

inmultireNRAux([], _, 0, []).
inmultireNRAux([], _, C, [C]).
inmultireNRAux([H|T], N, C, [H1|R]) :-
	H1 is (H * N + C) mod 10,
	C1 is (H * N + C) div 10,
	inmultireNRAux(T, N, C1, R).

inmultireNR(L1, N, R) :- 
	inverseazaLista(L1, [], IL1),
	inmultireNRAux(IL1, N, 0, IR), !,
	inverseazaLista(IR, [], R).

%Dandu-se o lista liniara numerica, sa se stearga toate secventele de valori consecutive

sterg([], []).
sterg([A,B], []) :- A =:= B-1.
sterg([E], [E]).
sterg([H1, H2, H3|T], R) :-
	H1 =:= H2-1,
	H2 =:= H3-1,
	sterg([H2, H3|T], R).
sterg([H1, H2, H3|T], R) :-
	H1 =:= H2-1,
	H2 =\= H3-1,
	sterg([H3|T], R).
sterg([H1, H2|T], [H1|R]) :-
	H1 =\= H2-1,
	sterg([H2|T], R).

%Verifica nr este prim

nrDivizoriAux(N, M, 0) :- M is N div 2 + 1, !.
nrDivizoriAux(N, M, R) :- N mod M =:= 0, M1 is M+1, nrDivizoriAux(N, M1, R1), R is R1 + 1.
nrDivizoriAux(N, M, R) :- N mod M =\= 0, M1 is M+1, nrDivizoriAux(N, M1, R).

prim(N) :- nrDivizoriAux(N, 2, R), R = 0.

%Sa se deteremine cea mai lunga secventa de nr pare consecutive dintr-o lista

%ceaMaiLungaSecv(Lista, Precedent, Contor, Maxim, Lista_curenta, Lista_maxima, Rez)
ceaMaiLungaSecv([], _, _, _, _, Lista_MAX, Lista_MAX).
ceaMaiLungaSecv([], Precedent, _, _, Rez, _, Rez) :- Precedent =\= -1.
ceaMaiLungaSecv([H|T], -1, Contor, Maxim, Lista_curenta, Lista_MAX, Rez) :-
	H mod 2 =:= 0,
	Contor1 is Contor+1,
	ceaMaiLungaSecv(T, H, Contor1, Maxim, [H|Lista_curenta], Lista_MAX, Rez).
ceaMaiLungaSecv([H|T], -1, Contor, Maxim, Lista_curenta, Lista_MAX, Rez) :-
	H mod 2 =:= 1,
	ceaMaiLungaSecv(T, -1, Contor, Maxim, Lista_curenta, Lista_MAX, Rez).
ceaMaiLungaSecv([H|T], Precedent, Contor, Maxim, Lista_curenta, Lista_MAX, Rez) :-
	H =:= Precedent+2,
	H mod 2 =:= 0,
	Contor1 is Contor+1,
	ceaMaiLungaSecv(T, H, Contor1, Maxim, [H|Lista_curenta], Lista_MAX, Rez).
ceaMaiLungaSecv([H|T], _, Contor, Maxim, Lista_curenta, _, Rez) :-
        H mod 2 =:= 1,
	Contor > Maxim,
        ceaMaiLungaSecv(T, -1, 0, Contor, [], Lista_curenta, Rez).
ceaMaiLungaSecv([H|T], _, Contor, Maxim, _, Lista_MAX, Rez) :-
        H mod 2 =:= 1,
        Contor =< Maxim,
        ceaMaiLungaSecv(T, -1, 0, Maxim, [], Lista_MAX, Rez).
ceaMaiLungaSecv([H|T], Precedent, Contor, Maxim, Lista_curenta, _, Rez) :-
        H =\= Precedent+2,
        H mod 2 =:= 0,
        Contor > Maxim,
        ceaMaiLungaSecv(T, -1, 1, Contor, [], Lista_curenta, Rez).
ceaMaiLungaSecv([H|T], Precedent, Contor, Maxim, _, Lista_MAX, Rez) :-
        H =\= Precedent+2,
        H mod 2 =:= 0,
        Contor =< Maxim,
        ceaMaiLungaSecv(T, -1, 1, Maxim, [], Lista_MAX, Rez).

ceaMaiLungaSecvPrincipal(L, R) :- ceaMaiLungaSecv(L, -1, 0, 0, [], [], IR), inverseazaLista(IR, [], R).
