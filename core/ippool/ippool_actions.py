from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.db import db_main,ibs_db,ibs_query
from core.ippool import ippool_main
from core.lib import iplib
from core.ras import ras_main
from core.user import user_main
from core.group import group_main

class IPpoolActions:

    def __reloadIPpool(self,ippool_id):
        ippool_main.getLoader().reloadIPpoolByID(ippool_id)
########################################
    def addNewPool(self,ippool_name,comment):
        """
            add a new ip pool
            ippool_name(string): name of new ip pool
            comment(string): comment about new ippool
        """
        self.__addNewPoolCheckInput(ippool_name,comment)
        ippool_id=self.__getNewIPpoolID()
        self.__insertPoolDB(ippool_id,ippool_name,comment)
        ippool_main.getLoader().loadIPpoolByID(ippool_id)
        return ippool_id

    def __addNewPoolCheckInput(self,ippool_name,comment):
        if not isValidName(ippool_name):
            raise GeneralException(errorText("IPPOOL","BAD_IP_POOL_NAME")%ippool_name)
        
        if ippool_main.getLoader().ippoolNameExists(ippool_name):
            raise GeneralException(errorText("IPPOOL","IP_POOL_NAME_ALREADY_EXISTS")%ippool_name)
        
    def __getNewIPpoolID(self):
        """
            return a new unique ip pool id
        """
        return db_main.getHandle().seqNextVal("ippool_id_seq")

    def __insertPoolDB(self,ippool_id,ippool_name,comment):
        db_main.getHandle().transactionQuery(self.__insertPoolQuery(ippool_id,ippool_name,comment))

    def __insertPoolQuery(self,ippool_id,ippool_name,comment):
        return ibs_db.createInsertQuery("ippool",{"ippool_id":ippool_id,
                                                  "ippool_name":dbText(ippool_name),
                                                  "ippool_comment":dbText(comment)
                                                 })
########################################################
    def updatePool(self,ippool_id,ippool_name,comment):
        self.__updatePoolCheckInput(ippool_id,ippool_name,comment)
        self.__updatePoolDB(ippool_id,ippool_name,comment)
        self.__reloadIPpool(ippool_id)
        
    def __updatePoolCheckInput(self,ippool_id,ippool_name,comment):
        ippool_main.getLoader().checkIPpoolID(ippool_id)

        ippool_obj=ippool_main.getLoader().getIPpoolByID(ippool_id)
        if ippool_obj.getIPpoolName()!=ippool_name:
            if not isValidName(ippool_name):
                raise GeneralException(errorText("IPPOOL","BAD_IP_POOL_NAME")%ippool_name)
        
            if ippool_main.getLoader().ippoolNameExists(ippool_name):
                raise GeneralException(errorText("IPPOOL","IP_POOL_NAME_ALREADY_EXISTS")%ippool_name)

    def __updatePoolDB(self,ippool_id,ippool_name,comment):
        db_main.getHandle().transactionQuery(self.__updatePoolQuery(ippool_id,ippool_name,comment))

    def __updatePoolQuery(self,ippool_id,ippool_name,comment):
        return ibs_db.createUpdateQuery("ippool",{"ippool_name":dbText(ippool_name),
                                           "ippool_comment":dbText(comment)},
                                           "ippool_id=%s"%ippool_id)
