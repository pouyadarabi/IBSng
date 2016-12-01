from core.db import db_main
from core.charge.voip_tariff.tariff import *
from core.ibs_exceptions import *
from core.errors import errorText

class TariffLoader:
    def __init__(self):
        self.__tariffs_id={}#id:obj
        self.__tariffs_name={}#name:obj

    def getTariffByID(self,tariff_id):
        try:
            return self.__tariffs_id[tariff_id]
        except KeyError:
            raise GeneralException(errorText("VOIP_TARIFF","TARIFF_ID_DOESNT_EXISTS")%tariff_id)

    def getTariffByName(self,tariff_name):
        try:
            return self.__tariffs_name[tariff_name]
        except KeyError:
            raise GeneralException(errorText("VOIP_TARIFF","TARIFF_NAME_DOESNT_EXISTS")%tariff_name)

    def tariffNameExists(self,tariff_name):
        return self.__tariffs_name.has_key(tariff_name)

    def getAllTariffNames(self):
        return self.__tariffs_name.keys()
    ###############################
    def loadAllTariffs(self):
        tariff_ids=self.__getAllTariffIDsDB()
        map(self.loadTariffByID,tariff_ids)

    def __getAllTariffIDsDB(self):
        ids_db=db_main.getHandle().get("voip_charge_rule_tariff","",0,-1,"",["tariff_id"])
        return [m["tariff_id"] for m in ids_db]
    ###############################
    def loadTariffByID(self,tariff_id):
        tariff_obj=self.__createTariffObj(tariff_id)
        self.__keepObj(tariff_obj)

    def __keepObj(self,tariff_obj):
        self.__tariffs_id[tariff_obj.getTariffID()]=tariff_obj
        self.__tariffs_name[tariff_obj.getTariffName()]=tariff_obj
    ###############################
    def __createTariffObj(self,tariff_id):
        tariff=self.__getTariffInfoDB(tariff_id)
        prefixes=self.__createPrefixObjs(tariff_id)
        return Tariff(tariff["tariff_id"],tariff["tariff_name"],tariff["comment"],prefixes)

    def __getTariffInfoDB(self,tariff_id):
        info_db=db_main.getHandle().get("voip_charge_rule_tariff","tariff_id=%s"%tariff_id)
        if not info_db:
            raise GeneralException(errorText("VOIP_TARIFF","TARIFF_ID_DOESNT_EXISTS"))
        return info_db[0]
    ###############################
    def __createPrefixObjs(self,tariff_id):
        prefixes=self.__getPrefixesDB(tariff_id)
        return map(lambda dic:Prefix(dic["prefix_id"],
                                     dic["prefix_code"],
                                     dic["prefix_name"],
                                     dic["cpm"],
                                     dic["free_seconds"],
                                     dic["min_duration"],
                                     dic["round_to"],
                                     dic["min_chargable_duration"]),prefixes)

    def __getPrefixesDB(self,tariff_id):
        return db_main.getHandle().get("tariff_prefix_list","tariff_id=%s"%tariff_id)
    ################################
    def unloadTariffByID(self,tariff_id):
        tariff_obj=self.getTariffByID(tariff_id)
        del(self.__tariffs_id[tariff_id])
        del(self.__tariffs_name[tariff_obj.getTariffName()])
    ################################
    