
with input_(s) as (
	select 'vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw'
),
input_lines(group_,  s) as (
	select ceil(level/3) group_, REGEXP_SUBSTR(s, '.*', 1, level)
	from input_
	connect by REGEXP_SUBSTR(s, '.*', 1, level) is not null
),
preprocessed_lines(s, group_, first_comp, second_comp) as (
	select s, group_, SUBSTR(s, 1, LENGTH(s)/2) first_comp, SUBSTR(s, length(s)/2+1, LENGTH(s)) second_comp
	from input_lines
),
transformed_input(s, group_, first_comp, letter_pos_in_comp, first_comp_letter, second_comp, second_comp_letter) as (
	select s, group_, first_comp, level letter_pos_in_comp, SUBSTR(first_comp, level, 1) as first_comp_letter, second_comp, SUBSTR(second_comp, level, 1) second_comp_letter
	from preprocessed_lines pl
	connect by prior s = s and level <= length(pl.first_comp)
),
wrong_assignments_per_rucksack as (
	selecT distinct fc.s, fc.first_comp_letter letter
	from transformed_input fc
	inner join transformed_input sc
	on fc.s = sc.s and fc.first_comp_letter = sc.second_comp_letter
),
transformed_input_part_two as (
	select s, group_, first_comp_letter letter from transformed_input
	union
	select s, group_, second_comp_letter letter from transformed_input
),
wrong_assignments_per_group as (
	select group_, letter from transformed_input_part_two
	group by 1, 2
	having count(*) = 3
),
wrong_assignments_per_rucksack_prios as (
	select s, letter,  26*to_number(upper(letter) = letter) + ascii(lower(letter)) - ascii('a') + 1 prio
	from wrong_assignments_per_rucksack
),
wrong_assignments_per_group_prios as (
	select group_, letter,  26*to_number(upper(letter) = letter) + ascii(lower(letter)) - ascii('a') + 1 prio
	from wrong_assignments_per_group
)
select 'Part one' part, sum(prio) from wrong_assignments_per_rucksack_prios
union all
select 'Part two' part, sum(prio) from wrong_assignments_per_group_prios