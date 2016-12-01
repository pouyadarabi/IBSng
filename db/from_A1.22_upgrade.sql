alter table internet_bw_snapshot drop constraint internet_bw_snapshot_pkey;
alter table internet_bw_snapshot add primary key(user_id, snp_date);

create index web_analyzer_log_user_id_index on web_analyzer_log(user_id);