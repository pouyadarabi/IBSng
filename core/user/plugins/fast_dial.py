"""
    Fast Dial, for voip rases that supports it
"""
from core.user import user_plugin,user_main,attribute
from core.admin import admin_main
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.user.attr_holder import AttrHolder
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core import defs

import types

def init():
    user_main.getAttributeManager().registerHandler(FastDialAttrHandler(),["fast_dial"],["fast_dial"],["fast_dial"])
    user_main.getUserPluginManager().register("fast_dial",FastDialUserPlugin,1)
    
    global actions_manager
    actions_manager=FastDialActionsManager()

def getActionsManager():
    return actions_manager

class FastDialUserPlugin(user_plugin.AttrCheckUserPlugin):
    """
        catch called numbers with defs.FASTDIAL_PREFIX and convert them to fast dial entry
    """
    #TODO: FIX IN B BRANCH!
    def __init__(self, user_obj):
        user_plugin.AttrCheckUserPlugin.__init__(self,user_obj,"fast_dial")
        self.__initValues()

    def __initValues(self):
        if self.hasAttr():
            self.fast_dials=self.user_obj.getUserAttrs()["fast_dial"].split(",")
    
    def s_login(self, ras_msg):
        self.__checkRasMsg(ras_msg)
    
    def s_update(self, ras_msg):
        self.__checkRasMsg(ras_msg)

    def _reload(self):
        user_plugin.AttrCheckUserPlugin._reload(self)
        self.__initValues()
    
    def __checkRasMsg(self, ras_msg):
        """
            check and update ras_msg
        """
        if defs.FASTDIAL_PREFIX: #@UndefinedVariable
            if ras_msg.hasAttr("called_number") and ras_msg["called_number"].startswith(defs.FASTDIAL_PREFIX): #@UndefinedVariable
                try:
                    fast_dial_index = int(ras_msg["called_number"][len(defs.FASTDIAL_PREFIX):]) #@UndefinedVariable
                except ValueError:
                    raise GeneralException(errorText("USER_LOGIN","INVALID_FAST_DIAL_INDEX")%ras_msg["called_number"])
                
                try:
                    fast_dial_entry = self.fast_dials[fast_dial_index]
                except IndexError: 
                    raise GeneralException(errorText("USER_LOGIN","INVALID_FAST_DIAL_INDEX")%fast_dial_index)
                
                instance = self.user_obj.getInstanceFromRasMsg(ras_msg)
                instance_info =  self.user_obj.getInstanceInfo(instance)
                instance_info["attrs"]["fast_dial_index"] = fast_dial_index
                
                #called number will be set later by charge plugin
                ras_msg["called_number"] = fast_dial_entry
                ras_msg.getRasObj().setRedirectNumber(ras_msg.getReplyPacket(), fast_dial_entry)
                
        
class FastDialAttrUpdater(AttrUpdater):
    
    def __checkFastDialString(self, fast_dial_numbers):
        
        if len(fast_dial_numbers)!=10:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_FAST_DIAL"))

        for number in fast_dial_numbers:
            if number != "" and not number.isdigit():
                raise GeneralException(errorText("USER_ACTIONS","INVALID_FAST_DIAL_ENTRY")%number)

    def changeInit(self, fast_dial):
        """
            fast_dial should be list of 10 strings representing numbers
        """
        if type(fast_dial)==types.DictType:
            fast_dial=fixXMLRPCList(fast_dial)
            
        self.__checkFastDialString(fast_dial)
        self.useGenerateQuery({"fast_dial":",".join(map(str,fast_dial))}, False)

    def deleteInit(self):
        self.useGenerateQuery(["fast_dial"], False)

class FastDialAttrHolder(AttrHolder):
    def __init__(self, fast_dial):
        self.fast_dial=fast_dial

    def getParsedDic(self):
        return {"fast_dial":self.fast_dial.split(",")}

class FastDialAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,"fast_dial")
        self.registerAttrUpdaterClass(FastDialAttrUpdater,["fast_dial"])
        self.registerAttrHolderClass(FastDialAttrHolder,["fast_dial"])


class FastDialActionsManager:
    def addDestinationToFastDial(self, voip_username, destination, _index):
        """
            add "destination" to fast dial _index of "voip_username"
        """
        self.__addDestinationToFastDialCheckInput(voip_username, destination, _index)
        loaded_user=user_main.getUserPool().getUserByVoIPUsername(voip_username)
        if loaded_user.userHasAttr("fast_dial"):
            fast_dials=loaded_user.getUserAttrs()["fast_dial"].split(",")
        else:
            fast_dials=['' for i in range(10)]
        
        fast_dials[_index]=destination
        
        user_main.getActionManager().updateUserAttrs([loaded_user],
                             admin_main.getLoader().getAdminByName("system"),
                             {"fast_dial":fast_dials},
                             [])
        
    def __addDestinationToFastDialCheckInput(self, voip_username, destination, _index):
        if not destination.isdigit():
            raise GeneralException(errorText("USER_ACTIONS","INVALID_DESTINATION")%destination)
        
        if not isInt(_index) or _index<0 or _index>9: 
            raise GeneralException(errorText("USER_ACTIONS","INVALID_FAST_DIAL_INDEX")%_index)
        
        #voip username will be checked by loading it

    ###############################################
    def getFastDialDestination(self, voip_username, _index):
        """
            return fast dial destination of voip_username and _index
            return an empty string if fast_dial is not set for _index
        """
        loaded_user=user_main.getUserPool().getUserByVoIPUsername(voip_username)
        try:
            return loaded_user.getUserAttrs()["fast_dial"].split(",")[_index]
        except:
            return ""

    #################################################
