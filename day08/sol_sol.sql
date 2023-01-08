with input_(s) as (select 
'30373
25512
65332
33549
35390'
),
input_rows(r, row_str) as (
	select level, REGEXP_SUBSTR(s, '.*', 1, level) from input_	connect by REGEXP_SUBSTR(s, '.*', 1, level) is not null
),
all_trees (r, c, h) as (
	select r, level, REGEXP_SUBSTR(row_str, '.', 1, level) from input_rows connect by prior r = r and REGEXP_SUBSTR(row_str, '.', 1, level) is not null
),
tree_visibility as (
	select r, c, h, 
	nvl(h > max(h) over (partition by r order by c rows between 0 preceding and unbounded following exclude current row), true) vis_from_right,
	nvl(h > max(h) over (partition by r order by c rows between unbounded preceding and 0 following exclude current row), true) vis_from_left,
	nvl(h > max(h) over (partition by c order by r rows between unbounded preceding and 0 following exclude current row), true) vis_from_above,
	nvl(h > max(h) over (partition by c order by r rows between 0 preceding and unbounded following exclude current row), true) vis_from_below
	from all_trees
),
visible_trees as (
	select r,c,h from tree_visibility where vis_from_right or vis_from_left or vis_from_above or vis_from_below
),
scenic_trees_from_visible_trees(r,c,h, tree_right_pos, tree_right_higher, tree_left_pos, tree_left_higher, tree_above_pos, tree_above_higher, tree_below_pos, tree_below_higher) as (
	select pos.r, pos.c, pos.h, right_.c, right_.h >= pos.h, left_.c, left_.h >= pos.h, above_.r, above_.h >= pos.h, below_.r, below_.h >= pos.h
	from visible_trees pos
	inner join all_trees right_	on pos.r = right_.r and right_.c > pos.c
	inner join all_trees left_	on pos.r = left_.r  and left_.c  < pos.c
	inner join all_trees above_	on pos.c = above_.c and above_.r < pos.r
	inner join all_trees below_	on pos.c = below_.c and below_.r > pos.r
),
scenic_points_for_visible_trees as (
	select vt.r,vt.c,vt.h, coalesce(min(case when tree_right_higher then abs(tree_right_pos - vt.c) end), count(distinct tree_right_pos), 0) as scenic_points_right,
	coalesce(min(case when tree_left_higher then abs(tree_left_pos - vt.c) end), count(distinct tree_left_pos), 0) as scenic_points_left,
	coalesce(min(case when tree_above_higher then abs(tree_above_pos - vt.r) end), count(distinct tree_above_pos), 0) as scenic_points_above,
	coalesce(min(case when tree_below_higher then abs(tree_below_pos - vt.r) end), count(distinct tree_below_pos), 0) as scenic_points_below,
	local.scenic_points_right * local.scenic_points_left * local.scenic_points_above * local.scenic_points_below as scenic_score
	from visible_trees vt
	left join scenic_trees_from_visible_trees stfvt on vt.r = stfvt.r and vt.c = stfvt.c
	group by vt.r,vt.c,vt.h
	order by vt.r,vt.c
)
select count(*) visible_trees, max(scenic_score) max_scenic_score_for_a_visible_tree
from scenic_points_for_visible_trees