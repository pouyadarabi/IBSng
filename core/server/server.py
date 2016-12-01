from core.server import handlers_manager,xmlrpcserver
from core.threadpool import thread_main
from core.stats import stat_main
from core import defs
import xmlrpclib

def init():
    global server, server_started
    server_started = False
    handlers_manager.init()
    server=xmlrpcserver.XMLRPCServer((defs.IBS_SERVER_IP,defs.IBS_SERVER_PORT))
    
def startServer():

    stat_main.getStatKeeper().registerStat("server_avg_response_time", "seconds")    
    stat_main.getStatKeeper().registerStat("server_max_response_time", "seconds")
    stat_main.getStatKeeper().registerStat("server_total_requests", "int")

    global server_started
    server_started = True
    thread_main.runThread(server.serve_forever,[],"server")


def shutdown():
    if not server_started:
        return
        
    try:
        server=xmlrpclib.ServerProxy("http://%s:%s"%(defs.IBS_SERVER_IP,defs.IBS_SERVER_PORT))
        getattr(server,"exit")()
    except:
        pass
