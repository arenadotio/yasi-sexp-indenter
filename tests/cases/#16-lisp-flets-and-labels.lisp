(labels ((fact2x (x)
           (fact (* 2 x)))
         (fact (x)
           (if (< x 2) 1 (* x (fact (1- x))))))
  (format t "Twice factorial: ~D" (fact2x 3)))

(defun example (y l)
  (flet ((attach (x)
           (setq l (append l (list x)))))
    (declare (inline attach))
    (dolist (x y)
      (unless (null (cdr x))
        (attach x)))
    l))
