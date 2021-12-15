select id_result_for_task from result_for_task 
	where task_number = {task_number} 
	AND id_oo_parallels_subjects IN 
		(select id_oo_parallels_subjects from oo_parallels_subjects 
			where id_subjects = {id_subjects} AND id_oo_parallels IN 
				(select id_oo_parallels from oo_parallels where parallel = {parallel}))