with test input: regexp is too large

with input_(s) as (
	select '$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k'
),
input_lines(lineno, s) as (
	select level lineno, REGEXP_SUBSTR(s, '.*', 1, level) from input_	connect by REGEXP_SUBSTR(s, '.*', 1, level) is not null
),
line_classification as (
	select lineno, case when substr(s, 1, 1) = '$' then 'COMMAND' when substr(s,1, 3) = 'dir' then 'DIRECTORY' else 'FILE' end as type_, LTRIM(s, '$ ') s
	from input_lines
),
line_infos as (
	select lineno, type_, case type_ when 'FILE' then regexp_substr(s, '^[0-9]+') end as filesize,
	case when type_ in ('FILE', 'DIRECTORY') then regexp_substr(s, '[^ ]+$') else regexp_substr(s, '^[^ ]+') end as name,
	case type_ when 'COMMAND' then regexp_substr(s, '(?<= )[^ ]+$') end as cmd_args, s from line_classification
),
change_dir_chain_infos(lineno, next_cd_lineno, cmd_args) as (
	select li.lineno, lead(lineno) over (order by lineno), li.cmd_args from line_infos li where type_ = 'COMMAND' and name = 'cd'
),
cd_translated as (
	select lineno,next_cd_lineno, cmd_args,	substr(SYS_CONNECT_BY_PATH(cmd_args, '/'), 3) current_dir from change_dir_chain_infos
	start with lineno = (select min(lineno) from change_dir_chain_infos) connect by prior next_cd_lineno = lineno
),
count_backtracks_pre(no_of_backtracks) as (select LENGTH(current_dir) - LENGTH(REPLACE(current_dir, '..', 'x')) from cd_translated),
count_max_backtracks(no_of_backtracks) as (select max(no_of_backtracks) from count_backtracks_pre),
dir_regexp_base(s) as (values '/[^/]', '/\.\.'),
dir_regexp_base_joined(s, no_of_backtracks) as (select * from dir_regexp_base cross join count_max_backtracks),
irregular_to_regular(level_, s) as (select level, SYS_CONNECT_BY_PATH(s, '') from dir_regexp_base_joined connect by prior s = s and level <= no_of_backtracks),
preagg_regexp(level_, s) as (select level_, GROUP_CONCAT(s separator '') from irregular_to_regular group by level_),
dir_regexp(r) as (select '(' || GROUP_CONCAT(s order by level_ separator '|') || ')' from preagg_regexp),
cd_translated_and_resolved as (select ct.lineno, ct.next_cd_lineno, ct.current_dir, REGEXP_REPLACE(current_dir, r.r) current_dir_path_resolved, 
	nvl(regexp_substr(local.current_dir_path_resolved, '[^/]+$'), '/') current_dir_resolved from cd_translated ct cross join dir_regexp r),
dir_hier_flat as (select distinct nvl(regexp_substr(current_dir_path_resolved, '[^/]+(?=/[^/]+$)'), '/') parent, 
	nvl(regexp_substr(current_dir_path_resolved, '[^/]$'), '/') child from cd_translated_and_resolved
	union all
	select name, name From line_infos where type_ = 'DIRECTORY'),
dir_hier_pre as (select CONNECT_BY_ROOT parent as root, nvl(parent, '/') parent, child from dir_hier_FLAT where child != '/' connect by nocycle prior child = parent),
dir_hier as (select distinct root, child from dir_hier_pre),
dir_sizes(dir, size_) as (
	select nvl(dh.root, '/'), sum(li.filesize)
	from line_infos li
	inner join cd_translated_and_resolved ct
	on li.lineno >= ct.lineno and li.lineno < coalesce(ct.next_cd_lineno, li.lineno+1)
	left join dir_hier dh
	on ct.current_dir_resolved = dh.child
	where type_ = 'FILE'
	group by 1
)
select sum(size_) from DIR_SIZES
where size_ <= 100000