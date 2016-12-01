from core.defs_lib.def_var import DefVar

class DefsLoader:
    def __init__(self):
        self.def_vars={}

    def __getitem__(self,key):
        return self.def_vars[key]
        
    def has_key(self,key):
        return self.def_vars.has_key(key)

    def setGlobalsDic(self,globals_dic):
        self.globals_dic=globals_dic
        
    def loadAll(self):
        defs=self.__getAllDefValues()
        map(self.__createDefVarObjs,defs)
        map(self.__setGlobalVars,self.def_vars)
        
    def getAllVars(self):
        return self.def_vars

    def __createDefVarObjs(self,def_dic):
        """
            create a DefVar Object with "def_dic" information
            and put it in self.def_vars
            def_dic should has name and value keys
        """
        self.def_vars[def_dic["name"]]=DefVar(def_dic["name"],def_dic["value"])
        
    def __getAllDefValues(self):
        """
            return a list of dics of all values from "defs" table
        """
        from core.db import db_main
        return db_main.getHandle().get("defs","true")
    
    def __setGlobalVars(self,def_name):
        """
            set defs_vals entries in global scope, so they can easily accessed in format defs.NAME
        """
        self.globals_dic[def_name]=self.def_vars[def_name].getValue()
