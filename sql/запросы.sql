SELECT value, COUNT(value) FROM
	(SELECT id_students,sum_marks,
       		CASE WHEN sum_marks<mark_three THEN 2
            	WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
	    		WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
	    		WHEN sum_marks>=mark_five THEN 5
            	ELSE 0
       		END AS value
    		FROM (SELECT id_students, sum_marks, mark_three, mark_four, mark_five  
			FROM (SELECT id_students, id_oo_parallels_subjects, SUM(mark) as sum_marks 
				FROM result_for_task 
				WHERE id_oo_parallels_subjects = 7364 AND id_oo_parallels = 1068
				GROUP BY id_students, id_oo_parallels_subjects) AS t1
			LEFT JOIN 
				(SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five 
				FROM oo_parallels_subjects 
				WHERE id_oo_parallels_subjects = 7364) AS t2
				USING (id_oo_parallels_subjects)) AS t3)
	AS t4 GROUP BY value;


SELECT result, COUNT(result) FROM
	(SELECT id_students,
	CASE WHEN mark_for_vpr<mark_for_last_semester THEN 'понизил'
    	WHEN mark_for_vpr>mark_for_last_semester THEN 'повысил'
		WHEN mark_for_vpr=mark_for_last_semester THEN 'подтвердил'
    END AS result
    FROM (SELECT id_students,sum_marks, mark_for_last_semester,
		CASE WHEN sum_marks<mark_three THEN 2
    	WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
		WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
		WHEN sum_marks>=mark_five THEN 5
    	ELSE 0
		END AS mark_for_vpr
	FROM (SELECT id_students, sum_marks, mark_three, mark_four, mark_five, mark_for_last_semester  
	FROM (SELECT id_students, id_oo_parallels_subjects, mark_for_last_semester, SUM(mark) as sum_marks 
		FROM result_for_task 
		WHERE id_oo_parallels_subjects = 7364 AND id_oo_parallels = 1068
		GROUP BY id_students, id_oo_parallels_subjects, mark_for_last_semester) AS t1
	LEFT JOIN 
		(SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five 
		FROM oo_parallels_subjects 
		WHERE id_oo_parallels_subjects = 7364) AS t2
		USING (id_oo_parallels_subjects)) AS t3) AS t4) AS t5 GROUP BY result;