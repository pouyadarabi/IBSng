import xmlrpclib, time

from analyze_conf import *
from analyze_exceptions import *


class WebAnalyzerRequest:
    def __init__(self, auth_name, auth_pass, auth_type):
        self.auth_name=auth_name
        self.auth_pass=auth_pass
        self.auth_type=auth_type

    def send(self, method_name, **kargs):
        server=xmlrpclib.ServerProxy("http://%s:%s"%(getConf('IBSNG_SERVER_IP'), getConf('IBSNG_SERVER_PORT')))#IBSng_server
        kargs["auth_type"]=self.auth_type
        kargs["auth_name"]=self.auth_name
        kargs["auth_pass"]=self.auth_pass
        
        return getattr(server,method_name)(kargs)

class Request(WebAnalyzerRequest):
    def __init__(self, web_analyzer_pass=None):
        WebAnalyzerRequest.__init__(self,"ANONYMOUS","ANONYMOUS","ANONYMOUS")
        if web_analyzer_pass == None:
            web_analyzer_pass = getConf('WEB_ANALYZER_PASS')#WEB_ANALYZER_PASS
        
        self.web_analyzer_pass = web_analyzer_pass

    def send(self, method_name,**kargs):
        """
            call method name with dictionary arguments and return the results
        """
        kargs["web_analyzer_password"]= self.web_analyzer_pass
        return apply(WebAnalyzerRequest.send,[self,"web_analyzer.%s"%method_name],kargs)
        

class RequestWrapper(threading.Thread):
    """
        Main Wrapper for XmlRpc requests,
        maintains a send Queue
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.send_queue = []
        self.qlock = threading.Condition()
        self.req = Request()
        self.exit = False
        self.start()

        if getConf('DEBUG'):
            toLog('Request Wrapper, Initiated and ready for feeding the baby :D')

    def run(self):
        try:
            self.__run()
        except:
            logException()
            raise

    def __run(self):
        while not self.exit:
            self.qlock.acquire()
            while not len(self.send_queue):
                self.qlock.wait(5)
                if self.exit:
                    return True
        
            data = self.send_queue.pop(0)
            self.qlock.release()
            if getConf('DEBUG') == 2:
                toLog('try to send %s records'%len(data))

            try:
                feedback = self.req.send('logAnalysis', log_dict = data)
            except:
                logException()
                self.qlock.acquire()
                self.send_queue = [data]+self.send_queue
                self.qlock.release()
                time.sleep(10)

        # oh, let's go home
        if getConf('DEBUG'):
            toLog('requester is stoped.')
        
    def putInQueue(self, data):
        """
            Put new ready to send data in send queue
        """      
        self.qlock.acquire()
        if len(self.send_queue) > getConf('FEEDER_MAX_QUEUE'):
            l = len(self.send_queue.pop(0))
            toLog("MAX_QUEUE reached, Drop records : %s"%l)
            
        self.send_queue.append(data)
        self.qlock.notify()
        self.qlock.release()
        
        if getConf('DEBUG') == 2:
            toLog('putting data in queue, Finished')
    
    def quitSendLoop(self):
        if getConf('DEBUG'):
            toLog('Request Wrapper: Closing ... ')
        self.exit = True
    