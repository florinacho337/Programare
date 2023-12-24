;drum(ab, sub, x, l)
;ab - lista, arbore initial
;sub - lista, subarbore de parcurs, sublista a lui ab
;x - nod dat
;l - lista, drumul de la varf la nodul x
;drumul de la varf la un nod sub forma de lista
(defun drum(ab sub x l)
  (cond
    ((equal (car ab) (car l)) l)
    ((equal (car sub) x) (drum ab ab x (cons x l)))
    ((and (equal (cdr sub) nil) (not (equal (car sub) x))) nil)
    ((and (not (equal (car l) nil)) (or (equal (caadr sub) (car l)) (equal (caaddr sub) (car l)))) (drum ab ab x (cons (car sub) l)))
    (t (or (drum ab (cadr sub) x l) (drum ab (caddr sub) x l)))
  )
)

;drum_main(ab, x)
;ab - lista, arbore initial
;x - nod dat
;drumul de la varful lui ab la nodul x sub forma de lista
(defun drum_main(ab x)
  (drum ab ab x nil)
)





;TESTE
;(drum_main '(A (B) (C (D) (E))) 'E)
;(drum_main '(A (B () (F)) (C (D) (E))) 'D)
;(drum_main '(A (B () (F)) (C (D) (E))) 'F)
;(drum_main '(A (B () (F (G))) (C (D) (E))) 'G)
;(drum_main '(A (B (F) ()) (C (D) (E))) 'E)

