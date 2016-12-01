from core.lib import *
from core.ibs_exceptions import *
from core import defs
from radius_server.pyrad import dictionary, packet, server
from core.ras import ras_main
from core.stats import stat_main
from radius_server import rad_main
from core.threadpool import thread_main
import time

class IBSRadiusServer(server.Server):
        def __getPacketCodeString(self, pkt_code):
            """
                return string representation of packet code
            """
            try:
                return {1:"AccessRequest",
                        2:"AccessAccept",
                        3:"AccessReject",
                        4:"AccountingRequest",
                        5:"AccountingResponse",
                        11:"AccessChallenge",
                        12:"StatusServer",
                        13:"StatusClient",
                        40:"DisconnectRequest",
                        41:"DisconnectAck",
                        42:"DisconnectNack"}[pkt_code]
                        
            except KeyError:
                return "Unknown"

        def __logRequest(self, pkt, incoming=True):
            """
                recv(boolean): did we recieved this packet? False if this is an outgoing packet
            """
            pkt_type = self.__getPacketCodeString(pkt.code)
        
        
            direction = ["O>","I<"][incoming]
            log_str = "##############\n"
            log_str += "%s %s attributes for %s:%s with id %s\n"%(direction,
                                                                pkt_type, 
                                                                pkt.source[0], 
                                                                pkt.source[1], 
                                                                pkt.id)

	    attrs = []
	    for attr_name in pkt.keys():
	        attrs.append("%s: %s"%(attr_name,pkt[attr_name]))

            log_str += " \n".join(attrs)
            toLog(log_str + "\n",LOG_RADIUS)


        def processAuthPacket(self, fd, request_pkt, reply_pkt):
                success=False
                try:
                    success=ras_main.getLoader().getRasByIP(request_pkt.source[0])._handleRadAuthPacket(request_pkt,reply_pkt)
                except:
                    logException(LOG_ERROR,"HandleAuthPacket Exception:\n")
            
                if success: #access ACCEPT      
                    reply_pkt.code=packet.AccessAccept
                else:
                    reply_pkt.code=packet.AccessReject
                    
        
        def processAcctPacket(self, fd, request_pkt, reply_pkt):
                try:
                    ras_main.getLoader().getRasByIP(request_pkt.source[0])._handleRadAcctPacket(request_pkt,reply_pkt)
                except:
                    logException(LOG_ERROR,"HandleAcctPacket exception\n")

        def _handleRequest(self, fd, request_pkt):
            if request_pkt.code == packet.AccessRequest:
                server.Server._HandleAuthPacket(self, fd, request_pkt)

                func = self.processAuthPacket
                stat_name_prefix = "auth"
            else: #acct
                server.Server._HandleAcctPacket(self, fd, request_pkt)

                func = self.processAcctPacket
                stat_name_prefix = "acct"

            if defs.LOG_RADIUS_REQUESTS:
                self.__logRequest(request_pkt)
                
            request_obj = rad_main.getRequestList().getRequest(request_pkt) #check for duplicate packet
            if request_obj != None:
                toLog("Duplicate Packet from %s:%s id %s"%(request_obj.getRequestPacket().source[0], \
                                                           request_obj.getRequestPacket().source[1], \
                                                           request_obj.getRequestPacket().id), LOG_DEBUG)
            
                stat_main.getStatKeeper().inc("%s_duplicate_packets"%stat_name_prefix)
        
                if request_obj.isFinished(): #reply has alreay sent
                    self.SendReplyPacket(fd, request_obj.getResponsePacket())
            else:
                rad_main.getRequestList().addRequest(request_pkt)
                thread_main.runThread(self.__runPacketHandler,(func, fd, request_pkt, stat_name_prefix),"radius")
                        
        def __runPacketHandler(self, func, fd, request_pkt, stat_name_prefix):
                """
                    Run Packet Handler _HandleAXXXPacket, and collect time statistics
                """
                
                reply_pkt = self.CreateReplyPacket(request_pkt)
                reply_pkt.dict = rad_main.getDictionary()

                start = time.time()

                #run the handler
                ret_val = func(fd, request_pkt, reply_pkt)

                duration = time.time() - start
                
                stat_main.getStatKeeper().avg("%s_avg_response_time"%stat_name_prefix, "%s_packets"%stat_name_prefix, duration)
                stat_main.getStatKeeper().max("%s_max_response_time"%stat_name_prefix, duration)
                
                request_obj = rad_main.getRequestList().getRequest(request_pkt)
                request_obj.setResponsePacket(reply_pkt)

                if defs.LOG_RADIUS_RESPONSES:
                    self.__logRequest(reply_pkt, False)

                self.SendReplyPacket(fd, reply_pkt)
                
                return ret_val
