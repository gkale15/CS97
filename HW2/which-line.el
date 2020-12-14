(defun which-line ()
  "Print the current buffer line number and narrowed line number of point."
  (interactive)
  (let ((start (point-min))
	(n (line-number-at-pos))
	(f (count-lines (point-min) (point-max))))
	
    (if (= start 1)
	(message "Line %d of %d" n f))))
