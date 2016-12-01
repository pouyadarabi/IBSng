--********************* Snap Shots
create table internet_onlines_snapshot(
    snp_date timestamp without time zone default CURRENT_TIMESTAMP,
    ras_id integer,
    value integer
);


create table voip_onlines_snapshot(
    snp_date timestamp without time zone default CURRENT_TIMESTAMP,
    ras_id integer,
    value integer
);

insert into ibs_states VALUES ('AUTO_CLEAN_SNAPSHOTS','0');


create index normal_users_user_id on normal_users (user_id);
create index persistent_lan_user_id on persistent_lan_users (user_id);
create index voip_users_user_id on voip_users (user_id);
create index caller_id_users_user_id on caller_id_users (user_id);
