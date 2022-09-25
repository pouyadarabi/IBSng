import pickle
from core.ibs_exceptions import *
from core.lib.general import *
import types

definitions = {
    "MAX_USER_POOL_SIZE":	b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\x10'.",
    "SNAPSHOT_BW_INTERVAL":	b"\x80\x04K<.",
    "REALTIME_BW_SNAPSHOT_INTERVAL":	b"\x80\x04K\x0f.",
    "REALTIME_ONLINES_SNAPSHOT_HOURS":	b"\x80\x04K\x05.",
    "REALTIME_ONLINES_SNAPSHOT_INTERVAL":	b"\x80\x04K\x0f.",
    "SNAPSHOT_ONLINES_INTERVAL":	b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M,\x01.",
    "TRUSTED_CLIENTS":	b"\x80\x04\x95\x10\x00\x00\x00\x00\x00\x00\x00]\x94\x8c\t127.0.0.1\x94a.",
    "USER_AUDIT_LOG":	b"\x80\x04K\x01.",
    "WEB_ANALYZER_PASSWORD":	b"\x80\x04\x95\x19\x00\x00\x00\x00\x00\x00\x00\x8c\x15web_analyzer_password\x94.",
    "BW_IPTABLES_COMMAND":	b"\x80\x04\x95\x0c\x00\x00\x00\x00\x00\x00\x00\x8c\x08iptables\x94.",
    "BW_TC_COMMAND":	b"\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00\x8c\x02tc\x94.",
    "CHECK_ONLINE_INTERVAL":	b"\x80\x04K<.",
    "CHECK_ONLINE_MAX_FAILS":	b"\x80\x04K\x03.",
    "FASTDIAL_PREFIX":	b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94.",
    "IAS_ENABLED":	b"\x80\x04K\x00.",
    "IBS_SERVER_IP":	b"\x80\x04\x95\r\x00\x00\x00\x00\x00\x00\x00\x8c\t127.0.0.1\x94.",
    "IBS_SERVER_PORT":	b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\xd3\x04.",
    "KILL_USERS_ON_SHUTDOWN":	b"\x80\x04K\x01.",
    "KILL_USERS_SHUTDOWN_WAIT_TIME":	b"\x80\x04K\x14.",
    "RADIUS_SERVER_ACCT_PORT":	b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\x15\x07.",
    "RADIUS_SERVER_AUTH_PORT":	b"\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\x14\x07.",
    "RADIUS_SERVER_BIND_IP":	b"\x80\x04\x95\x0e\x00\x00\x00\x00\x00\x00\x00]\x94\x8c\x070.0.0.0\x94a.",
    "RADIUS_SERVER_CLEANUP_TIME":	b"\x80\x04K\x14.",
    "RADIUS_SERVER_ENABLED":	b"\x80\x04K\x01.",
    "REALTIME_BW_SNAPSHOT_HOURS":	b"\x80\x04K\x05.",
}
class DefVar:
    """
        Def Variable, instances of this class would be keep in memory (in a DefLoader instance)
    """
    def __init__(self,name,value):
        """
            value(string): pickled value of variable, we'll unpickle it
        """
        self.name=name
        self.__unpickleValue(value)

    def __unpickleValue(self,value):
        self.value=pickle.loads(definitions[self.name])
        self._type=type(self.value)

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def getType(self):
        return self._type


class RawDefVar:
    """
        Raw Def Variable, used on add/updates
    """
    def __init__(self,var_name,var_value):
        """
            var_name(string): varibale name
            var_values(mixed): value of varible
        """
        self.name=var_name
        self.value=var_value

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def castValue(self,_type):
        if _type==int or _type==bool:
            self.value=to_int(self.value,self.name)
        elif _type==bytes:
            self.value=to_str(self.value,self.name)
        elif _type==list:
            if type(self.value)==dict:
                self.value=list(self.value.values())
            self.value=to_list(self.value,self.name)
        else:
            raise GeneralException("%s has unsupported type %s"%(self.name,_type))

    def insertToDefsQuery(self):
        """

            return a query to insert variable "var_name" with value "var_value" to "defs" table
            value is pickled in order to keep variable type
        """
        from core.db import ibs_db
        return ibs_db.createInsertQuery("defs",{"name":dbText(self.name),
                                        "value":dbText(pickle.dumps(self.value))
                                        })

    def updateDefsQuery(self):
        """
            return an update query to change value(s) of "var_name" in "defs" table
        """
        from core.db import ibs_db
        return ibs_db.createUpdateQuery("defs",{"value":dbText(pickle.dumps(self.value))},
                                                "name=%s"%dbText(self.name))
