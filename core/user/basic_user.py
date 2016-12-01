from core.group import group_main
from core.admin import admin_main
from core.lib.date import AbsDate
from core.user import user_main
from core.ibs_exceptions import *

class BasicUser:
    """
        Basic user contains user basic information. It's a part of LoadedUser class
    """
    def __init__(self,user_id,owner_id,credit,group_id,creation_date):
        """
            user_id(integer): user id of this user
            owner_id(integer): owner id of this user
            credit(float): credit amount of user
            group_id(integer): group id of this user
            creation_date(str): timestamp representation of creation date
        """
        self.user_id=user_id
        self.owner_id=owner_id
        self.credit=credit
        self.group_id=group_id
        self.creation_date=creation_date

    def getUserID(self):
        return self.user_id

    def getOwnerObj(self):
        try:
            return admin_main.getLoader().getAdminByID(self.owner_id)
        except GeneralException:
            toLog("Can't load owner object with id %s, using system..."%self.owner_id, LOG_ERROR)
            return admin_main.getLoader().getAdminByID(0)

    def getGroupObj(self):
        return group_main.getLoader().getGroupByID(self.group_id)

    def getGroupID(self):
        return self.group_id

    def getInitialCredit(self):
        return self.credit

    def getCredit(self):
        user_obj=user_main.getOnline().getUserObj(self.getUserID())
        if user_obj==None:
            return self.getInitialCredit()
        else:
            return user_obj.calcCurrentCredit()

    def getInfo(self,date_type="gregorian"):
        """
            return a dic containing Basic User Information
        """
        return {"user_id":self.user_id,
                "owner_id":self.owner_id,
                "credit":self.getCredit(),
                "group_id":self.group_id,
                "creation_date":AbsDate(self.creation_date,"gregorian").getDate(date_type),
                "group_name":self.getGroupObj().getGroupName(),
                "owner_name":self.getOwnerObj().getUsername()
                }

