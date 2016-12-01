from core.server import handler
from core.snapshot import snapshot_main,snapshot_searcher
from core.lib.general import *
from core.lib import report_lib
from core.lib.multi_strs import MultiStr
from core.user import user_main
from core.ras import ras_main


import time

class SnapShotHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"snapshot")
        self.registerHandlerMethod("getRealTimeSnapShot")
        self.registerHandlerMethod("getBWSnapShotForUser")
        self.registerHandlerMethod("getOnlinesSnapShot")
        self.registerHandlerMethod("getBWSnapShot")

    ############################################
    def getRealTimeSnapShot(self, request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("name")
        requester=request.getAuthNameObj()
        requester.canDo("SEE REALTIME SNAPSHOTS")
        snapshot=snapshot_main.getRealTimeManager().getSnapShot(request["name"])
        return (snapshot.getDates(),snapshot.getValues())
        

    #############################################
    def getBWSnapShotForUser(self, request):
        """
            real time version
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("user_id","ras_ip","unique_id_val")
        requester=request.getAuthNameObj()
        requester.canDo("SEE REALTIME SNAPSHOTS")
        return self.__getUserBWValues(to_int(request["user_id"],"user id"),
                                      ras_main.getLoader().getRasByIP(request["ras_ip"]).getRasID(),
                                      request["unique_id_val"])



    def __getUserBWValues(self,user_id,ras_id,unique_id_val):
        snapshot = snapshot_main.getRealTimeManager().getSnapShot("user_bw")
        dates,values = snapshot.getDates(),snapshot.getValues()

        user_vals = []
        
        key = ",".join(map(str,(user_id,ras_id,unique_id_val)))


        i = len(values) - 1

        if i < 0:
            return ([],[])
        
        user_vals = []
        cur_val = values[i]
        while cur_val.has_key(key):
            user_vals.append(cur_val[key])

            i -= 1
            if i<0:
                break
            
            cur_val = values[i]

        user_vals.reverse()
        return (dates[i+1:],user_vals)

    ############################################
    def getOnlinesSnapShot(self, request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("conds","type")
        requester=request.getAuthNameObj()
        requester.canDo("SEE ONLINE SNAPSHOTS")

        conds = report_lib.fixConditionsDic(request["conds"])
        
        searcher = snapshot_searcher.SnapShotSearcher(conds,requester,"admin",request["type"])
        return searcher.getSnapShots()

    ############################################
    def getBWSnapShot(self, request):
        request.checkArgs("conds")
        conds = report_lib.fixConditionsDic(request["conds"])
        requester = request.getAuthNameObj()

        if request.hasAuthType(request.ADMIN):
            if not conds.has_key("user_id"):
                request.raiseIncompleteRequest("user_id")
        
            user_ids = MultiStr(conds["user_id"])
            loaded_users=user_main.getActionManager().getLoadedUsersByUserID(user_ids)  
                
            for loaded_user in loaded_users:
                requester.canDo("SEE BW SNAPSHOTS", loaded_user)

            role = "admin"
                
        elif request.hasAuthType(request.NORMAL_USER) or request.hasAuthType(request.VOIP_USER):
            conds["user_id"] = str(request.getAuthNameObj().getUserID())
            role = "user"
            
        searcher = snapshot_searcher.SnapShotSearcher(conds, requester, role, "bw")
        return searcher.getSnapShots()
