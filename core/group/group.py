from core.ibs_exceptions import *
from core.errors import errorText
from core.user import user_main
from core.admin import admin_main

class Group:
    def __init__(self,group_id,group_name,comment,owner_id,attributes):
        self.group_id=group_id
        self.group_name=group_name
        self.comment=comment
        self.owner_id=owner_id
        self.attributes=attributes
        
    def hasAttr(self,attr_name):
        return self.attributes.has_key(attr_name)

    def getAttr(self,attr_name):
        try:
            return self.attributes[attr_name]
        except KeyError:
            raise GeneralException(errorText("GENERAL","ATTR_NOT_FOUND")%attr_name)

    def getGroupName(self):
        return self.group_name

    def getGroupID(self):
        return self.group_id

    def getComment(self):
        return self.comment

    def getOwnerID(self):
        return self.owner_id

    def getAttrs(self):
        return self.attributes

    def getParsedAttrs(self, date_type):
       return user_main.getAttributeManager().parseAttrs(self.getGroupID(),"group",self.getAttrs(),date_type)

    def getInfo(self,date_type):
        return {"group_id":self.getGroupID(),
                "group_name":self.getGroupName(),
                "comment":self.getComment(),
                "owner_id":self.getOwnerID(),
                "owner_name":admin_main.getLoader().getAdminByID(self.getOwnerID()).getUsername(),
                "raw_attrs":self.getAttrs(),
                "attrs":self.getParsedAttrs(date_type)
               }