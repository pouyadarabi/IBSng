import pickle
from core.db import ibs_db,db_main
from core.lib.general import *
from core.defs_lib.def_var import RawDefVar
from core.defs import getDefsLoader

class DefsActions:
    def saveDefs(self,defs_dic):
        """
            save contents of defs_dic by updating values in database
        """
        def_vars=self.__createDefVars(defs_dic)
        self.__checkDefVars(def_vars)
        self.__saveDefsDB(def_vars)
        getDefsLoader().loadAll()
            
    def __saveDefsDB(self,def_vars):
        query=self.__saveDefsQuery(def_vars)
        db_main.getHandle().transactionQuery(query)
        
    def __saveDefsQuery(self,def_vars):
        query=""
        for def_var in def_vars:
            query+=def_var.updateDefsQuery()
        return query
    
    def __checkDefVars(self,def_vars):
        """
            check def vars.
            check if defined names are valid and cast their value if needed
        """
        for def_var in def_vars:
            if not getDefsLoader().has_key(def_var.getName()):
                raise GeneralException(errorText("DEFS","INVALID_DEFINITION_NAME")%def_var.getName())
            
            loaded_def_var=getDefsLoader()[def_var.getName()]
            def_var.castValue(loaded_def_var.getType())
            
    def __createDefVars(self,defs_dic):
        def_vars=[]
        for def_name in defs_dic:
            def_vars.append(RawDefVar(def_name,defs_dic[def_name]))
        return def_vars
