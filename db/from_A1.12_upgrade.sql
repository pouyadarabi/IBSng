-- Don't forget to import functions.sql for upgrading from A1.12

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

create index group_attrs_name_value on group_attrs (attr_name, attr_value);
create index user_attrs_name_value on user_attrs (attr_name, attr_value);
