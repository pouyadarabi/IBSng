from core.db import db_main
from core.ippool import ippool
from core.ibs_exceptions import *
from core.errors import errorText

class IPpoolLoader:
    def __init__(self):
        self.pool_names={}#ippool_name=>ippool_obj
        self.pool_id={}   #ippool_id  =>ippool_obj


    def checkIPpoolID(self,ippool_id):
        """
            check if pool with id "ippool_id" exists
            raise a GeneralException if !
        """
        if not self.pool_id.has_key(ippool_id):
            raise GeneralException(errorText("IPPOOL","INVALID_IP_POOL_ID")%ippool_id)

    def checkIPpoolName(self,ippool_name):
        """
            check if pool with name "ippool_name" exists
            raise a GeneralException if not
        """
        if not self.pool_names.has_key(ippool_name):
            raise GeneralException(errorText("IPPOOL","INVALID_IP_POOL_NAME")%ippool_id)


    def getIPpoolByID(self,ippool_id):
        """
            return an IPPool instance using "ippool_id"
            raise a GeneralException if ippool_id is not valid
        """
        try:
            return self.pool_id[ippool_id]
        except KeyError: 
            raise GeneralException(errorText("IPPOOL","INVALID_IP_POOL_ID")%ippool_id)

    def getIPpoolByName(self,ippool_name):
        try:
            return self.pool_names[ippool_name]
        except KeyError: 
            raise GeneralException(errorText("IPPOOL","INVALID_IP_POOL_NAME")%ippool_name)

    def ippoolNameExists(self,ippool_name):
        """
            return True if ippool with name "ippool_name" exists
            else return False
        """
        return self.pool_names.has_key(ippool_name)


    def loadIPpoolByID(self,ippool_id):
        """
            load an fresh ip pool using it's "ippool_id" and keep the ippool object to be loaded before
        """
        ippool_obj = self.getIPpoolObjByID(ippool_id)
        self.__keepObj(ippool_obj)

    def getIPpoolObjByID(self,ippool_id):
        """
            get ip pool object that belongs to "ippool_id"
            it doesn't actually load the ippool, instead use loadIpoolByID if you need that
        """
        ippool_info=self.__getIPpoolInfoDB(ippool_id)
        ippool_ips=self.__getIPpoolIPs(ippool_id)
        ippool_obj=self.__createIPpoolObj(ippool_info,ippool_ips)
        return ippool_obj

    def unloadIPpoolByID(self,ippool_id):
        """
            unload an ip pool using it's "ippool_id". remove object from internal list
        """
        ippool_name=self.getIPpoolByID(ippool_id).getIPpoolName()
        del(self.pool_names[ippool_name])
        del(self.pool_id[ippool_id])

    def unloadIPpoolByName(self,ippool_name):
        """
            unload an ip pool using it's "ippool_name". remove object from internal list
        """
        ippool_id=self.getIPpoolByName(ippool_name).getIPpoolID()
        del(self.pool_names[ippool_name])
        del(self.pool_id[ippool_id])


    def loadAllIPpools(self):
        """
            load all ip pools into object, normally should be called by startup routing
        """
        ippool_ids=self.__getAllIPpoolIds()
        map(self.loadIPpoolByID,ippool_ids)

    def getAllIPpoolNames(self):
        return self.pool_names.keys()

    def reloadIPpoolByID(self,ippool_id):
        ippool_obj=self.getIPpoolByID(ippool_id)
        old_name = ippool_obj.getIPpoolName()
        ippool_obj._reload()
        if old_name != ippool_obj.getIPpoolName():
            self.__nameChanged(ippool_obj,old_name)
    
    def __nameChanged(self,ippool_obj,old_name):
        """
            name of ippool_obj has been changed
            this may happen by reload. 
        """
        self.unloadIPpoolByName(old_name)
        self.__keepObj(ippool_obj)
    
    def __getAllIPpoolIds(self):
        """
            return a list of ippool id's from ippool table
        """
        ippoolids_dic=db_main.getHandle().get("ippool","true",0,-1,"ippool_id",["ippool_id"])
        return map(lambda x:x["ippool_id"],ippoolids_dic)

    def __keepObj(self,ippool_obj):
        """
            save object in internal lists
        """
        self.pool_names[ippool_obj.getIPpoolName()]=ippool_obj
        self.pool_id[ippool_obj.getIPpoolID()]=ippool_obj

    def __getIPpoolInfoDB(self,ippool_id):
        """
            return a dic of ippool informations from ippool table
        """
        return db_main.getHandle().get("ippool","ippool_id=%s"%ippool_id)[0]

    def __getIPpoolIPs(self,ippool_id):
        """
            return a list of ip's belongs to ippool with id "ippool_id"
        """
        ip_list=[]
        ips_db=self.__getIPpoolIPsDB(ippool_id)
        for _dic in ips_db:
            ip_list.append(_dic["ip"])
        return ip_list
    
    def __getIPpoolIPsDB(self,ippool_id):
        """
            get ip addresses of ippool with id "ippool_id" from db, and return dic of it's values
        """
        return db_main.getHandle().get("ippool_ips","ippool_id=%s"%ippool_id)   
                    
        
    def __createIPpoolObj(self,ippool_info,ippool_ips):
        """
            create and retun an IPpool instance, from ippool_info and ippool_ips
        """
        return ippool.IPPool(ippool_info["ippool_id"],
                             ippool_info["ippool_name"],
                             ippool_info["ippool_comment"],
                             ippool_ips)
