%a
%intercaleaza(i,i,i,o)
%intercaleaza(L,N,E,R)
%intercaleaza un element pe pozitia n a unei liste de numere intregi
%L - lista
%N - intreg, pozitia unde se intercaleaza elementul E
%E - intreg, elementul de intercalat
%R - lista rezultat
intercaleaza(L, 1, E, [E|L]).
intercaleaza([], N, _, []) :- N > 1; N < 1.
intercaleaza([T|H], N, E, [T|Intercalat]) :- N1 is N-1, intercaleaza(H, N1, E, Intercalat).

%b
%cmmdc(i,i,o)
%cmmdc(A, B, D)
%afla cel mai mic divizor comun dintre doua numere intregi
%A - intreg, primul numar
%B - intreg, al doilea numar
%D - intreg, cel mai mare divizor comun al lui A si B
cmmdc(0, B, B).
cmmdc(A, B, A) :- A==B;B==0.
cmmdc(A, B, Cmmdc) :- A < B, C is B-A, cmmdc(A, C, Cmmdc). 
cmmdc(A, B, Cmmdc) :- A > B, C is A-B, cmmdc(C, A, Cmmdc).

%cmmdc_lista(i,o)
%cmmdc_lista(L, R)
%afla cel mai mic divizor comun al numerelor dintr-o lista
%L - lista
%R - cel mai mare divizor comun al numerelor din lista L
cmmdc_lista([],0).
cmmdc_lista([H], H).
cmmdc_lista([H|T], Cmmdc) :- cmmdc_lista(T, V), cmmdc(H, V, Cmmdc).

%teste - true
test1 :- intercaleaza([], 2, 5, []).
test2 :- intercaleaza([], 1, 6, [6]).
test3 :- intercaleaza([1,2,3,4], 2, 3, [1,3,2,3,4]).
test4 :- cmmdc_lista([], 0).
test5 :- cmmdc_lista([1], 1).
test6 :- cmmdc_lista([14,28,49,70], 7).
test7 :- cmmdc_lista([23,46,57,89,2], 1).
adevarat :- test1,test2,test3,test4,test5,test6,test7.
%teste - false
test8 :- intercaleaza([2,3,6], 5, 7, [2,3,6,7]).
test9 :- cmmdc_lista([2,4,3,5,9,10], 11).
fals :- test8;test9.


