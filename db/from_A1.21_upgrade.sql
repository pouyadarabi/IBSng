alter table ras add comment text;
update ras set comment = '';

alter table ras add ras_description text;
alter table ras add unique(ras_description);
update ras set ras_description = substring(ras_ip::text,1,length(ras_ip::text)-3); -- remove /32 from ip address
alter table ras alter column ras_description set not null;

alter table ras add unique(ras_ip);
alter table ras alter column ras_ip set not null;
