-- ***************************** IAS
create table ias_event (
    event_id bigint primary key,
    event_type smallint, -- 1: CHANGE_USER_CREDIT 2: CHANGE_ADMIN_DEPOSIT 3: ADD_USER 4: DELETE_USER 5: ADD_ADMIN 6: DELETE_ADMIN
    event_date timestamp without time zone default CURRENT_TIMESTAMP,
    actor text, -- admin usernme
    amount numeric(12,2),
    destinations text, -- admin username/user_ids separated by ,
    comment text
);

create sequence ias_event_event_id;

create table ias_event_extended(
    event_id bigint references ias_event,
    name text,
    value text,
    primary key(event_id,name)
);

insert into defs (name,value) VALUES ('IAS_ENABLED','I1
.') ;

-- **************************************** IAS New EVENT
create or replace function insert_ias_event(bigint, smallint, text, numeric, text, text) RETURNS integer as '
DECLARE
BEGIN
insert into ias_event (event_id, event_type, actor, amount, destinations, comment) values ($1, $2, $3, $4, $5, $6);
return 1;
END;
' LANGUAGE plpgsql;

-- *************************************** Mail 
create or replace function get_mail_quota(text) RETURNS integer as '
DECLARE
  quota INTEGER;
BEGIN
select into quota attr_value::integer from user_attrs where attr_name=''mail_quota'' and exists(select normal_users.user_id from normal_users where user_attrs.user_id=normal_users.user_id and normal_username = $1); 
IF NOT FOUND THEN
  select into quota attr_value::integer from group_attrs where attr_name=''mail_quota'' and exists(select normal_users.user_id from normal_users,users where normal_username=$1 and normal_users.user_id=users.user_id and  group_attrs.group_id=users.group_id); 
END IF;	
return quota;
END;
' LANGUAGE plpgsql;

create or replace function get_mail_dir(text) RETURNS text as '
DECLARE
  mail_dir text;
BEGIN
select into mail_dir normal_username||''/'' from normal_users where normal_username=$1 and ( exists (select user_attrs.user_id from user_attrs where user_attrs.user_id=normal_users.user_id and user_attrs.attr_name=''mail_quota'') or exists(select group_attrs.group_id from group_attrs,users where group_attrs.attr_name=''mail_quota'' and users.user_id=normal_users.user_id and users.group_id=group_attrs.group_id)) and not exists (select user_attrs.user_id from user_attrs where user_attrs.user_id=normal_users.user_id and user_attrs.attr_name=''lock'');
return mail_dir;
END;
' LANGUAGE plpgsql;


-- *************************************** Persistent lan changes
alter table persistent_lan_users drop CONSTRAINT persistent_lan_users_pkey;
alter table persistent_lan_users drop CONSTRAINT persistent_lan_users_persistent_lan_mac_key;
alter table persistent_lan_users alter persistent_lan_mac set not null;
alter table persistent_lan_users alter persistent_lan_ip set not null;
alter table persistent_lan_users add primary key(persistent_lan_mac,persistent_lan_ip);
