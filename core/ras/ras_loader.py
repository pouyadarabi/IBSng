from core.db import db_main
from core.ras import ras_main
from core.ibs_exceptions import *
from core.errors import errorText
from radius_server.pyrad.server import RemoteHost

class RasLoader:
    def __init__(self):
        self.rases_ip={}
        self.rases_id={}
        self.rases_description={}
        self.radius_remote_hosts={}

    def __getitem__(self,key):
        return self.getRasByID(key)

    def getRasByIP(self,ras_ip):
        try:
            return self.rases_ip[ras_ip]
        except KeyError:
            raise GeneralException(errorText("RAS","INVALID_RAS_IP")%ras_ip)

    def getRasByID(self,ras_id):
        try:
            return self.rases_id[ras_id]
        except KeyError:
            raise GeneralException(errorText("RAS","INVALID_RAS_ID")%ras_id)
        
    def getRasByDesc(self, ras_description):
        try:
            return self.rases_description[ras_description]
        except KeyError:
            raise GeneralException(errorText("RAS","INVALID_RAS_DESCRIPTION")%ras_description)
        
    
    def checkRasIP(self,ras_ip):
        """
            check if ras with ip "ras_ip" is loaded
            raise a GeneralException on Error
        """
        if not self.rasIPExists(ras_ip):
            raise GeneralException(errorText("RAS","INVALID_RAS_IP")%ras_ip)

    
    def checkRasID(self,ras_id):
        """
            check if ras with id "ras_id" is loaded
            raise a GeneralException on Error
        """
        if not self.rases_id.has_key(ras_id):
            raise GeneralException(errorText("RAS","INVALID_RAS_ID")%ras_ip)

    def rasIPExists(self,ras_ip):
        """
            return True if ras with ip "ras_ip" already exists and False if it doesn't exists
        """
        return self.rases_ip.has_key(ras_ip)

    def rasDescExists(self,ras_description):
        """
            return True if ras with description "ras_description" already exists and False if it doesn't exists
        """
        return self.rases_description.has_key(ras_description)

    def getAllRasIPs(self):
        """
            return a list of all ras_ips that is loaded into object
        """
        return self.rases_ip.keys()

    def getAllRasIDs(self):
        """
            return a list of all ras_ids that is loaded into object
        """
        return self.rases_id.keys()

    def getRasDescToIPMap(self):
        """
            return dic in format {ras_description:ras_ip}
        """
        mapping = {}
        for desc in self.rases_description:
            mapping[desc] = self.rases_description[desc].getRasIP()

        return mapping

    def runOnAllRases(self,method):
        """
            run "method" multiple times with each ras_obj as argument
            method should accept one argument (ras_obj)
        """
        return map(method,self.rases_id.values())

    def loadAllRases(self):
        ras_ids=self.__getAllActiveRasIDs()
        map(self.loadRas,ras_ids)

    def loadRas(self,ras_id):
        """
            load ras with id "ras_id" and keep it in the loader object
        """
        ras_obj=self.loadRasObj(ras_id)
        self.keepObj(ras_obj)

    def loadRasObj(self,ras_id):
        """
            load ras with id "ras_id" and return the object
        """
        (ras_info,ras_attrs,ports,ippools)=self.getRasInfo(ras_id)
        ras_obj=self.__createRasObj(ras_info,ras_attrs,ports,ippools)
        return ras_obj

    def getRasInfo(self,ras_id):
        ras_info=self.__getRasInfoDB(ras_id)
        ras_attrs=self.__getRasAttrs(ras_id)
        ports=self.__getRasPorts(ras_id)
        ippools=self.__getRasIPpools(ras_id)
        return (ras_info,ras_attrs,ports,ippools)

    def unloadRas(self,ras_id):
        """
            unload ras, with id "ras_id" from object
            useful when the ras is deleted
        """
        ras_obj=self.getRasByID(ras_id)
        ras_obj.unloaded()
        self.unKeepObj(ras_obj)
    
    def getRadiusRemoteHosts(self):
        return self.radius_remote_hosts

    def __getAllActiveRasIDs(self):
        """
            return a list of all ras_id s from table "ras"
        """
        ras_ids=db_main.getHandle().get("ras","active='t'",0,-1,"",["ras_id"])
        return [m["ras_id"] for m in ras_ids]
            
    def __getRasIPpools(self,ras_id):
        """
            return a list of ras ippool ids in format [pool_id1,pool_id2,..]
        """
        ras_ippools_db=self.__getRasIPpoolsDB(ras_id)
        return [m["ippool_id"] for m in ras_ippools_db]
        
    def __getRasIPpoolsDB(self,ras_id):
        """
            return a list of ras ippool names from table ras_ippools
        """
        return db_main.getHandle().get("ras_ippools", "ras_id=%s"%ras_id, 0, -1, "serial asc")

    def __getRasPorts(self,ras_id):
        """
            return a dic of ports of ras with id "ras_id" in format 
            {port_name:{"phone":phone_no,"type":type,"comment":comment}
        """
        ports={}
        db_ports=self.__getPortsDB(ras_id)
        for _dic in db_ports:
            ports[_dic["port_name"]]=_dic
        return ports

    def __getPortsDB(self,ras_id):
        """
            return a list of dics, that returned from db query from table "ras_ports"
        """
        return db_main.getHandle().get("ras_ports","ras_id=%s"%ras_id)

    def __getRasInfoDB(self,ras_id):
        """
            return a dictionary of ras basic info from table "ras"
        """
        return db_main.getHandle().get("ras","ras_id=%s"%ras_id)[0]

    def __getRasAttrs(self,ras_id):
        """
            return ras attributes in a dic with format {attr_name:attr_value}
        """
        attrs={}
        attrs_db=self.__getRasAttrsDB(ras_id)
        for _dic in attrs_db:
            attrs[_dic["attr_name"]]=_dic["attr_value"]
        return attrs

    def __getRasAttrsDB(self,ras_id):
        """
            return a dic of ras_attributes returned from "ras_attrs" table 
        """
        return db_main.getHandle().get("ras_attrs","ras_id=%s"%ras_id)

    def __createRasObj(self,ras_info,ras_attrs,ports,ippools):
        """
            create a ras object, using ras_info and ras_attrs
        """
        return ras_main.getFactory().getClassFor(ras_info["ras_type"])(ras_info["ras_ip"],      
                                                                       ras_info["ras_id"],
                                                                       ras_info["ras_description"],
                                                                       ras_info["ras_type"],
                                                                       ras_info["radius_secret"],
                                                                       ras_info["comment"],
                                                                       ports,
                                                                       ippools,
                                                                       ras_attrs)

    def keepObj(self,ras_obj):
        """
            keep "ras_obj" into self, by adding them to internal dics
        """
        self.rases_ip[ras_obj.getRasIP()]=ras_obj
        self.rases_id[ras_obj.getRasID()]=ras_obj
        self.rases_description[ras_obj.getRasDesc()]=ras_obj
        self.updateRadiusRemoteHost(ras_obj.getRasIP(),ras_obj.getRadiusSecret())

    def unKeepObj(self,ras_obj):
        del(self.rases_id[ras_obj.getRasID()])
        del(self.rases_ip[ras_obj.getRasIP()])
        del(self.rases_description[ras_obj.getRasDesc()])
        del(self.radius_remote_hosts[ras_obj.getRasIP()])

    def updateRadiusRemoteHost(self, ras_ip, secret_key):
        """
            update the radius remote hosts, setting "ras_ip" secret as "secret_key"
        """
        self.radius_remote_hosts[ras_ip] = RemoteHost(ras_ip,secret_key,ras_ip)
        