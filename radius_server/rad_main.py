import sys
import socket
from core.stats import stat_main
from core.threadpool import thread_main
from core.ras import ras_main
from core import defs
from core.ibs_exceptions import *
from radius_server.pyrad import dictionary
from core.event import periodic_events

radius_server_started=False

def init():
    global radius_server_started
    if defs.RADIUS_SERVER_ENABLED==0:
        return

    toLog("Initializing IBS Radius Server", LOG_DEBUG)

    stat_main.getStatKeeper().registerStat("auth_packets", "int")
    stat_main.getStatKeeper().registerStat("acct_packets", "int")    

    stat_main.getStatKeeper().registerStat("auth_duplicate_packets", "int")
    stat_main.getStatKeeper().registerStat("acct_duplicate_packets", "int")    

    stat_main.getStatKeeper().registerStat("auth_avg_response_time", "seconds")
    stat_main.getStatKeeper().registerStat("acct_avg_response_time", "seconds")    

    stat_main.getStatKeeper().registerStat("auth_max_response_time", "seconds")
    stat_main.getStatKeeper().registerStat("acct_max_response_time", "seconds")    

    global ibs_dic
    ibs_dic=dictionary.Dictionary("%s/radius_server/dictionary"%defs.IBS_ROOT,
				  "%s/radius_server/dictionary.usr"%defs.IBS_ROOT,
				  "%s/radius_server/dictionary.ser"%defs.IBS_ROOT,
				  "%s/radius_server/dictionary.sip"%defs.IBS_ROOT)

    from radius_server.request_list import RequestList, CleanRequestListPeriodicEvent
    global request_list
    request_list = RequestList()
    periodic_events.getManager().register(CleanRequestListPeriodicEvent())

    startRadiusServer()
    radius_server_started=True

def startRadiusServer():

    from radius_server.rad_server import IBSRadiusServer
    srv = IBSRadiusServer(dict=ibs_dic, addresses=defs.RADIUS_SERVER_BIND_IP, authport=defs.RADIUS_SERVER_AUTH_PORT, acctport=defs.RADIUS_SERVER_ACCT_PORT)
    srv.hosts = ras_main.getLoader().getRadiusRemoteHosts()
    thread_main.runThread(srv.Run,[],"radius")


def shutdown():
    if not radius_server_started:
        return
            
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.connect((defs.RADIUS_SERVER_BIND_IP[0], defs.RADIUS_SERVER_ACCT_PORT))
    sock.send("\n")
    sock.close()

def getDictionary():
    return ibs_dic

def getRequestList():
    return request_list
