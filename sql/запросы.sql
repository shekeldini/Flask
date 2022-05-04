select count(*) from students 
where id_oo_parallels in 
(
    select id_oo_parallels from oo_parallels 
    where id_oo in 
    (
        select id_oo from oo 
        where year = '2022'
    )
);