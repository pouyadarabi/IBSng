from core.lib.pysnmp import asn1, v1, v2c
from core.lib.pysnmp import role
from core.ibs_exceptions import *
import threading

class Snmp:
    def __init__(self,ip,community,timeout=10,retries=3,port=161,version="1",max_concurrent=3):
        """
            ip(str): ip of snmp server
            community(str): communuty of server
            timeout(int): timeout
            retries(int): number of retries
            port(int): server snmp port
            version(str): should be either "1" or "2c", snmp version to use
            max_concurrent(str): Maximum concurrent use of this object, further requests will be queued
        """
        self.ip=ip
        self.port=port
        self.community=community
        self.version=version
        self.timeout=timeout
        self.retries=retries
        self.lock=threading.Semaphore(max_concurrent)
        self.clients_lock=threading.Lock()
        
        try:
            self.module=eval('v%s'%version)
        except:
            toLog("Unknown snmp version %s, using v1"%version,LOG_ERROR)
            self.module=v1

        self.clients=[]

#############################
    def createClient(self):
        client=role.manager((self.ip, self.port))
        client.timeout=self.timeout
        client.retries=self.retries
        return client

    def getClient(self):
        self.clients_lock.acquire()
        try:
            if self.clients:
                return self.clients.pop()
            else:
                return self.createClient()
        finally:
            self.clients_lock.release()

    def releaseClient(self, client):
        self.clients_lock.acquire()
        try:
            client.close()
            self.clients.append(client)
        finally:
            self.clients_lock.release()
        

############################
    def getAgentIP(self):
        return self.ip

    def getCommunity(self):
        return self.community
######################################
    def _raiseException(self,_str):
        raise SnmpException("%s\ndst: %s port: %s community: %s version: %s"%(_str,self.ip,self.port,self.community,self.version))

#######################################
    def set(self,oid,type,val):
        """
            set "oid" to "val" that is in type "type"
            oid(str): object id
            type(str): can be on of "i" integer "u" unsigned integer "t" timetick "a" ip address o "object" "s" octet string "u" counter 64
            val(str): value to be set
            an SnmpException will be raised on error
        """
        try:
            type,val=self.__convType(type,val)
            req = self.module.SETREQUEST()
            rsp = self.module.GETRESPONSE()
            encoded_oid=self.__encodeOid(oid)
            encoded_val=eval('asn1.'+type+'()').encode(val)
            self.__sendAndRecv(req,rsp,encoded_oid,encoded_vals=(encoded_val,))
            if rsp['error_status']:
                raise 'SNMP error ' + str(self.module.SNMPError(rsp['error_status']))
        except:
            exc_value=self.__getExceptionValue()
            self._raiseException("SnmpSet on oid: %s type: %s value: %s is \"%s\""%(oid,type,val,exc_value))

    def __convType(self,type,val):
        if type == 'i':
            return ('INTEGER',int(val))
        elif type == 'u':
            return ('UNSIGNED32', int(val))
        elif type == 't':
            return ('TIMETICKS', int(val))
        elif type == 'a':
            return ('IPADDRESS',val)
        elif type == 'o':
            return ('OBJECTID', val)
        elif type == 's':
            return ('OCTETSTRING', val)
        elif type == 'U':
            return ('COUNTER64', long(val))
        else:
            raise GeneralException("Unknown snmp type %s"%type)

##################################
    def walk(self,oid):
        """
            walk on oid, return a dic of {oid:value} or raise an SnmpException
        """
        try:
            return self.__walk(oid)
        except SnmpException:
            raise
        except:
            raise
            exc_value=self.__getExceptionValue()
            self._raiseException("SnmpWalk on oid: %s is \"%s\""%(oid,exc_value))

    def __walk(self,oid):
#       req = self.module.GETREQUEST()    
        req = self.module.GETNEXTREQUEST()
        rsp = self.module.GETRESPONSE()
        encoded_oid=self.__encodeOid(oid)
        completed=False
        result={} #oid:value
        
        while True:
            self.__sendAndRecv(req,rsp,encoded_oid)
            # Check for remote SNMP agent failure

            if rsp['error_status']:
            # SNMP agent reports 'no such name' when walk is over
                if rsp['error_status'] == 2:
                # One of the tables exceeded
                    completed=True
                else:
                    self._raiseException('SNMP error ' + str(self.module.SNMPError(rsp['error_status'])))
            
            # Decode BER encoded Object IDs.
            oids = map(lambda x: x[0], map(asn1.OBJECTID().decode, \
                                   rsp['encoded_oids']))
            # Decode BER encoded values associated with Object IDs.
            vals = map(lambda x: x[0](), map(asn1.decode, rsp['encoded_vals']))

            if not asn1.OBJECTID(oid).isaprefix(oids[0]):
                completed=True

            if completed:
                return result
            
            result[oids[0]]=vals[0]
            
            encoded_oid=self.__encodeOid(oids[0])

    
#################################
    def __encodeOid(self,oid):
        return asn1.OBJECTID().encode(oid)

    def __sendAndRecv(self,req,rsp,encoded_oid,**args):
        kargs={"community":self.community, "encoded_oids":(encoded_oid,)}
        kargs.update(args)

        self.lock.acquire()
        try:
            client=self.getClient()
            (answer, src) = client.send_and_receive(\
                                                    apply(req.encode,[],kargs))
        finally:
            self.releaseClient(client)
            self.lock.release()
            
        rsp.decode(answer)
        if req != rsp:
            self._raiseException('Unmatched response: %s vs %s' % (str(req), str(rsp)))
    
        
    def __getExceptionValue(self):
        exctype, exc_value = sys.exc_info()[:2]
        if exc_value==None: 
            exc_value=str(exctype)
        return exc_value
    