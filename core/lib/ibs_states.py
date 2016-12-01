from core.db import db_main,ibs_db
from core.lib.general import *

class State:
    def __init__(self,state_name):
        self.state_name=state_name
        self.cur_value=self.__getCurValueDB()

    def getCurVal(self):
        return self.cur_value

    def __getCurValueDB(self):
        cur_val=db_main.getHandle().get("ibs_states","name="+dbText(self.state_name))
        if len(cur_val)==0:
            raise GeneralException("Zero length value for state %s"%self.state_name)
        return cur_val[0]["value"]

    def setValue(self,value):
        if value==None:
            raise generalException("setState: invalid value %s"%value)
        self.__updateValueDB(value)
        self.cur_value=value

    def updateValueQuery(self,value):
        return ibs_db.createUpdateQuery("ibs_states",{"value":dbText(value)},"name=%s"%dbText(self.state_name))
    
    def __updateValueDB(self,value):
        db_main.getHandle().query(self.updateValueQuery(value))

    