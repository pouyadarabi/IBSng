from core.db.ibs_query import IBSQuery
from core.db import ibs_db,db_main
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib import iplib
from core.lib.general import *

class CreditChangeLogActions:
    CREDIT_CHANGE_ACTIONS={"ADD_USER":1,"CHANGE_CREDIT":2,"DEL_USER":3}
    CREDIT_CHANGE_ACTIONS_REV={1:"Add User",2:"Change Credit",3:"Delete User"}


    def logCreditChangeQuery(self,action,admin_id,user_ids,per_user_credit,admin_credit,remote_address,comment):
        """
        
            log credit change to credit_change table
            action(string): action that credit changed in, should be referenced by self.CREDIT_CHANGE_ACTIONS
            admin_id(integer): Admin issueing the credit change for user
            user_ids(list of integers): user ids that credit being changed
            per_user_credit(float): credit change for each of users
            admin_credit(float): credit admin spent, equals to count of users * per_user_credit
            remote_address(str): remote ip of admin while changing credit
            comment(str): comment of credit change
        """
        self.__creditChangeCheckInput(remote_address,comment)
        change_id=self.__getNewCreditChangeID()
        ibs_query=IBSQuery()
        ibs_query=ibs_db.createInsertQuery("credit_change",{"credit_change_id":change_id,
                                                        "action":self.getActionID(action),
                                                        "admin_id":admin_id,
                                                        "per_user_credit":per_user_credit,
                                                        "admin_credit":admin_credit,
                                                        "remote_addr":dbText(remote_address),
                                                        "comment":dbText(comment)
                                                        })
        

        for user_id in user_ids:
            ibs_query+=ibs_db.createInsertQuery("credit_change_userid",{"user_id":user_id,
                                                                    "credit_change_id":change_id})
        return ibs_query

    def __getNewCreditChangeID(self):
        """
            return a new unique credit change id
        """
        return db_main.getHandle().seqNextVal("credit_change_id")

    def __creditChangeCheckInput(self,remote_address,credit_change_comment):
        """
            check credit changed related inputs and raise exception on errors
        """
        if iplib.checkIPAddrWithoutMask(remote_address)==0:
            raise GeneralException(errorText("GENERAL","INVALID_IP_ADDRESS")%remote_address)

    def getActionID(self,action):
        return self.CREDIT_CHANGE_ACTIONS[action]

    def getIDActionText(self,action_id):
        return self.CREDIT_CHANGE_ACTIONS_REV[action_id]
        