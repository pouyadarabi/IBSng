class SearchGroup:
    def __init__(self,op=""):
        self.__groups=[]
        self.setOperator(op)

    def setOperator(self,operator):
        """
            set operator between each member of this group. Normally it should be "or" or "and"
        """
        self.__operator=operator
    
    def addGroup(self,group):
        """
            add a new group to be member of this group
            group can be an string or another group object.
            group objects would be queried to reach a group without another group_obj builtin
        """
        self.__groups.append(group)

    def getConditionalClause(self):
        """
            build an conditional clause based on member groups
        """
        if len(self.__groups)==0:
            return ""
        str_groups=map(self.__getConditionStr,self.__groups)
        return " (%s) "%(" %s "%self.__operator).join(str_groups)
    
    def isEmpty(self):
        return len(self.__groups)==0

    def __getConditionStr(self,group_obj):
        if isinstance(group_obj,SearchGroup):
            return group_obj.getConditionalClause()
        else:
            return group_obj

