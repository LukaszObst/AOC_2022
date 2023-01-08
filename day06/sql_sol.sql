with input_(s) as (
	select 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
),
processed_input_packet(pos, marker) as (
	select level + 3 pos, substr(s, level, 4) marker
	from input_
	connect by level <= LENGTH(s) - 3
),
processed_input_message(pos, marker) as (
	select level + 13 pos, substr(s, level, 14) marker
	from input_
	connect by level <= LENGTH(s) - 13
),
chars_per_marker_packet(pos, marker_char_pos, marker_char) as (
	select pos, level marker_char_pos, substr(marker, level, 1) marker_char
	from processed_input_packet
	connect by prior pos = pos and level <= 4
),
chars_per_marker_message(pos, marker_char_pos, marker_char) as (
	select pos, level marker_char_pos, substr(marker, level, 1) marker_char
	from processed_input_message
	connect by prior pos = pos and level <= 14
),
marker_test as (
	select 'PACKET' type_, l.pos, max(r.pos) is null as marker_possible
	from chars_per_marker_packet l
	left join chars_per_marker_packet r
	on l.pos = r.pos and l.marker_char = r.marker_char and l.marker_char_pos != r.marker_char_pos
	group by 1, 2
	union all
	select 'MESSAGE' type_, l.pos, max(r.pos) is null as marker_possible
	from chars_per_marker_message l
	left join chars_per_marker_message r
	on l.pos = r.pos and l.marker_char = r.marker_char and l.marker_char_pos != r.marker_char_pos
	group by 1, 2
)
select distinct type_, min(pos) over (partition by type_ order by pos)
from marker_test
where marker_possible