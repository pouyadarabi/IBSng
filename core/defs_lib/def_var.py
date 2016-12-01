import pickle
from core.ibs_exceptions import *
from core.lib.general import *
import types


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
        self.value=pickle.loads(value)
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
        if _type==types.IntType or _type==types.BooleanType:
            self.value=to_int(self.value,self.name)
        elif _type==types.StringType:
            self.value=to_str(self.value,self.name)
        elif _type==types.ListType:
            if type(self.value)==types.DictType:
                self.value=self.value.values()
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
