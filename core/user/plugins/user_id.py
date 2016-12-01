from core.user import user_main,attribute
from core.user.attr_searcher import AttrSearcher
from core.lib.multi_strs import MultiStr


def init():
    user_main.getAttributeManager().registerHandler(UserIDAttrHandler())

class UserIDAttrSearcher(AttrSearcher):
    def run(self):
        users_table=self.getSearchHelper().getTable("users")
        users_table.ltgtSearch(self.getSearchHelper(),
                                   "user_id",
                                   "user_id_op",
                                   "user_id",
                                   MultiStr
                                  )

class UserIDAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,"user_id")
        self.registerAttrSearcherClass(UserIDAttrSearcher)
