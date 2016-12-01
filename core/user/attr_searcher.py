from core.lib.general import *

class AttrSearcher:
    def __init__(self,search_helper):
        self.search_helper=search_helper

    def getSearchHelper(self):
        return self.search_helper

    def run(self):
        """
            AttrSearchers should override this method and do the real job here
            by updating search_helper groups and addTable
        """
        pass

    def getUserAndGroupAttrsTable(self):
        return (self.getSearchHelper().getTable("user_attrs"),
                self.getSearchHelper().getTable("group_attrs"))
        

    def exactSearchOnUserAndGroupAttrs(self,cond_key,attr_db_name,value_parser_method=None):
        for table in self.getUserAndGroupAttrsTable():
            table.exactSearch(self.getSearchHelper(),
                              cond_key,
                              attr_db_name,
                              value_parser_method
                             )

    def ltgtSearchOnUserAndGroupAttrs(self,cond_key,cond_op_key,attr_db_name,value_parser_method=None):
        for table in self.getUserAndGroupAttrsTable():
            table.ltgtSearch(self.getSearchHelper(),
                              cond_key,
                              cond_op_key,
                              attr_db_name,
                              value_parser_method
                             )

    def likeStrSearchOnUserAndGroupAttrs(self,cond_key,cond_op_key,attr_db_name,value_parser_method=None):
        for table in self.getUserAndGroupAttrsTable():
            table.likeStrSearch(self.getSearchHelper(),
                              cond_key,
                              cond_op_key,
                              attr_db_name,
                              value_parser_method
                             )
