select sum from 
(select id_students, sum(mark) from result_for_task 
	where id_oo_parallels_subjects in 
	(
		select id_oo_parallels_subjects from oo_parallels_subjects 
		where id_subjects = 5 
		and id_oo_parallels in 
		(
			select id_oo_parallels from oo_parallels 
			where parallel = 4
			and id_oo in 
			(
				select id_oo from oo 
				where id_name_of_the_settlement in 
				(
					select id_name_of_the_settlement from name_of_the_settlement 
					where id_district = 19
				)
			)
		)
	)
group by id_students order by sum) as t1;