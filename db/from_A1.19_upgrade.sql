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

create table internet_bw_snapshot(
    snp_date timestamp without time zone default CURRENT_TIMESTAMP,
    user_id integer references users,
    in_rate integer,
    out_rate integer,
    primary key(snp_date, user_id)
);

create index connection_log_details_name_value_index on connection_log_details(name,value);

delete from web_analyzer_log WHERE _date < now() - interval '2 weeks';
update ibs_states set value = '1209600' where name='AUTO_CLEAN_WEB_ANALYZER_LOG'; -- 14 days

create index web_analyzer_log_date_index on web_analyzer_log(_date);
