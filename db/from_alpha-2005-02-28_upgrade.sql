ALTER TABLE normal_users DROP CONSTRAINT normal_users_pkey;
ALTER TABLE normal_users alter column normal_username drop not null;
ALTER TABLE normal_users ADD CONSTRAINT normal_username_unique unique(normal_username);

ALTER TABLE voip_users DROP CONSTRAINT voip_users_pkey;
ALTER TABLE voip_users alter column voip_username drop not null;
ALTER TABLE voip_users ADD CONSTRAINT voip_username_unique unique(voip_username);

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
    round_to smallint
);
create sequence tariff_prefix_list_tariff_id_seq;
create unique index prefix_name_index on tariff_prefix_list (tariff_id,prefix_code);


create table voip_charge_rules (
    tariff_id integer references voip_charge_rule_tariff
) inherits (charge_rules);
