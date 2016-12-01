#### Default definition file
#### Run defs2sql.py [-i,-u] defs.defaults.py to create a sql script file from this file
#### -i option tells defs_sc.py to use insert queries (When you install IBS) 
#### -u tells defs.sc_py to use update queries (When updating defs table)

#### WARNING: all of variables should be defined in python syntax

#######  SERVER IP/PORT
IBS_SERVER_PORT=1235
IBS_SERVER_IP="127.0.0.1" #server bind ip address

TRUSTED_CLIENTS=["127.0.0.1"] #clients we trust(ex. webserver). We trust auth_remoteaddr from these clients

###### RADIUS SERVER
RADIUS_SERVER_ENABLED=1 #ENABLE RADIUS SERVER?
RADIUS_SERVER_BIND_IP=["0.0.0.0"] #radius server bind ip address
RADIUS_SERVER_AUTH_PORT=1812
RADIUS_SERVER_ACCT_PORT=1813
RADIUS_SERVER_CLEANUP_TIME=20

MAX_USER_POOL_SIZE=10000

BW_TC_COMMAND="tc"
BW_IPTABLES_COMMAND="iptables"

CHECK_ONLINE_INTERVAL=60 #seconds
CHECK_ONLINE_MAX_FAILS=2

USER_AUDIT_LOG=1 #enables user audit logging

KILL_USERS_ON_SHUTDOWN=1
KILL_USERS_SHUTDOWN_WAIT_TIME=20

IAS_ENABLED=0 #enables IAS handler and event loggin

WEB_ANALYZER_PASSWORD="web_analyzer_password"

REALTIME_ONLINES_SNAPSHOT_INTERVAL=15
REALTIME_BW_SNAPSHOT_INTERVAL=15
REALTIME_ONLINES_SNAPSHOT_HOURS=5
REALTIME_BW_SNAPSHOT_HOURS=5

SNAPSHOT_ONLINES_INTERVAL=300 #5 minutes
SNAPSHOT_BW_INTERVAL=60 #1 minute

FASTDIAL_PREFIX=""
