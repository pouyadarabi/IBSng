from core.group import group_main
class AttributeHandler:
    def __init__(self,attr_updater_name):
        """
            attr_handler_name: name string representation of info holder we generate
        """
        self.attr_handler_name = attr_updater_name
        self.attr_holders = []
        self.attr_searchers = []

    def getName(self):
        return self.attr_handler_name

    ###############################################
    def registerAttrUpdaterClass(self,attr_updater_class,change_attr_list):
        """
            register "attr_updater_class" 
            attr_updater_class changeInit method will be called with values of "change_attr_list" as arguments
            if you use this method --DONT-- override method getattrUpdater
        """
        self.attr_updater_class=attr_updater_class
        self.attr_updater_change_arg_attrs=change_attr_list

    def getAttrUpdater(self,attr_name,attrs,action):
        """
            attr_name(string): attribute name we encountered and we want attr updater for this attribute
                               and all other relevant attributes
            attrs(dic or list): dic of attributes for "change" action, and list of attribute for "delete"
            action(string): should be "change" or "delete". 
        """
        
        attr_updater=self.attr_updater_class(self.getName())
        if action=="change":
            arg_list=map(lambda x:attrs[x],self.attr_updater_change_arg_attrs)
            apply(attr_updater.changeInit,arg_list)
        else:
            attr_updater.deleteInit()
        return attr_updater

    #########################################################
    def registerAttrHolderClass(self,attr_holder_class,holder_attrs):
        """
            register a attr holder for this handler
            attr_holder_class(Class): the class to be registered
            holder_attrs(list): list of attributes that will be passed to initializer of attr_holder
        """
        self.attr_holders.append((attr_holder_class,holder_attrs))

    def getAttrHolder(self,attr_name,attrs):
        """
            attr_name(string): attribute name we encountered and we want attr holder for this attribute
                               and all other relevant attributes
            attrs(dic or list): dic of attributes 
        """
        (attr_holder_class,attr_holder_attrs)=self.__findAttrHolder(attr_name)
        arg_list=map(lambda x:attrs[x],attr_holder_attrs)
        return apply(attr_holder_class,arg_list)

    def __findAttrHolder(self,attr_name):
        for (attr_holder_class,holder_attrs) in self.attr_holders:
            if attr_name in holder_attrs:
                return (attr_holder_class,holder_attrs)

        return (None,None)
    ##########################################################
    def registerAttrSearcherClass(self,attr_searcher):
        """
            register an attr_searcher class
        """
        self.attr_searchers.append(attr_searcher)

    def getAttrSearchers(self):
        return self.attr_searchers

class UserAttributes:
    def __init__(self,attributes,group_id):
        """
            attributes(dic): set of user attributes in format {attr_name:attr_value}
            group_id(int): Group ID, that will be asked, if we don't have an attribute
        """
        self.attributes=attributes
        self.group_id=group_id

    def __getitem__(self,key):
        return self.getAttr(key)
    
    def __getGroupObj(self):
        """
            maybe group attributes changed during 
        """
        return group_main.getLoader().getGroupByID(self.group_id)
    
    def getAttr(self,attr_name):
        if self.userHasAttr(attr_name):
            return self.attributes[attr_name]
        
        return self.__getGroupObj().getAttr(attr_name) 

    def setAttr(self,attr_name,attr_value):
        """
            set "attr_name" value to "attr_value" in loaded object
            use this with caution, this may lead to database inconsistency
        """
        assert(not self.attributes.has_key(attr_name))
        self.attributes[attr_name]=attr_value
            

    def userHasAttr(self,attr_name):
        return self.attributes.has_key(attr_name)
        
    def hasAttr(self,attr_name):
        return self.userHasAttr(attr_name) or self.__getGroupObj().hasAttr(attr_name)
    
    def getAllAttrs(self):
        return self.attributes
