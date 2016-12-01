create index user_attrs_abs_exp_date on user_attrs (attr_name,(cast(attr_value as bigint))) where attr_name in ('abs_exp_date','first_login');
create index users_group_id on users(group_id);

