from core.server import handler
from core.message import message_main, message_searcher
from core.lib.multi_strs import MultiStr
from core.lib.general import *
from core.lib import report_lib


class MessageHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"message")
        self.registerHandlerMethod("postMessageToUser")
        self.registerHandlerMethod("postMessageToAdmin")

        self.registerHandlerMethod("getAdminMessages")
        self.registerHandlerMethod("getUserMessages")

        self.registerHandlerMethod("deleteMessages")
        self.registerHandlerMethod("deleteUserMessages")

        self.registerHandlerMethod("getLastMessageID")

    ####################################

    def postMessageToUser(self, request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("user_ids","message")
        requester=request.getAuthNameObj()
        requester.canDo("POST MESSAGES")
        if request["user_ids"] == "ALL USERS":
            user_ids = None
        else:
            user_ids = map(lambda x:to_long(x,"user id"),MultiStr(request["user_ids"]))
            
        message_main.getActionsManager().postMessageToUser(user_ids,
                                                           request["message"])

    def postMessageToAdmin(self, request):
        request.needAuthType(request.VOIP_USER,request.NORMAL_USER)
        request.checkArgs("message")
        requester=request.getAuthNameObj()
        message_main.getActionsManager().postMessageToAdmin(long(requester.getUserID()),
                                                           request["message"])

    ######################################
    def getAdminMessages(self, request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("conds", "from", "to", "sort_by", "desc")
        requester = request.getAuthNameObj()

        requester.canDo("VIEW MESSAGES")

        conds = report_lib.fixConditionsDic(request["conds"])
        if conds.has_key("table") and conds["table"] == "user":
            table = "user_messages"
        else:
            table = "admin_messages"
        searcher = message_searcher.MessageSearcher(conds, requester, "admin", table)
        messages = searcher.getMessages(request["from"],
                                        request["to"],
                                        request["sort_by"],
                                        request["desc"],
                                        request.getDateType())
    
        return messages

    def getUserMessages(self, request):
        request.needAuthType(request.VOIP_USER,request.NORMAL_USER)
        request.checkArgs("conds", "from", "to", "sort_by", "desc")
        requester = request.getAuthNameObj()
        conds = report_lib.fixConditionsDic(request["conds"])

        searcher = message_searcher.MessageSearcher(conds, requester, "user", "user_messages")
        messages = searcher.getMessages(request["from"],
                                        request["to"],
                                        request["sort_by"],
                                        request["desc"],
                                        request.getDateType())
    
        return messages

    ###########################
    def deleteUserMessages(self, request):
        request.needAuthType(request.VOIP_USER,request.NORMAL_USER)
        request.checkArgs("message_ids")
        
        message_main.getActionsManager().deleteUserMessages(self.__getMessageIDs(request),
                                                            request.getAuthNameObj().getUserID()
                                                            )

    def deleteMessages(self, request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("message_ids","table")
        
        message_main.getActionsManager().deleteMessages(self.__getMessageIDs(request), request["table"])
    
    def __getMessageIDs(self, request):
        return map(lambda x:to_long(x,"message_id"),request.fixList("message_ids"))

    #########################   
    
    def getLastMessageID(self, request):
        request.needAuthType(request.VOIP_USER,request.NORMAL_USER)

        return message_main.getActionsManager().getUserLastMessageID(request.getAuthNameObj().getUserID())
