# для всех муниципалитетов
SELECT task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, COUNT(value) FROM
(SELECT task_number,task_number_from_kim, fgos, poop_noo, mark, max_mark, 
    CASE WHEN mark = max_mark THEN 'Выполнили'
        ELSE 'Не выполнили'
    END AS value FROM
(SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number_from_kim, fgos, poop_noo, id_result_for_task, task_number, mark, max_mark FROM 
(SELECT id_distributio_of_tasks_by_positions_of_codifiers, id_result_for_task, task_number, mark FROM
	(SELECT id_result_for_task, task_number, mark FROM result_for_task 
	    WHERE id_oo_parallels_subjects IN 
	        (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
	            WHERE id_oo_parallels IN 
	                (SELECT id_oo_parallels FROM oo_parallels 
	                    WHERE parallel=4 AND id_oo in 
	                        (SELECT id_oo FROM oo 
	                            WHERE year='2021'))
	            AND id_subjects=5) GROUP BY id_result_for_task, id_students, task_number, mark) AS T1

	LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers, id_result_for_task FROM result_for_task_distributio_of_tasks_by_positions_of_codifiers WHERE id_subjects = 5 AND parallel = 4) AS T2
		USING (id_result_for_task) ORDER BY task_number) AS T4

LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers,task_number_from_kim, fgos, poop_noo, max_mark FROM distributio_of_tasks_by_positions_of_codifiers) AS T3
	USING(id_distributio_of_tasks_by_positions_of_codifiers)) AS T5) AS Res group by task_number, task_number_from_kim, fgos, poop_noo, max_mark, value;


# для муниципалитета
SELECT task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, COUNT(value) FROM
(SELECT task_number,task_number_from_kim, fgos, poop_noo, mark, max_mark, 
    CASE WHEN mark = max_mark THEN 'Выполнили'
        ELSE 'Не выполнили'
    END AS value FROM
(SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number_from_kim, fgos, poop_noo, id_result_for_task, task_number, mark, max_mark FROM 
(SELECT id_distributio_of_tasks_by_positions_of_codifiers, id_result_for_task, task_number, mark FROM
	(SELECT id_result_for_task, task_number, mark FROM result_for_task 
	    WHERE id_oo_parallels_subjects IN 
	        (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
	            WHERE id_oo_parallels IN 
	                (SELECT id_oo_parallels FROM oo_parallels 
	                    WHERE parallel=4 AND id_oo in 
	                        (SELECT id_oo FROM oo 
	                            WHERE year='2021'
	                            AND id_name_of_the_settlement in (SELECT id_name_of_the_settlement FROM name_of_the_settlement WHERE id_district = 6)))
	            AND id_subjects=5) GROUP BY id_result_for_task, id_students, task_number, mark) AS T1

	LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers, id_result_for_task FROM result_for_task_distributio_of_tasks_by_positions_of_codifiers WHERE id_subjects = 5 AND parallel = 4) AS T2
		USING (id_result_for_task) ORDER BY task_number) AS T4

LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers,task_number_from_kim, fgos, poop_noo, max_mark FROM distributio_of_tasks_by_positions_of_codifiers) AS T3
	USING(id_distributio_of_tasks_by_positions_of_codifiers)) AS T5) AS Res group by task_number, task_number_from_kim, fgos, poop_noo, max_mark, value;

# Для ОО
SELECT task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, COUNT(value) FROM
(SELECT task_number,task_number_from_kim, fgos, poop_noo, mark, max_mark, 
    CASE WHEN mark = max_mark THEN 'Выполнили'
        ELSE 'Не выполнили'
    END AS value FROM
(SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number_from_kim, fgos, poop_noo, id_result_for_task, task_number, mark, max_mark FROM 
(SELECT id_distributio_of_tasks_by_positions_of_codifiers, id_result_for_task, task_number, mark FROM
	(SELECT id_result_for_task, task_number, mark FROM result_for_task 
	    WHERE id_oo_parallels_subjects = 6255
	         GROUP BY id_result_for_task, id_students, task_number, mark) AS T1

	LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers, id_result_for_task FROM result_for_task_distributio_of_tasks_by_positions_of_codifiers 
			WHERE id_subjects IN (SELECT id_subjects FROM oo_parallels_subjects WHERE id_oo_parallels_subjects = 6255)
			 AND parallel IN (SELECT parallel FROM oo_parallels WHERE id_oo_parallels IN (SELECT id_oo_parallels FROM oo_parallels_subjects WHERE id_oo_parallels_subjects = 6255))) AS T2
		USING (id_result_for_task) ORDER BY task_number) AS T4
 
LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers,task_number_from_kim, fgos, poop_noo, max_mark FROM distributio_of_tasks_by_positions_of_codifiers) AS T3
	USING(id_distributio_of_tasks_by_positions_of_codifiers)) AS T5) AS Res group by task_number, task_number_from_kim, fgos, poop_noo, max_mark, value;

SELECT task_number_from_kim FROM distributio_of_tasks_by_positions_of_codifiers WHERE id_subjects = 5 AND parallel = 4;

SELECT task_number_from_kim FROM distributio_of_tasks_by_positions_of_codifiers 
	WHERE id_subjects IN 
		(SELECT id_subjects FROM oo_parallels_subjects WHERE id_oo_parallels_subjects = 6255)
	AND parallel IN (SELECT parallel FROM oo_parallels WHERE id_oo_parallels IN (SELECT id_oo_parallels FROM oo_parallels_subjects WHERE id_oo_parallels_subjects = 6255));