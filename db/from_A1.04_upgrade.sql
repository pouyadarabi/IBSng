-- ********************* User Audit Log
create table user_audit_log(
    admin_id integer,
    is_user bool,
    object_id bigint, -- user_id, or group_id
    attr_name text,
    old_value text,
    new_value text,
    change_time timestamp without time zone default CURRENT_TIMESTAMP
);

insert into defs (name,value) VALUES ('USER_AUDIT_LOG','I01
.') ;


insert into ibs_states VALUES ('AUTO_CLEAN_CONNECTION_LOG','0');
insert into ibs_states VALUES ('AUTO_CLEAN_CREDIT_CHANGE','0');
insert into ibs_states VALUES ('AUTO_CLEAN_USER_AUDIT_LOG','0');

create table caller_id_users (
    user_id bigint references users,
    caller_id text unique
);

