from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_holder import AttrHolder
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.lib.date import *
from core.errors import errorText
import time

attr_handler_name="abs exp date"

def init():
    user_main.getUserPluginManager().register("abs_exp_date",AbsExpDate)
    user_main.getAttributeManager().registerHandler(AbsExpDateAttrHandler(),["abs_exp_date"],["abs_exp_date"],["abs_exp_date"])

class AbsExpDate(user_plugin.AttrCheckUserPlugin):
    def __init__(self,user_obj):
        user_plugin.AttrCheckUserPlugin.__init__(self,user_obj,"abs_exp_date")
        self.__initValues()

    def __initValues(self):
        if self.hasAttr():
            self.abs_exp_date=long(self.user_obj.getUserAttrs()["abs_exp_date"])

    def __isAbsExpired(self):
        """
            check if user absolute expiration date has reached
        """
        return self.abs_exp_date<time.time()

    def s_login(self,ras_msg):
        if self.__isAbsExpired():
            raise LoginException(errorText("USER_LOGIN","ABS_EXP_DATE_REACHED"))

    def s_canStayOnline(self):
        result=self.createCanStayOnlineResult()
        if self.__isAbsExpired():
            result.setKillForAllInstances(errorText("USER_LOGIN","ABS_EXP_DATE_REACHED",False),self.user_obj.instances)
        else:
            result.newRemainingTime(self.abs_exp_date-time.time())
        return result

    def _reload(self):
        user_plugin.AttrCheckUserPlugin._reload(self)
        self.__initValues()
    
class AbsExpAttrUpdater(AttrUpdater):
    def changeInit(self,abs_exp_date,abs_exp_date_unit):
        try:
            self.date_obj=AbsDateWithUnit(abs_exp_date,abs_exp_date_unit, False)
        except GeneralException,e:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_ABS_EXP_DATE")%e)

        self.useGenerateQuery({"abs_exp_date":self.date_obj.getDate("epoch")})
                
    def deleteInit(self):
        self.useGenerateQuery(["abs_exp_date"])

    def genQueryAuditLogPrepareOldValue(self,attr_name, old_value):
        return AbsDateFromEpoch(long(old_value)).getDate()

    def genQueryAuditLogPrepareNewValue(self,attr_name, new_value):
        return self.date_obj.getDate()

class AbsExpAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        if search_helper.hasCondFor("abs_exp_date","abs_exp_date_unit","abs_exp_date_op"):
            checkltgtOperator(search_helper.getCondValue("abs_exp_date_op"))
            date_obj=AbsDateWithUnit(search_helper.getCondValue("abs_exp_date"),
                                      search_helper.getCondValue("abs_exp_date_unit"), False)
            for table in self.getUserAndGroupAttrsTable():
                table.search("abs_exp_date",(date_obj.getDate("epoch"),),search_helper.getCondValue("abs_exp_date_op"),"bigint")

class AbsExpAttrHolder(AttrHolder):
    def __init__(self,abs_exp_date):
        self.abs_exp_date=long(abs_exp_date)
        self.date_obj=AbsDateFromEpoch(self.abs_exp_date)

    def getParsedDic(self):
        return {"abs_exp_date":self.date_obj.getDate(self.date_type),"abs_exp_date_unit":self.date_type}

class AbsExpDateAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(AbsExpAttrUpdater,["abs_exp_date","abs_exp_date_unit"])
        self.registerAttrHolderClass(AbsExpAttrHolder,["abs_exp_date"])
        self.registerAttrSearcherClass(AbsExpAttrSearcher)
