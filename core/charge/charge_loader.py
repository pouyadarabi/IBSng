from core.charge.charge_rule import *
from core.charge.charge_types import *
from core.db import ibs_db,db_main
from core.ras import ras
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.time_lib import *
from core.lib.day_of_week import *
import threading

class ChargeLoader:
    def __init__(self):
        self.charges_id={} #{charge_id=>charge_obj}
        self.charges_name={} #{charge_name=>charge_obj}
        self.rule_loader=ChargeRuleLoader(self)
    
    def __getitem__(self,key):
        return self.getChargeByID(key)
    
    def __iter__(self):
        return self.charges_id.iterkeys()
    
    def getChargeByID(self,charge_id):
        try:
            return self.charges_id[charge_id]
        except KeyError:
            raise GeneralException(errorText("CHARGES","INVALID_CHARGE_ID")%charge_id)

    def getChargeByName(self,charge_name):
        try:
            return self.charges_name[charge_name]
        except KeyError:
            raise GeneralException(errorText("CHARGES","INVALID_CHARGE_NAME")%charge_name)
    
    def loadCharge(self,charge_id):
        """
            create a new charge object and all corresponding rules and put it in self.charges
        """
        charge_obj=self.__createCharge(charge_id)
        self.charges_id[charge_id]=charge_obj
        self.charges_name[charge_obj.getChargeName()]=charge_obj

    def loadAllCharges(self):
        """
            load all charges  from db and put em in self.charges
        """
        charge_ids=self.__getAllChargeIDs()
        for charge_id in charge_ids:
            self.loadCharge(charge_id)
    
    def unloadCharge(self,charge_id):
        """
            delete charge with id "charge_id" from object charges dic
        """
        charge_obj=self.getChargeByID(charge_id)
        del(self.charges_id[charge_obj.getChargeID()])
        del(self.charges_name[charge_obj.getChargeName()])


    def checkChargeID(self,charge_id):
        """
            check if charge with id "charge_id" exists
            raise a general exception if not
        """
        if charge_id not in self.charges_id:
            raise GeneralException(errorText("CHARGES","INVALID_CHARGE_ID") % charge_id)

    def checkChargeName(self,charge_name):
        """
            check if charge with name "charge_name" exists
            raise a general exception if not
        """
        if not self.chargeNameExists(charge_name):
            raise GeneralException(errorText("CHARGES","INVALID_CHARGE_NAME")%charge_name)
            
    def chargeNameExists(self,charge_name):
        """
            check if charge with name "charge_name" exists
            return 1 if it exists, and there's a charge with name "charge_name"
            return 0 if not
        """
        return self.charges_name.has_key(charge_name)

    def runOnAllCharges(self,function):
        """
            function(function instance): function to be called with charge_obj as argument
            function should accept one argument that is a charge_obj. Function will be called for
            all loaded charge_objs
        """
        map(function,self.charges_id.values())

    def getAllChargeNames(self):
        return self.charges_name.keys()

    def __createCharge(self,charge_id):
        """
            create and return a new charge object from charge_id information . it'll load all corresponding
            rules into the object
        """
        charge_info=self.__getChargeInfo(charge_id)
        charge_obj=self.__createChargeObject(charge_info)       
        rules=self.rule_loader.loadChargeRules(charge_obj)
        charge_obj.setRules(rules)
        return charge_obj

        
    def __createChargeObject(self,charge_info):
        """
            create and return a charge object from charge_info dic
        """
        klass=getChargeClassForType(charge_info["charge_type"])
        return klass(charge_info["charge_id"],charge_info["name"],charge_info["comment"],
                               charge_info["admin_id"],charge_info["visible_to_all"],charge_info["charge_type"])
        
    def __getChargeInfo(self,charge_id):
        """
            return a dic of charge properties or raise an exception on error
        """
        try:
            charge_info=db_main.getHandle().get("charges","charge_id=%s"%charge_id)[0]
        except:
            logException("ChargeLoader.getChargeInfo: error in getting charge information")
            raise
        
        return charge_info
    
    def __getAllChargeIDs(self):
        """
            return a list of charge id's from database
        """
        charge_ids=db_main.getHandle().get("charges","true",0,-1,"",["charge_id"])
        return [m["charge_id"] for m in charge_ids]


class ChargeRuleLoader:
    def __init__(self,charge_loader):
        self.charge_loader=charge_loader

    def loadChargeRules(self,charge_obj):
        """
            return a dic of rules of charge_id in format {charge_rule_id=>charge_rule_obj}
        """
        rules_dic={}
        rules=self.__getChargeRuleIDs(charge_obj)
        for rule_info in rules:
            ports=self.__getRulePorts(rule_info["charge_rule_id"])
            day_of_weeks=self.__getDayOfWeeks(rule_info["charge_rule_id"])
            day_of_week_container=apply(DayOfWeekIntContainer,day_of_weeks)
            rule_obj=self.__createChargeRuleObject(charge_obj,rule_info,day_of_week_container,ports)
            rules_dic[rule_obj.getRuleID()]=rule_obj
        return rules_dic


    def __getChargeRuleIDs(self,charge_obj):
        """
            return a list of rules and their properties belongs to charge_id
        """
        rules_table=getRulesTable(charge_obj.getType())
        return db_main.getHandle().get(rules_table,"charge_id=%s"%charge_obj.getChargeID())


    def __createChargeRuleObject(self,charge_obj,rule_info,day_of_weeks,ports):
        """
            create a charge rule object from rule_info dic and ports list
        """
        return getChargeRuleObjForType(charge_obj.getType(),rule_info,charge_obj,day_of_weeks,ports)

    def __getRulePorts(self,charge_rule_id):
        """
            return a list of ports belongs to charge_rule_id
        """
        ports=db_main.getHandle().get("charge_rule_ports","charge_rule_id=%s"%charge_rule_id)
        return [m["ras_port"] for m in ports]
        

    def __getDayOfWeeks(self,charge_rule_id):
        """
            return a list of DayOfWeekInt instances 
        """
        return map(DayOfWeekInt,self.__getDayOfWeeksDB(charge_rule_id))

    def __getDayOfWeeksDB(self,charge_rule_id):
        """
            return a list of day of week integers belongs to charge_rule_id
        """
        dows=db_main.getHandle().get("charge_rule_day_of_weeks","charge_rule_id=%s"%charge_rule_id)
        return [m["day_of_week"] for m in dows]
        