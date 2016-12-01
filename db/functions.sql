-- ******************** Stored Functions

-- ******************** user attrs

create or replace function insert_user_attr(bigint, text, text) RETURNS integer as '
DECLARE
BEGIN
insert into user_attrs (user_id, attr_name, attr_value) values($1,$2,$3);
return 1;
END;
' LANGUAGE plpgsql;

create or replace function update_user_attr(bigint, text, text) RETURNS integer as '
DECLARE
BEGIN
update user_attrs set attr_value = $3 where attr_name = $2 and user_id = $1;
return 1;
END;
' LANGUAGE plpgsql;

create or replace function delete_user_attr(bigint, text) RETURNS integer as '
DECLARE
BEGIN
delete from user_attrs where attr_name = $2 and user_id = $1;
return 1;
END;
' LANGUAGE plpgsql;

-- ****************************** Group Attrs

create or replace function insert_group_attr(bigint, text, text) RETURNS integer as '
DECLARE
BEGIN
insert into group_attrs (group_id, attr_name, attr_value) values($1,$2,$3);
return 1;
END;
' LANGUAGE plpgsql;

create or replace function update_group_attr(bigint, text, text) RETURNS integer as '
DECLARE
BEGIN
update group_attrs set attr_value = $3 where attr_name = $2 and group_id = $1;
return 1;
END;
' LANGUAGE plpgsql;

create or replace function delete_group_attr(bigint, text) RETURNS integer as '
DECLARE
BEGIN
delete from group_attrs where attr_name = $2 and group_id = $1;
return 1;
END;
' LANGUAGE plpgsql;
-- ****************************** Normal Users

create or replace function insert_normal_user(bigint, text, text) RETURNS integer as '
DECLARE
BEGIN
insert into normal_users (user_id, normal_username, normal_password) values($1,$2,$3);
return 1;
END;
' LANGUAGE plpgsql;

create or replace function update_normal_user(bigint, text, text) RETURNS integer as '
DECLARE
BEGIN
update normal_users set normal_username = $2, normal_password = $3 where user_id = $1;
return 1;
END;
' LANGUAGE plpgsql;

create or replace function delete_normal_user(bigint) RETURNS integer as '
DECLARE
BEGIN
delete from normal_users where user_id = $1;
return 1;
END;
' LANGUAGE plpgsql;

-- *************************************** Add User
create or replace function add_user(bigint, numeric, integer, integer) RETURNS integer as '
DECLARE
BEGIN
insert into users (user_id, credit, owner_id, group_id) values ($1, $2, $3, $4);
return 1;
END;
' LANGUAGE plpgsql;
-- *************************************** User Audit Log
create or replace function insert_user_audit_log(integer, boolean, bigint, text, text, text) RETURNS integer as '
DECLARE
BEGIN
insert into user_audit_log (admin_id, is_user, object_id, attr_name, old_value, new_value) values ($1, $2, $3, $4, $5, $6);
return 1;
END;
' LANGUAGE plpgsql;
-- *************************************** Connection Log
create or replace function insert_connection_log(bigint, numeric, timestamp without time zone, timestamp without time zone, boolean, smallint, integer, text[], text[]) RETURNS integer as '
DECLARE
    l_user_id alias for $1;
    l_credit_used alias for $2;
    l_login_time alias for $3;
    l_logout_time alias for $4;
    l_successful alias for $5;
    l_service alias for $6;
    l_ras_id alias for $7;
    l_names_array alias for $8;
    l_values_array alias for $9;
    l_connection_log_id integer;
BEGIN
    l_connection_log_id := nextval(''connection_log_id'');
    insert into connection_log (connection_log_id, user_id, credit_used, login_time, logout_time, successful, service, ras_id)
				values
			       (l_connection_log_id, l_user_id, l_credit_used, l_login_time, l_logout_time, l_successful, l_service, l_ras_id);

    FOR i in array_lower(l_names_array,1) .. array_upper(l_names_array,1) LOOP
	insert into connection_log_details (connection_log_id, name, value) 
					    values
					   (l_connection_log_id, l_names_array[i], l_values_array[i]);
    END LOOP;
    return 1;
END;
' LANGUAGE plpgsql;
				
-- *************************************** Change Credit
create or replace function change_user_credit(bigint, numeric) RETURNS integer as '
DECLARE
BEGIN
    update users set credit = credit + $2 where user_id = $1;
return 1;
END;
' LANGUAGE plpgsql;
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
select into quota attr_value::integer 
	    from 
	user_attrs 
	    where 
	attr_name=''mail_quota'' 
	    and exists(
	select email_attr.user_id 
	    from 
	user_attrs as email_attr
	    where 
	user_attrs.user_id=email_attr.user_id 
	    and 
	email_attr.attr_name = ''email_address''
	    and
	email_attr.attr_value = $1); 
	    
IF NOT FOUND THEN
  select into quota attr_value::integer 
	from 
    group_attrs 
	where 
    attr_name=''mail_quota'' 
	and exists(
    select user_attrs.user_id 
	from 
    user_attrs,users 
	where 
    attr_name=''email_address''
	and
    attr_value=$1 
	and 
    user_attrs.user_id=users.user_id 
	and 
    group_attrs.group_id=users.group_id); 
END IF;	
return quota;
END;
' LANGUAGE plpgsql;

create or replace function get_mail_dir(text) RETURNS text as '
DECLARE
  mail_dir text;
BEGIN
select into mail_dir email_attr.attr_value||''/'' from user_attrs as email_attr
					    where 
					email_attr.attr_name = ''email_address''
					    and 
					email_attr.attr_value = $1 
					    and not exists 
					(select user_attrs.user_id 
					    from 
					user_attrs 
					    where 
					user_attrs.user_id=email_attr.user_id 
					    and 
					user_attrs.attr_name=''lock'');
return mail_dir;
END;
' LANGUAGE plpgsql;

--************************************* Web Analyzer
create or replace function insert_web_analyzer_log(timestamp without time zone ,bigint, inet, text, integer, integer, smallint, smallint, smallint, smallint, integer) RETURNS integer as '
DECLARE
    _id bigint;
BEGIN
select into _id nextval(''web_analyzer_log_log_id'');
insert into web_analyzer_log (log_id, _date, user_id, ip_addr, url, elapsed, bytes, miss, hit, successful, failure, _count ) values(_id,$1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11);
return 1;
END;
' LANGUAGE plpgsql;
