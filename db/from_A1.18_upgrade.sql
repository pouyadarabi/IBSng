
alter table ras_ippools add serial integer;
create sequence ras_ippools_serial_seq;
alter table ras_ippools drop CONSTRAINT ras_ippools_pkey;
alter table ras_ippools alter column serial set default  nextval('public.ras_ippools_serial_seq'::text);
update ras_ippools set serial = nextval('public.ras_ippools_serial_seq'::text);
alter table ras_ippools alter column serial set not null;
alter table ras_ippools add primary key (serial);

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


insert into ibs_states VALUES ('AUTO_CLEAN_WEB_ANALYZER_LOG','0');

insert into defs (name,value) VALUES ('WEB_ANALYZER_PASSWORD','S\'web_analyzer_password\'
p0
.') ;
