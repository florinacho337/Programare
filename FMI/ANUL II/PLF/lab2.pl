%a - sorteaza o lista cu eliminarea dublurilor
%plaseaza(L, E, R)
%plaseaza(i, i, o)
%L - lista initiala
%E - elementul care se plaseaza
%R - lista rezultat
plaseaza([], E, [E]).
plaseaza([H|T], E, [H|R1]) :- E > H, plaseaza(T, E, R1).
plaseaza([H|T], E, [E, H|T]) :- E =< H.

%sorteaza(L, R)
%sorteaza(i, o)
%L - lista initiala
%R - lista sortata fara dubluri
sorteaza([], []).
sorteaza([H|T], R) :- sorteaza(T, R1), plaseaza(R1, H, R).

%b - sa se sorteze fiecare sublista fara pastrarea dublurilor
%sortare_subliste(L, R)
%sotare_subliste(i,o)
%L - lista initiala
%R - lista rezultat
sortare_subliste([], []).
sortare_subliste([H|T], [R|T1]) :- H = [_ |_], sorteaza(H, R), sortare_subliste(T, T1).
sortare_subliste([H|T], [H|T1]) :- H \= [_| _], sortare_subliste(T, T1).
