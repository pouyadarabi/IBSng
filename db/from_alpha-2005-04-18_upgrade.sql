create table admin_deposit_change(
    admin_deposit_change_id integer primary key,    
    admin_id integer ,
    to_admin_id integer,
    deposit_change numeric(12,2),
    change_time timestamp without time zone default CURRENT_TIMESTAMP,
    remote_addr inet,
    comment text
);
create sequence admin_deposit_change_id;
