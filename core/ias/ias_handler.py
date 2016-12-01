from core.server import handler
from core.ias import ias_main
from core.lib.general import to_int
from core.user import user_main
from core.admin import admin_main

class IASHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"ias")
        self.registerHandlerMethod("getEvents")
        self.registerHandlerMethod("deleteEvents")
        self.registerHandlerMethod("getIASUserInfo")


    def getEvents(self, request):
        request.needAuthType(request.ADMIN)
        creator_obj=request.getAuthNameObj()
        creator_obj.canDo("HANDLE IAS EVENTS")

        request.checkArgs("from_event_id","from","to")
        return ias_main.getActionsManager().getEvents(to_int(request["from_event_id"],"from_event_id"),
                                                      to_int(request["from"],"from"),
                                                      to_int(request["to"],"to"))

    def deleteEvents(self, request):
        request.needAuthType(request.ADMIN)
        creator_obj=request.getAuthNameObj()
        creator_obj.canDo("HANDLE IAS EVENTS")
        request.checkArgs("event_ids")

        event_ids=map(lambda event_id:to_int(event_id,"event_id"),request.fixList("event_ids"))
        return ias_main.getActionsManager().deleteEvents(event_ids)
        

    def getIASUserInfo(self, request):
        request.needAuthType(request.ADMIN)
        requester_obj=request.getAuthNameObj()
        requester_obj.canDo("HANDLE IAS EVENTS")
        request.checkArgs("user_ids")

        loaded_users=user_main.getActionManager().getLoadedUsersByUserID(request.fixList("user_ids"))

        user_infos=user_main.getActionManager().getUserInfosFromLoadedUsers(loaded_users,request.getDateType())

        return self.__filterUserInfos(user_infos)

    def __filterUserInfos(self, user_infos):
        """
            remove unnecessary attribute from user_info
        """
        filtered_user_infos = []
        for user_id in user_infos:
            user_info = user_infos[user_id]
            user_dic={"user_id":user_id,
                      "owner":user_info["basic_info"]["owner_name"],
                      "credit":user_info["basic_info"]["credit"]}

            for attr_name in ("normal_username", "voip_username"):
                if user_info["attrs"].has_key(attr_name):
                    user_dic[attr_name] = user_info["attrs"][attr_name]

            filtered_user_infos.append(user_dic)
        
        return filtered_user_infos
    
    #################################
    def lockUser(self, request):
        request.needAuthType(request.ADMIN)
        requester_obj=request.getAuthNameObj()
        requester_obj.canDo("HANDLE IAS EVENTS")
        request.checkArgs("user_id", "reason")
        
        loaded_user=user_main.getUserPool().getUserByUserID(request["user_id"])
        if loaded_user.userHasAttr("lock"):
            lock_reason = "%s, %s"%(loaded_user.getUserAttrs()["lock"], request["reason"])
        else:
            lock_reason = request["reason"]
        
        self.updateUserAttrs([loaded_user],
                             requester_obj,
                             {"lock":lock_reason},
                             [])
                             
    def lockAdmin(self, request):
        request.needAuthType(request.ADMIN)
        requester_obj=request.getAuthNameObj()
        requester_obj.canDo("HANDLE IAS EVENTS")
        request.checkArgs("admin_username", "reason")
        
        admin_main.getActionManager().lockAdmin(request["admin_username"],
                                                request["reason"],
                                                requester_obj)