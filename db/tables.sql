-- ******************* ADMINS
create table admins(
    admin_id integer primary key,
    username text unique,
    password char(34),
    deposit numeric(12,2) default 0,
    due numeric(12,2) default 0,
    name text,
    comment text,
    creator_id integer
);   

create sequence admins_id_seq;

create table admins_extended_attrs(
    admin_id integer references admins,
    attr_name text,
    attr_value text,
    primary key(admin_id, attr_name)
);

create table admin_locks(
    lock_id bigint primary key,
    locker_admin_id integer references admins,
    admin_id integer references admins,
    reason text
);

create sequence admin_locks_lock_id_seq;

create table admin_perms (
    admin_id integer references admins,
    perm_name text,
    perm_value text,
    primary key(admin_id,perm_name));

create table admin_perm_templates (
    template_id integer primary key,
    template_name text
);

create sequence admin_perm_template_id;

create table admin_perm_templates_detail (
    template_id integer references admin_perm_templates,
    perm_name text,
    perm_value text,
    primary key(template_id, perm_name));

-- ****************** IP POOLS
create table ippool(
    ippool_id integer primary key,
    ippool_name text,
    ippool_comment	text
);

create sequence ippool_id_seq;

create table ippool_ips(
    ippool_id integer references ippool,
    ip	inet,
    primary key (ippool_id, ip));
create unique index ippool_ips_index on ippool_ips (ippool_id,ip);

-- *********************** RAS
create table ras (
    ras_id integer primary key,
    ras_description text unique,
    ras_ip inet unique,
    ras_type text,
    radius_secret text,
    active boolean default 't',
    comment text
);
create sequence ras_id_seq;

create table ras_ports (
    ras_id integer references ras,
    port_name text,
    phone text,
    type text,
    comment text,
    primary key(ras_id, port_name)
);
create unique index ras_ports_index on ras_ports (ras_id,port_name);

create table ras_attrs (
    ras_id integer references ras,
    attr_name text,
    attr_value text,
    primary key(ras_id, attr_name)
);

create table ras_ippools (
    serial serial primary key,
    ras_id integer references ras,
    ippool_id integer references ippool
);

create unique index ras_attrs_index on ras_attrs (ras_id,attr_name);


-- ******************
create table groups (
    group_id integer primary key,
    group_name text unique,
    owner_id integer references admins,
    comment text
);

create sequence groups_group_id_seq;

create table group_attrs (
    group_id integer references groups,
    attr_name text,
    attr_value text,
    primary key(group_id, attr_name)
);

create index group_attrs_name_value on group_attrs (attr_name, attr_value);


-- *************** USERS
create table users (
    user_id bigint primary key,
    owner_id integer references admins,
    credit numeric(12,2),
    group_id integer ,
    creation_date timestamp without time zone default CURRENT_TIMESTAMP
);
create index users_group_id on users(group_id);

create table normal_users (
    user_id bigint references users,
    normal_username text unique,  -- not primary key, it will be cast as null in updates
    normal_password text
);
create unique index normal_users_user_id on normal_users (user_id);

create table persistent_lan_users (
    user_id bigint references users,
    persistent_lan_mac macaddr,
    persistent_lan_ip cidr,
    persistent_lan_ras_id integer references ras,
    primary key(persistent_lan_mac,persistent_lan_ip)
);
create index persistent_lan_ras_id_index on persistent_lan_users (persistent_lan_ras_id);
create index persistent_lan_user_id on persistent_lan_users (user_id);


create sequence add_user_save_id_seq;
create table add_user_saves(
    add_user_save_id integer primary key,
    add_date	timestamp without time zone default CURRENT_TIMESTAMP,
    admin_id	integer references admins,
    type	integer, --1:Normal 2:VoIP
    comment	text
);

create table add_user_save_details(
    add_user_save_id integer references add_user_saves,
    user_id bigint,
    username text,
    password text,
    primary key(add_user_save_id, user_id)
);

