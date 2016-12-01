from core.server import handler
from core import defs
from core.defs_lib import defs_main
from core.lib.sort import SortedList


class DefsHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"ibs_defs")
        self.registerHandlerMethod("getAllDefs")
        self.registerHandlerMethod("saveDefs")

    #######################################
    def getAllDefs(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE IBS DEFINITIONS")
        def_vars=defs.getDefsLoader().getAllVars()
        defs_list=self.__getDefsListFromDefVars(def_vars)
        sorted=SortedList(defs_list)
        sorted.sortByPostText('["name"]',0)
        return sorted.getList()

    def __getDefsListFromDefVars(self,def_vars):
        """
            def_vars is a dictionary of def_vars in format{"def name":DefVar instance}
            return a list all defs values in format [{"name":def var name,"value":value],...]
        """
        defs_list=[]
        for def_name in def_vars:
            def_var_obj=def_vars[def_name]
            defs_list.append({"name":def_var_obj.getName(),"value":def_var_obj.getValue()})
        return defs_list
    ##########################################
    def saveDefs(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE IBS DEFINITIONS")
        request.checkArgs("defs")
        defs_main.getActionManager().saveDefs(request["defs"])
                