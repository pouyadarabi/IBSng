import copy
from core.ibs_exceptions import *
from core.errors import errorText
from core.user.attr_updater import AttrUpdaterContainer
from core.user.search_user import SearchUserHelper

class AttributeManager:
    def __init__(self):
        self.change_attr_handlers={}
        self.delete_attr_handlers={}
        self.parse_attr_handlers={}
        self.post_parse_methods=[]
        self.all_handlers=[]

    def registerHandler(self,handler_obj,change_attr_list=[],delete_attr_list=[],parse_attr_list=[],post_parse_methods=[]):
        """
            handler_obj(AttributeHandler instance): Attribute Handler that generate an attr_updater and attr_holder
            change_attr_list(list of strs): list of attributes for change action, one would be enough
            delete_attr_list(list of strs): list of attributes for delete action, one would be enough
            parse_attr_list(list of strs): list of attributes that this attr handle can parse, one attribute per parser
            post_parse_methods(list of callable objects): call these methods after parsing is done. 
                                               proto type of method is "method(_id,_type,raw_attrs,parsed_attrs,date_type)" where parsed_attrs is a dic
                                               of parsed attrs and raw_attrs is raw attributes. method
                                               may change parsed_attrs but not raw_attrs

            register a attr_handler, that will be called when we encounter an attribute in attr_list
        """
        if handler_obj:
            self.all_handlers.append(handler_obj)
            
        for attr in change_attr_list:
            if self.change_attr_handlers.has_key(attr):
                raise IBSException(errorText("USER","DUPLICATE_ATTR_REGISTRATION")%attr)
            self.change_attr_handlers[attr]=handler_obj

        for attr in delete_attr_list:
            if self.delete_attr_handlers.has_key(attr):
                raise IBSException(errorText("USER","DUPLICATE_ATTR_REGISTRATION")%attr)
            self.delete_attr_handlers[attr]=handler_obj

        for attr in parse_attr_list:
            if self.parse_attr_handlers.has_key(attr):
                raise IBSException(errorText("USER","DUPLICATE_ATTR_REGISTRATION")%attr)
            self.parse_attr_handlers[attr]=handler_obj

        self.post_parse_methods += post_parse_methods
#########################################
    def __getAttrHandlerForUpdater(self,attr_name,action):
        try:
            if action=="change":
                return self.change_attr_handlers[attr_name]
            elif action=="delete":
                return self.delete_attr_handlers[attr_name]
        except KeyError:
            pass
        
    def getAttrUpdaters(self,attrs,action):
        """
            attrs(dic or list): dic of all attributes in format name:value
            action(string): should be "change" ro "delete"
            return an AttrUpdaterContainer instance containing attrs attrUpdaters
        """
        attr_updaters=AttrUpdaterContainer()
        for attr_name in attrs:
            handler=self.__getAttrHandlerForUpdater(attr_name,action)
            if handler !=None and not attr_updaters.hasName(handler.getName()):
                attr_updaters.addNew(handler.getAttrUpdater(attr_name,attrs,action))
        return attr_updaters

##########################################
    def __getAttrHandlerForHolder(self,attr_name):
        try:
            return self.parse_attr_handlers[attr_name]
        except KeyError:
            return None

    def getAttrHolders(self,attrs):
        """
            attrs(dic or list): dic of all attributes in format name:value
            return a list of attr holders for attrs 
        """
        attr_holders=[]
        for attr_name in attrs:
            handler=self.__getAttrHandlerForHolder(attr_name)
            if handler!=None:
                attr_holders.append(handler.getAttrHolder(attr_name,attrs))
        return attr_holders

    def parseAttrs(self,_id,_type,attrs,date_type):
        """
            return a dic of attrs containing the parsed attributes of attrs
            _id(integer): id of group or user
            _type(str): "group" or "user"
        """
        attrs=copy.copy(attrs) #make sure we don't change user/group attributes
        parsed_attrs=copy.copy(attrs)
        attr_holders=self.getAttrHolders(parsed_attrs)
        for attr_holder in attr_holders:
            attr_holder.setDateType(date_type)
            parsed_attrs.update(attr_holder.getParsedDic())

        self.__callPostParseMethods(_id,_type,attrs,parsed_attrs,date_type)

        return parsed_attrs

    def __callPostParseMethods(self,_id,_type,raw_attrs,parsed_attrs,date_type):
        for method in self.post_parse_methods:
            apply(method,[_id,_type,raw_attrs,parsed_attrs,date_type])
#############################################
    def runAttrSearchers(self,conditions,admin_obj):
        """
            create attr searcher instances and execute their "run" method
        """
        search_helper=SearchUserHelper(conditions,admin_obj,"admin")
        attr_searchers=self.__getAllAttrSearchers(search_helper)
        map(lambda x:apply(getattr(x,"run")),attr_searchers)
        return search_helper

    def __getAllAttrSearchers(self, search_helper):
        attr_searchers=[]

        for handler in self.all_handlers:
            for attr_searcher in handler.getAttrSearchers():
                attr_searchers.append(attr_searcher(search_helper))
                
        return attr_searchers
    
    