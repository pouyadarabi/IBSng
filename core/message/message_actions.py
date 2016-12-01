from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.user import user_main
from core.db import db_main, ibs_db, ibs_query

class MessageActions:
    def __init__(self):
        self.last_to_all_message_id = self.__getLastToAllMessageID()

    def postMessageToUser(self, user_ids, message_text):
        """
            user_ids(iterable object): id of users, if set to None, means send message to all users
            message_text(string): body of message
        """
        self.__postMessageToUserCheckInput(user_ids, message_text)
        message_ids = self.__postMessageToUserDB(user_ids, message_text)
        self.__postMessageToUserUpdateLastID(user_ids, message_ids)
        return message_ids

    def __postMessageToUserCheckInput(self,user_ids, message_text):
        if user_ids != None:
            map(self.__checkUserID, user_ids)
        
        self.__checkMessageText(message_text)

    def __checkUserID(self, user_id):
        if not isLong(user_id):
            raise GeneralException(errorText("USER","INVALID_USER_ID")%user_id)

        loaded_user = user_main.getUserPool().getUserByID(user_id) #check user id

    def __checkMessageText(self, message_text):
        if not len(message_text) or len(message_text) > 1000:
            raise GeneralException(errorText("MESSAGES","INVALID_MESSAGE_LENGTH"))
        
    def __postMessageToUserDB(self, user_ids, message_text):
        query = ibs_query.IBSQuery()
        message_ids = []
        if user_ids:
            for user_id in user_ids:
                message_id = self.__getNextMessageIDForUser()
                message_ids.append(message_id)
                query += self.__postMessageToUserQuery(message_id, user_id, message_text)
        else:
            message_id = self.__getNextMessageIDForUser()
            message_ids.append(message_id)
            query += self.__postMessageToUserQuery(message_id, "NULL", message_text)

        query.runQuery()
        return message_ids

    def __getNextMessageIDForUser(self):
        return db_main.getHandle().seqNextVal("user_messages_message_id")

    def __postMessageToUserQuery(self, message_id, user_id, message_text):
        return self.__postMessageToTableQuery("user_messages",message_id, user_id, message_text, False)

    def __postMessageToTableQuery(self, table_name, message_id, user_id, message_text, strip_tags=True):
        if strip_tags:
            message_text = dbText(message_text)
        else:
            message_text = "'%s'"%escapeSlashes(message_text)
        return ibs_db.createInsertQuery(table_name,{"message_id":message_id,
                                                         "user_id":user_id,
                                                         "message_text":message_text})

    def __postMessageToUserUpdateLastID(self, user_ids, message_ids):
        if user_ids == None:
            self.last_to_all_message_id = message_ids[0]
        else:
            for i in range(len(user_ids)):
                user_id = user_ids[i]
                user_obj = user_main.getOnline().getUserObj(user_id)
                if user_obj:
                    user_obj.last_message_id = message_ids[i]
        
        
    ######################################
    def postMessageToAdmin(self, user_id, message_text):
        """
            user_id(int): id of user
            message_text(string): body of message
        """
        self.__postMessageToAdminCheckInput(user_id, message_text)
        self.__postMessageToAdminDB(user_id, message_text)

        self.postMessageToUser((user_id,), "Message Sent - %s" % escapeTags(message_text))

    def __postMessageToAdminCheckInput(self, user_id, message_text):
        self.__checkUserID(user_id)
        self.__checkMessageText(message_text)

    def __postMessageToAdminDB(self, user_id, message_text):
        message_id = self.__getNextMessageIDForAdmin()
        db_main.getHandle().transactionQuery(self.__postMessageToAdminQuery(message_id, user_id, message_text))
        return message_id
        
    def __getNextMessageIDForAdmin(self):
        return db_main.getHandle().seqNextVal("admin_messages_message_id")

    def __postMessageToAdminQuery(self, message_id, user_id, message_text):
        return self.__postMessageToTableQuery("admin_messages",message_id, user_id, message_text)
    ########################################
    def deleteUserMessages(self, message_ids, user_id):
        self.__deleteUserMessagesCheckInput(message_ids, user_id)
        self.__deleteUserMessagesDB(message_ids, user_id)       

    def __deleteUserMessagesCheckInput(self, message_ids, user_id):
        map(self.__checkMessageID, message_ids)
        self.__checkSendToAllMessageIDs(message_ids)
        self.__checkUserID(user_id)

    def __checkSendToAllMessageIDs(self, message_ids):
        cond = " or ".join(map(lambda message_id:"message_id=%s"%message_id,message_ids))
        _count = db_main.getHandle().getCount("user_messages", "(%s) and user_id is null"%cond)
        if _count:
            raise GeneralException(errorText("MESSAGES","CANT_DELETE_SEND_TO_ALL"))
        

    def __checkMessageID(self, message_id):
        if not isLong(message_id):
            raise GeneralException(errorText("MESSAGES","INVALID_MESSAGE_ID")%message_id)
    
    def __deleteUserMessagesDB(self, message_ids, user_id):
        db_main.getHandle().transactionQuery(self.__deleteUserMessagesQuery(message_ids, user_id))
    
    def __deleteUserMessagesQuery(self, message_ids, user_id):
        cond = "( %s ) and user_id = %s"%(" or ".join(map(lambda message_id:"message_id=%s"%message_id,message_ids)),
                                          user_id)
        return ibs_db.createDeleteQuery("user_messages",cond)                             

    #########################################
    def deleteMessages(self, message_ids, table):
        self.__deleteMessagesCheckInput(message_ids, table)
        db_table_name = "%s_messages"%table
        self.__deleteMessagesDB(db_table_name, message_ids)

    def __deleteMessagesCheckInput(self, message_ids, table):
        map(self.__checkMessageID, message_ids)
        if table not in ["admin","user"]:
            raise GeneralException(errorText("MESSAGES","INVALID_MESSAGE_TABLE")%table)

    def __deleteMessagesDB(self, table_name, message_ids):
        query = ""
        for message_id in message_ids:
            query += self.__deleteMessageQuery(table_name, message_id)
        db_main.getHandle().transactionQuery(query)

    def __deleteMessageQuery(self, table_name, message_id):
        return ibs_db.createDeleteQuery(table_name , "message_id = %s"%message_id)
    ########################################
    def getUserLastMessageID(self, user_id):
        """
            return Last Message ID for user with id "user_id"
        """
        self.__getUserLastMessageIDCheckInput(user_id)
        loaded_user = user_main.getUserPool().getUserByID(user_id)
        if loaded_user.isOnline():
            user_obj = user_main.getOnline().getUserObj(user_id)
            if hasattr(user_obj,"last_message_id"):
                return max(user_obj.last_message_id, self.last_to_all_message_id)
        
        last_message_id = self.__getLastMessageIDForUser(user_id)
        
        if loaded_user.isOnline() and "user_obj" in locals(): #prevent a rare race condition
            user_obj.last_message_id = last_message_id
        
        return max(last_message_id, self.last_to_all_message_id)
        
    def __getUserLastMessageIDCheckInput(self, user_id):
        self.__checkUserID(user_id)


    def __getLastToAllMessageID(self):
        ret = db_main.getHandle().selectQuery("select max(message_id) as max from user_messages where user_id is null")
        if ret and ret[0]["max"] != None:
            return ret[0]["max"]
        else:
            return -1


    def __getLastMessageIDForUser(self, user_id):
        ret = db_main.getHandle().selectQuery("select max(message_id) as max from user_messages where user_id = %s"%user_id)
        if ret and ret[0]["max"] != None:
            return ret[0]["max"]
        else:
            return -1