create table voip_users (
    user_id bigint references users,
    voip_username text unique, 
    voip_password text
);
create unique index voip_users_user_id on voip_users (user_id);


create table user_attrs (
    user_id bigint references users,
    attr_name text,
    attr_value text,
    primary key(user_id, attr_name)
);
create sequence users_user_id_seq;
create index user_attrs_name_value on user_attrs (attr_name, attr_value);
create index user_attrs_abs_exp_date on user_attrs (attr_name,(cast(attr_value as bigint))) where attr_name in ('abs_exp_date','first_login');

create table caller_id_users (
    user_id bigint references users,
    caller_id text primary key
);
create index caller_id_users_user_id on caller_id_users (user_id);

-- ************************ CONFIGURATION

create table defs (
    name text primary key,
    value text,
    type text    
);

create table ibs_states(
    name text primary key,
    value text
);

-- *********************** LOGS
create table credit_change (
    credit_change_id bigint primary key,
    admin_id integer,
    action smallint,
    per_user_credit numeric(12,2),
    admin_credit numeric(12,2),
    change_time timestamp without time zone default CURRENT_TIMESTAMP,
    remote_addr inet,
    comment text
);

create table credit_change_userid (
    credit_change_id bigint references credit_change,
    user_id bigint,
    primary key (credit_change_id, user_id)
);

create index credit_change_userid_index on credit_change_userid (user_id);
create sequence credit_change_id;

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


create table connection_log (
    connection_log_id bigint primary key,
    user_id bigint,
    credit_used numeric(12,2),
    login_time timestamp,
    logout_time	timestamp,
    successful bool,
    service smallint,--1 internet , 2- voip
    ras_id integer
);

create index connection_log_userid_index on connection_log (user_id);
create index connection_log_login_time_index on connection_log(login_time);

create table connection_log_details (
    connection_log_id bigint references connection_log,
    name text, 
    value text,
    primary key (connection_log_id, name)
);

create sequence connection_log_id;
create index connection_log_details_name_value_index on connection_log_details(name,value);

-- *********************** BANDWIDTH MANAGER
create table bw_interface (
    interface_id integer primary key,
    interface_name text,
    comment text
);
create sequence bw_interface_interface_id_seq;

create table bw_node (
    node_id integer primary key,
    interface_id integer references bw_interface,
    parent_id integer references bw_node,
    rate_kbits integer,
    ceil_kbits integer
);
create sequence bw_node_node_id_seq;

create table bw_leaf (
    leaf_id integer primary key,
    leaf_name text,
    interface_id integer references bw_interface,
    parent_id integer references bw_node,
    default_rate_kbits integer,
    default_ceil_kbits integer,
    total_rate_kbits integer,
    total_ceil_kbits integer
);
create sequence bw_leaf_leaf_id_seq;

create table bw_leaf_services (
    leaf_service_id integer primary key,
    leaf_id integer references bw_leaf,
    protocol text,
    filter text,
    rate_kbits integer,
    ceil_kbits integer
);
create sequence bw_leaf_services_leaf_service_id_seq;    

create table bw_static_ip (
    bw_static_ip_id integer primary key,
    ip inet unique,
    transmit_leaf_id integer references bw_leaf,
    receive_leaf_id integer references bw_leaf
);
create sequence bw_static_ip_bw_static_ip_id_seq;    

-- ******************* CHARGES ***********
create table charges (
    charge_id integer primary key,
    name text unique,
    charge_type text, --'Internet' or 'VoIP'
    comment text,
    admin_id integer references admins ,
    visible_to_all boolean default 'FALSE'
);

create sequence charges_id_seq;
create sequence charge_rules_id_seq; --used for both voip and internet rules

create table charge_rules (
    charge_id integer references charges,
    charge_rule_id integer primary key,
    start_time time,
    end_time time,
    time_limit integer, -- in minutes
    ras_id integer references ras
);


