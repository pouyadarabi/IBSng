from core.server import handler
from core.web_analyzer import web_analyzer_main
from core.web_analyzer import web_analyzer_report
from core.ibs_exceptions import *
from core.lib import report_lib
from core import defs


class WebAnalyzerHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self, "web_analyzer")
        self.registerHandlerMethod("logAnalysis")
        self.registerHandlerMethod("getWebAnalyzerLogs")
        self.registerHandlerMethod("getTopVisited")
        
        
    def __checkWebAnalyzerAuth(self, request):
        """
            Checks for valid ip and password in request received from
            Web Analyzer Clients, if confirmed ...
            Clients are defined by admin
        """
        request.checkArgs("web_analyzer_password")
        
        if request["web_analyzer_password"] != defs.WEB_ANALYZER_PASSWORD:
            request.raiseAccessDenied()


########################## Handler Methods  ###############
    def logAnalysis(self, request):
        self.__checkWebAnalyzerAuth(request)
        #client_id = self.__checkWebAnalyzerAuth(request)
        request.checkArgs('log_dict')
        return web_analyzer_main.getAnalyzerLogger().logAnalysis(request['log_dict'])

    def getWebAnalyzerLogs(self, request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("conds", "from", "to", "sort_by", "desc")
        requester = request.getAuthNameObj()
        conds = report_lib.fixConditionsDic(request["conds"])
    
        requester.canDo("SEE WEB ANALYZER LOGS")
        role = "admin"
        
        searcher = web_analyzer_report.WebAnalyzerSearcher(conds, requester, role)
        totals, report =  searcher.getWebAnalyzerLogs(request["from"],
                                            request["to"],
                                            request["sort_by"],
                                            request["desc"],
                                            request.getDateType())
        
        totals = self.__convTotalsToFloat(totals)
        
        return (totals, report)

    def __convTotalsToFloat(self, totals):
        for name in totals:
            totals[name] = float(totals[name])

        return totals

    def getTopVisited(self, request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("conds", "from", "to")
        requester = request.getAuthNameObj()
        conds = report_lib.fixConditionsDic(request["conds"])
        
        requester.canDo("SEE WEB ANALYZER LOGS")
        role = "admin"
        
        searcher = web_analyzer_report.WebAnalyzerSearcher(conds, requester, role)
        return searcher.getTopVisited(request["from"],
                                      request["to"],
                                      request.getDateType())
