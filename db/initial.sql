-- ******************************************    Default values    **************************

insert into admins values (0,'system','',0,0,'IBS Internal System Account','',0);
CREATE rule system_admin as on delete to admins where admin_id=0 do instead nothing;
INSERT INTO admin_perms (admin_id,perm_name,perm_value) values (0,'GOD','');
CREATE rule system_admin_god as on delete to admin_perms where admin_id=0 and perm_name='GOD' do instead nothing;
insert into ibs_states VALUES ('MIDNIGHT_JOBS','0');
insert into ibs_states VALUES ('LOWLOAD_JOBS','0');

insert into ibs_states VALUES ('AUTO_CLEAN_CONNECTION_LOG','0');
insert into ibs_states VALUES ('AUTO_CLEAN_CREDIT_CHANGE','0');
insert into ibs_states VALUES ('AUTO_CLEAN_USER_AUDIT_LOG','0');
insert into ibs_states VALUES ('AUTO_CLEAN_SNAPSHOTS','0');
insert into ibs_states VALUES ('AUTO_CLEAN_WEB_ANALYZER_LOG','1209600'); -- 14 days



