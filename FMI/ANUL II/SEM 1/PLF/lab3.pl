%pb 13

%selecteaza un element X dintr-o lista si returneaza lista fara X
%selecteaza(X, L, R)
%selecteaza(i, i, o)
%X - elementul selectat
%L - lista
%R - lista fara X
selecteaza(X, [X|Xs], Xs).
selecteaza(X, [Y|Ys], [Y|Zs]) :- selecteaza(X, Ys, Zs).

%verifica daca un element X este membru al unei liste
%membru(X, L)
%membru(i, i)
%X - elementul de verificat
%L - lista de verificat
membru(X, [X|_]).
membru(X, [_|Xs]) :- membru(X, Xs).

%verifica daca o lista L1 este sau se poate lega de o sublista a listei L2
%subset(L1, L2)
%subset(i, i)
%L1 - sublista de verificat
%L2 - lista mare
subset([], _).
subset([X|Xs], Ys) :- membru(X, Ys), subset(Xs, Ys).

%coloreaza o regiune cu o culoare din lista de culori (regiunea este o pereche [tara, Tara, [Vecin1, Vecin2...]])
%coloreazaRegiune(R, C)
%coloreazaRegiune(i, i)
%R - regiune de colorat
%C - lista de culori
coloreazaRegiune([_, Culoare, Vecini], Culori) :-
	selecteaza(Culoare, Culori, CuloriRamase),
	subset(Vecini, CuloriRamase).

%afiseaza o regiune in forma [Nume, Culoare]
%afiseazaRegiune(R, Rez)
%afiseazaRegiune(i, o)
%R - Regiune
%Rez - Rezultat
afiseazaRegiune([Nume, Culoare, _], [Nume, Culoare]).

%coloreaza toata harta (harta este o lista de regiuni) cu culorile din lista de culori
%coloreazaHarta(H, C, R)
%coloreazaHarta(i, i, o)
%H - lista de regiuni (harta)
%C - lista de culori
%R - lista rezultat
coloreazaHarta([], _, []).
coloreazaHarta([Regiune|Regiuni], Culori, [Rezultat1|Rezultat2]) :-
	coloreazaRegiune(Regiune, Culori),
	afiseazaRegiune(Regiune, Rezultat1),
	coloreazaHarta(Regiuni, Culori, Rezultat2).
