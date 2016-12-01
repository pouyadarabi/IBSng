from core.server import handler
from core.stats import stat_main
from core.lib.sort import SortedDic


class StatHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"stat")
        self.registerHandlerMethod("getStatistics")

    def getStatistics(self, request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("GOD")

        
        stat_dic = stat_main.getStatKeeper().getStats()

        sorted_dic=SortedDic(stat_dic)
        sorted_dic.sortByKey(False)
        return sorted_dic.getList()
