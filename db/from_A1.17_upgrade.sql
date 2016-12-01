insert into defs (name,value) VALUES ('TRUSTED_CLIENTS','(lp0
S\'127.0.0.1\'
p1
a.') ;

create index connection_log_login_time_index on connection_log(login_time);

ALTER TABLE tariff_prefix_list add min_chargable_duration smallint;
update tariff_prefix_list set min_chargable_duration=0;