#########################################################
    def deletePool(self,ippool_name):
        """
            delete a pool using it's "ippool_name"
        """     
        self.__deletePoolCheckInput(ippool_name)
        ippool_obj=ippool_main.getLoader().getIPpoolByName(ippool_name)
        self.__deletePoolDB(ippool_obj.getIPpoolID())
        ippool_main.getLoader().unloadIPpoolByID(ippool_obj.getIPpoolID())
    
    def __deletePoolCheckInput(self,ippool_name):
        ippool_obj=ippool_main.getLoader().getIPpoolByName(ippool_name)

        def checkIPpoolInRas(ras_obj):
            if ras_obj.hasIPpool(ippool_obj.getIPpoolID()):
                raise GeneralException(errorText("IPPOOL","IPPOOL_USED_IN_RAS")%ras_obj.getRasIP())

        ras_main.getLoader().runOnAllRases(checkIPpoolInRas)
        self.__checkPoolUsageInUsers(ippool_obj)
        self.__checkPoolUsageInGroups(ippool_obj)
        
    def __checkPoolUsageInUsers(self,ippool_obj):
        user_ids=user_main.getActionManager().getUserIDsWithAttr("ippool",ippool_obj.getIPpoolID())
        if len(user_ids)>0:
            raise GeneralException(errorText("IPPOOL","IPPOOL_USED_IN_USER")%",".join(map(str,user_ids)))

    def __checkPoolUsageInGroups(self,ippool_obj):
        group_ids=group_main.getActionManager().getGroupIDsWithAttr("ippool",ippool_obj.getIPpoolID())
        if len(group_ids)>0:
            raise GeneralException(errorText("IPPOOL","IPPOOL_USED_IN_GROUP")% ",".join(map(str,group_ids)))


    def __deletePoolDB(self,ippool_id):
        query=self.__deletePoolIPsQuery(ippool_id)
        query+=self.__deletePoolQuery(ippool_id)        
        db_main.getHandle().transactionQuery(query)
    
    def __deletePoolQuery(self,ippool_id):
        return ibs_db.createDeleteQuery("ippool","ippool_id=%s"%ippool_id)
        
    def __deletePoolIPsQuery(self,ippool_id):
        return ibs_db.createDeleteQuery("ippool_ips","ippool_id=%s"%ippool_id)

###########################################################
    def addIPtoPool(self,ippool_name,ips):
        """
            add new "ip" to ippool with name "ippool_name"
            ips(MultiStr): can be a multi string of multiple ips
        """
        self.__addIPtoPoolCheckInput(ippool_name,ips)
        ippool_obj=ippool_main.getLoader().getIPpoolByName(ippool_name)
        self.__addIPtoPoolDB(ippool_obj.getIPpoolID(),ips)
        self.__reloadIPpool(ippool_obj.getIPpoolID())

    def __addIPtoPoolCheckInput(self,ippool_name,ips):
        ippool_obj=ippool_main.getLoader().getIPpoolByName(ippool_name)
        map(self.__checkIPAddr,ips)

        def checkIPAvailabilityInPool(ip):
            if ippool_obj.hasIP(ip):
                raise GeneralException(errorText("IPPOOL","IP_ALREADY_IN_POOL")%ip)

        map(checkIPAvailabilityInPool,ips)

        
    def __checkIPAddr(self,ip):
        """
            check if "ip" is valid, raise an exception if not
        """
        if not iplib.checkIPAddrWithoutMask(ip):
            raise GeneralException(errorText("GENERAL","INVALID_IP_ADDRESS")%ip)


    def __addIPtoPoolDB(self,ippool_id,ips):
        query=ibs_query.IBSQuery()
        for ip in ips:
            query+=self.__addIPToPoolQuery(ippool_id,ip)
        query.runQuery()
    
    def __addIPToPoolQuery(self,ippool_id,ip):
        return ibs_db.createInsertQuery("ippool_ips",{"ippool_id":ippool_id,
                                                      "ip":dbText(ip)})



##########################################################
    def delIPfromPool(self,ippool_name,ips):
        """
            delete "ip" from ippool with name "ippool_name"
            ips(MultiStr instance): can be a multi string of multiple ips
        """
        self.__delIPfromPoolCheckInput(ippool_name,ips)
        ippool_obj=ippool_main.getLoader().getIPpoolByName(ippool_name)
        self.__delIPfromPoolDB(ippool_obj.getIPpoolID(),ips)
        self.__reloadIPpool(ippool_obj.getIPpoolID())

    def __delIPfromPoolCheckInput(self,ippool_name,ips):
        ippool_obj=ippool_main.getLoader().getIPpoolByName(ippool_name)

        for ip in ips:
            self.__checkIPAddr(ip)
        
            if not ippool_obj.hasIP(ip):
                raise GeneralException(errorText("IPPOOL","IP_NOT_IN_POOL")%ip)

            if ippool_obj.isIPUsed(ip):
                raise GeneralException(errorText("IPPOOL","IP_IS_USED")%ip)

    def __delIPfromPoolDB(self,ippool_id,ips):
        query=ibs_query.IBSQuery()
        for ip in ips:
            query+=self.__delIPfromPoolQuery(ippool_id,ip)
        query.runQuery()
    
    def __delIPfromPoolQuery(self,ippool_id,ip):
        return ibs_db.createDeleteQuery("ippool_ips","ippool_id=%s and ip=%s"%(ippool_id,dbText(ip)))

