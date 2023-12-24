;a
;==================
;prod(L)
;L - lista initiala
;produsul atomilor numerici dintr-o lista neliniara, de la nivel superficial
(defun prod(l)
  (cond
    ((null l) 0)
    ((and (equal (length l) 1) (numberp (car l)) (car l)))
    ((and (equal (length l) 1) (not (numberp (car l))) 1))
    ((numberp (car l)) (* (car l) (prod (cdr l))))
    (t (prod (cdr l)))
  )
)
;===================
;b
;===================
;formeaza toate perechile formate dintr-un element si elementele unei liste
;pereche(e, L)
;e - element de adaugat la inceput
;L - lista din care se extrag elemente pt perechi
(defun pereche(e l)
  (cond
    ((null l) nil)
    (t (cons (list e (car l)) (pereche e (cdr l))))
  )
)

;returneaza o lista cu toate perechile care se pot forma cu elementele unei liste
;perechi(L)
;L - lista
(defun perechi(l)
  (cond
    ((null l) nil)
    (t (append (pereche (car l) (cdr l)) (perechi (cdr l))))
  )
)
;================
;c
;================
;returneaza rezultatul unei operatii
;operatie(semn, nr1, nr2)
;semn - caracter, operatie
;nr1 - atom, primul operand
;nr2 - atom, al doilea operand
(defun operatie(semn nr1 nr2)
    (cond
        ((equal semn '+) (+ nr1 nr2))
        ((equal semn '*) (* nr1 nr2))
        ((equal semn '-) (- nr1 nr2))
	((equal semn '/) (/ nr1 nr2))
    )
)

;returneaza rezultatul unei expresii din interiorul unei liste
;calculeaza(l)
;l - lista, expresia memorata in preordine
(defun calculeaza(l)
    (cond
        ((equal (cdr l) nil) (car l))
        ((AND (not (numberp (car l))) (numberp (cadr l)) (numberp (caddr l)) ) (cons (operatie (car l) (cadr l) (caddr l))  (cdddr l)  ))
        (t (cons (car l) (calculeaza (cdr l)) ))
    )
)

;returneaza rezultatul expresiei
;expresie_preordine(l)
;l - lista, expresia memorata in preordine
(defun expresie_preordine(l)
    (cond
        ((null (cdr l)) (car l))
        (t (expresie_preordine (calculeaza l) ))
    )
)
;================
;d
;================
;returneaza numarul de aparitii al unui element intr-o lista
;numara(e, L)
;e - element de numarat
;L - lista in care se numara
(defun numara(e l)
  (cond
    ((null l) 0)
    ((equal e (car l)) (+ 1 (numara e (cdr l))))
    (t (numara e (cdr l)))
  )
)

;verifica daca un element apartine unei liste
;exista(e, L)
;e - elementul cautat
;L - lista in care se cauta
(defun exista(e l)
  (cond
    ((null l) nil)
    ((equal e (car l)) t)
    (t (exista e (cdr l)))
  )
)

;returneaza o lista de perechi (atom n), unde atom apare in lista initiala de n ori
;perechi2(L, C)
;L - lista initiala
;C - lista colectoare (se adauga atomii care au fost deja numarati)
(defun perechi2(l c)
  (cond
    ((null l) nil)
    ((exista (car l) c) (perechi2 (cdr l) c))
    (t (cons (list (car l) (numara (car l) l)) (perechi2 (cdr l) (cons (car l) c))))
  )
)

;functia principala, returneaza ce returneaza si perechi2
;perechi2main(L)
;L - lista in care se numara
(defun perechi2main(l)
  (perechi2 l nil)
)
