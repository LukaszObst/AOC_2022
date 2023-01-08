
with input_(s) as (
	select  'B X
C Y
A X'
),
input_lines(s) as (
	select REGEXP_SUBSTR(s, '.*', 1, level)
	from input_
	connect by REGEXP_SUBSTR(s, '.*', 1, level) is not null
),
processed_input(opponent, col_two) as (
	select REGEXP_SUBSTR(s, '.') as opponent, REGEXP_SUBSTR(s, '.$') as col_two from input_lines
),
translation_rules_for_part_two(opponent, action_, me) as (
	values (0,0,2), (0,1,0), (0,2,1), (1,0,0), (1,1,1), (1,2,2), (2,0,1), (2,1,2), (2,2,0)
),
translated_input_into_numbers(opponent, me_part_one, action_part_two, me_part_two) as (
	select ascii(pi_.opponent) - ascii('A') as opponent, ascii(pi_.col_two) - ascii('X') as me_part_one, local.me_part_one as action_part_two, r.me as me_part_two
	from processed_input pi_
	left join translation_rules_for_part_two r
	on (ascii(pi_.opponent) - ascii('A')) = r.opponent and (ascii(pi_.col_two) - ascii('X')) = r.action_
),
rules_for_outcome_points(opponent, me, points) as (
	values (0,0,3), (1,1,3), (2,2,3), (0,1,6), (1,2,6), (2,0,6)
),
calculated_points as (
	select shapes.opponent, shapes.me_part_one,
		shapes.me_part_one + 1 as points_for_shape_part_one, nvl(r_part_one.points , 0) points_for_outcome_part_one, 
			local.points_for_shape_part_one + local.points_for_outcome_part_one as total_points_part_one,
		shapes.opponent opponent_part_two, shapes.action_part_two, shapes.me_part_two, 
		shapes.me_part_two + 1 as points_for_shape_part_two, nvl(r_part_two.points , 0) points_for_outcome_part_two, 
			local.points_for_shape_part_two + local.points_for_outcome_part_two as total_points_part_two
	from translated_input_into_numbers shapes
	left join rules_for_outcome_points r_part_one
		on shapes.opponent = r_part_one.opponent and shapes.me_part_one = r_part_one.me
	left join rules_for_outcome_points r_part_two
		on shapes.opponent = r_part_two.opponent and shapes.me_part_two = r_part_two.me
)
select sum(total_points_part_one) total_points_part_one,  sum(total_points_part_two) total_points_part_two
from calculated_points

with test_(x) as (
	values 'a', 'z', 'A', 'Z'
)
select x,  26*to_number(upper(x) = x) + ascii(LOWER(x)) - ascii('a') + 1
from test_
