# Changes made to make this work with IBS
# Written by Brian Quinlan (brian@sweetapp.com).
# Based on code written by Fredrik Lundh.

import xmlrpclib
import SocketServer
import BaseHTTPServer
import sys
import time

from core import main
from core.server import handlers_manager
from core.threadpool import thread_main
from core.stats import stat_main
from core.ibs_exceptions import *
from core.lib.general import *
from core import defs

class XMLRPCRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """XML-RPC request handler class.

    Handles all HTTP POST requests and attempts to decode them as
    XML-RPC requests.

    XML-RPC requests are dispatched to the _dispatch method.
    """

    DEBUG=False

    def do_POST(self):
        """Handles the HTTP POST request.

        Attempts to interpret all HTTP POST requests as XML-RPC calls,
        which are forwarded to the _dispatch method for handling.
        """

        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            params, method = xmlrpclib.loads(data)

            # generate response
            try:
                response = self._dispatch(method, params)
                # wrap response in a singleton tuple
                response = (response,)
            except XMLRPCFault:
                # report exception back to server
                response = xmlrpclib.dumps(
                    xmlrpclib.Fault(1, "%s" % (sys.exc_info()[1]))
                    )
            else:
                response = xmlrpclib.dumps(response, methodresponse=1)
        except:
            logException(LOG_ERROR,"XMLRPCServer")
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown(1)

    def _dispatch(self, method, params):
        """Dispatches the XML-RPC method.
        """
        start=time.time()
        if defs.LOG_SERVER_REQUESTS:
            try:
                format="%s %s %s"
                args=[params[0]["auth_type"],params[0]["auth_name"],method]
            except (KeyError,IndexError,TypeError):
                format="N/A N/A %s %s"
                args=[method,str(params)]
        
            apply(self.log_message,[format]+args)
            

        #handle request
        params=self.__convToUTF8(params)        
        ret_val=handlers_manager.getManager().dispatch(method,params,self.client_address)


        #update statistics
        duration = time.time() - start

        stat_main.getStatKeeper().avg("server_avg_response_time", "server_total_requests", duration)
        stat_main.getStatKeeper().max("server_max_response_time", duration)

        if defs.LOG_SERVER_REQUESTS:
            apply(self.log_message,[format+ " duration: %s"]+args+[duration])

        return ret_val

    def __convToUTF8(self,param):
        if type(param)==types.DictType:
            for key in param:
                param[key]=self.__convToUTF8(param[key])

        elif type(param)==types.ListType or type(param)==types.TupleType:
            param=map(self.__convToUTF8,param)

        elif type(param)==types.UnicodeType:
            param=param.encode("utf-8")
        
        return param

    def log_request(self, code='-', size='-'):
        """Selectively log an accepted request."""

        if self.DEBUG and defs.LOG_SERVER_REQUESTS:
            BaseHTTPServer.BaseHTTPRequestHandler.log_request(self, code, size)
            
    def log_message(self, format, *args):
        toLog("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args),LOG_SERVER)

        

class IBSServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer): #overide process request method
        allow_reuse_address=True
        
        def process_request(self,request,client_address):
            if not main.isShuttingDown() and not main.noLoginSet():
                thread_main.runThread(self.process_request_thread,[request,client_address],"server")
#           else:
#               raise IBSException("Ignore server request while we're shutting down")

        def serve_forever(self):
            while not main.isShuttingDown():
                self.handle_request()

        def handle_error(self,request,client_address):
            logException(LOG_ERROR,"IBSServer handle_error")


class XMLRPCServer(IBSServer):
    """Simple XML-RPC server.

    Simple XML-RPC server that allows functions and a single instance
    to be installed to handle requests.
    """

    def __init__(self, addr, requestHandler=XMLRPCRequestHandler):
        self.funcs = {}
        self.instance = None
        SocketServer.TCPServer.__init__(self, addr, requestHandler)

