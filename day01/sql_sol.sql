with input_(s) as (
	select '1000
2000
3000

4000

5000
6000

7000
8000
9000

10000'
	from dual
),
input_for_each_elf(elf_number, s) as (
	select row_number() over (order by 1) elf_number, REGEXP_SUBSTR(REGEXP_SUBSTR(s, '(*CRLF)(?s).*?((\r?\n){2}|$)', 1, level), '(?s).*?(?=(\r?\n){2}|$)')
	from input_
	connect by REGEXP_SUBSTR(s, '(*CRLF)(?s).*?((\r?\n){2}|$)', 1, level) is not null 
),
arr_for_each_elf(elf_number, val) as (
	select elf_number, REGEXP_SUBSTR(s, '.*', 1, level)
	from input_for_each_elf
	connect by prior s = s and REGEXP_SUBSTR(s, '.*', 1, level) is not null 
),
agg_for_each_elf(val) as (
	select sum(val) From arr_for_each_elf
	group by elf_number 
),
top_three_elves_by_val(val) as (
	select val
	from agg_for_each_elf
	order by val desc
	limit 3
)
select max(val) sol_part_one, sum(val) sol_part_two
from top_three_elves_by_val