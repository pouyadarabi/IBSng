from core.user import user_main,attribute
from core.user.attr_searcher import AttrSearcher
from core.lib.multi_strs import MultiStr


def init():
    user_main.getAttributeManager().registerHandler(CreditAttrHandler())

class CreditAttrSearcher(AttrSearcher):
    def run(self):
        users_table=self.getSearchHelper().getTable("users")
        users_table.ltgtSearch(self.getSearchHelper(),
                                   "credit",
                                   "credit_op",
                                   "credit"
                                  )

class CreditAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,"credit")
        self.registerAttrSearcherClass(CreditAttrSearcher)