create table internet_charge_rules (
    cpm numeric(12,2),
    cpk numeric(12,2),
    assumed_kps integer,
    bandwidth_limit_kbytes integer default -1,
    bw_transmit_leaf_id integer references bw_leaf,
    bw_receive_leaf_id integer references bw_leaf,
    primary key(charge_rule_id)
) inherits (charge_rules);

create table charge_rule_ports (
    charge_rule_id integer,
    ras_port text,
    primary key(charge_rule_id, ras_port)
);

create table charge_rule_day_of_weeks (
    charge_rule_id integer,
    day_of_week integer,
    primary key(charge_rule_id, day_of_week)
);

-- *********************
create table voip_charge_rule_tariff (
    tariff_id integer primary key,
    tariff_name text,
    comment text
);
create sequence voip_charge_rule_tariff_tariff_id_seq;

create table tariff_prefix_list (
    tariff_id integer references voip_charge_rule_tariff,
    prefix_id integer primary key,
    prefix_code text,
    prefix_name text,
    cpm numeric(12,2),
    free_seconds smallint,
    min_duration smallint,
    round_to smallint,
    min_chargable_duration smallint
);
create sequence tariff_prefix_list_tariff_id_seq;
create unique index prefix_name_index on tariff_prefix_list (tariff_id,prefix_code);


create table voip_charge_rules (
    tariff_id integer references voip_charge_rule_tariff,
    primary key(charge_rule_id)
) inherits (charge_rules);


-- ********************* User Audit Log
create table user_audit_log(
    user_audit_log serial primary key,
    admin_id integer,
    is_user bool,
    object_id bigint, -- user_id, or group_id
    attr_name text,
    old_value text,
    new_value text,
    change_time timestamp without time zone default CURRENT_TIMESTAMP
);

--********************* Snap Shots
create table internet_onlines_snapshot(
    snp_date timestamp without time zone default CURRENT_TIMESTAMP,
    ras_id integer,
    value integer,
    primary key(snp_date, ras_id)
);


create table voip_onlines_snapshot(
    snp_date timestamp without time zone default CURRENT_TIMESTAMP,
    ras_id integer,
    value integer,
    primary key(snp_date, ras_id)
);

create table internet_bw_snapshot(
    snp_date timestamp without time zone default CURRENT_TIMESTAMP,
    user_id integer references users,
    in_rate integer,
    out_rate integer,
    primary key(user_id, snp_date)
);



--********************* Messaging
create table user_messages ( -- user queued messages
    message_id bigint primary key,
    user_id bigint references users,
    message_text text,
    post_date timestamp without time zone default CURRENT_TIMESTAMP
);
create sequence user_messages_message_id;

create table admin_messages ( -- admin queued messages
    message_id bigint primary key,
    user_id bigint references users,
    message_text text,
    post_date timestamp without time zone default CURRENT_TIMESTAMP
);
create sequence admin_messages_message_id;

-- ***************************** IAS
create table ias_event (
    event_id bigint primary key,
    event_type smallint, -- 1: CHANGE_USER_CREDIT 2: CHANGE_ADMIN_DEPOSIT 3: ADD_USER 4: DEL_USER 5: ADD_ADMIN 6: DELETE_ADMIN 7: USER_CONSUME(IAS Internal) 8: ADMIN_CONSUME(IAS Internal) 9:ADMIN_CREDIT(IAS Internal)
    event_date timestamp without time zone default CURRENT_TIMESTAMP,
    actor text, -- admin username
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

-- ********************************** Web Analyzer
create table web_analyzer_log(
    log_id	bigint primary key,
    _date	timestamp without time zone default CURRENT_TIMESTAMP,
    user_id	bigint,
    ip_addr	inet,
    url		text,
    elapsed	integer,
    bytes	integer,
    miss	smallint,
    hit		smallint,
    successful	smallint,
    failure	smallint,
    _count	integer
);

create sequence web_analyzer_log_log_id;
create index web_analyzer_log_date_index on web_analyzer_log(_date);
create index web_analyzer_log_user_id_index on web_analyzer_log(user_id);