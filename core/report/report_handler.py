from core.report import connection_usage
from core.server import handler
from core.ibs_exceptions import *
from core.errors import errorText
from core.report import online,connection,credit,audit_log,admin_deposit_change_log
from core.lib.date import RelativeDate
from core.lib import report_lib
from core.report import report_main, onlines_filter

class ReportHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"report")
        self.registerHandlerMethod("getOnlineUsers")

        self.registerHandlerMethod("getConnections")
        self.registerHandlerMethod("getDurations")
        self.registerHandlerMethod("getGroupUsages")
        self.registerHandlerMethod("getRasUsages")
        self.registerHandlerMethod("getVoIPDisconnectCauses")
        self.registerHandlerMethod("getSuccessfulCounts")
        self.registerHandlerMethod("getAdminUsages")

        self.registerHandlerMethod("getInOutUsages")
        self.registerHandlerMethod("getCreditUsages")
        self.registerHandlerMethod("getDurationUsages")

        self.registerHandlerMethod("getCreditChanges")
        self.registerHandlerMethod("getUserAuditLogs")
        self.registerHandlerMethod("getAdminDepositChangeLogs")

        self.registerHandlerMethod("delReports")
        self.registerHandlerMethod("autoCleanReports")
        self.registerHandlerMethod("getAutoCleanDates")


    ####################################################
    def getOnlineUsers(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("normal_sort_by", "normal_desc", "voip_sort_by", "voip_desc", "conds")
        requester=request.getAuthNameObj()
        if requester.hasPerm("SEE ONLINE USERS"):
            admin_perm_obj=requester.getPerms()["SEE ONLINE USERS"]
        elif requester.isGod():
            admin_perm_obj=None
        else:
            raise GeneralException(errorText("GENERAL","ACCESS_DENIED"))

        filter_manager = onlines_filter.createFilterManager(report_lib.fixConditionsDic(request["conds"]))
        
        normal_onlines, voip_onlines = online.getFormattedOnlineUsers(request.getDateType(), filter_manager)
        normal_onlines, voip_onlines = online.sortOnlineUsers(normal_onlines, voip_onlines,
                                       (request["normal_sort_by"], request["normal_desc"]),
                                       (request["voip_sort_by"], request["voip_desc"]))
        
        if admin_perm_obj!=None and admin_perm_obj.isRestricted():
            normal_onlines=filter(lambda online_dic:online_dic["owner_id"]==requester.getAdminID(),normal_onlines)
            voip_onlines=filter(lambda online_dic:online_dic["owner_id"]==requester.getAdminID(),voip_onlines)

        return (normal_onlines, voip_onlines)
        
    #############################################
    def getConnections(self,request):
        request.needAuthType(request.ADMIN,request.NORMAL_USER,request.VOIP_USER)
        request.checkArgs("conds","from","to","sort_by","desc")
        requester=request.getAuthNameObj()
        conds=report_lib.fixConditionsDic(request["conds"])
        
        if request.hasAuthType(request.ADMIN):
            requester.canDo("SEE CONNECTION LOGS")
            role = "admin"
        elif request.hasAuthType(request.NORMAL_USER) or request.hasAuthType(request.VOIP_USER):
            conds["user_ids"]=str(requester.getUserID())
            role = "user"
        
        searcher=connection.ConnectionSearcher(conds,requester,role)
        
        connections = searcher.getConnectionLog(request["from"],request["to"],request["sort_by"],request["desc"],request.getDateType())
        
        if role == "user":
            connections = self.__filterConnectionsForUser(connections)
        
        return connections

    def __filterConnectionsForUser(self,connections):
        """
            filter unnecessary attributes from details, for user reports.
            Some attributes may expose system informations, so we show only trusted attributes
            This can be moved to database for better perfomance, but it's really server handlers job
        """
        trusted_attrs=["caller_id","prefix_name","mac","persistent_lan","kill_reason","voip_username","username","remote_ip","bytes_in","bytes_out","station_ip","called_number"]
        for row in connections["report"]:
            details=[]
            for attr_tuple in row["details"]:
                if attr_tuple[0] in trusted_attrs:
                    details.append(attr_tuple)
            row["details"]=details
        return connections
    ###########################################
    
    def getDurations(self,request):
        request.needAuthType(request.ADMIN,request.NORMAL_USER,request.VOIP_USER)
        request.checkArgs("conds")
        requester=request.getAuthNameObj()
        conds=report_lib.fixConditionsDic(request["conds"])
        
        if request.hasAuthType(request.ADMIN):
            requester.canDo("SEE CONNECTION LOGS")
            role = "admin"
        elif request.hasAuthType(request.NORMAL_USER) or request.hasAuthType(request.VOIP_USER):
            conds["user_ids"]=str(requester.getUserID())
            role = "user"
        
        searcher=connection.ConnectionSearcher(conds,requester,role)
        
        return searcher.getDurations()

    ###########################################
    def __adminConnectionReport(self, request, method_name):
        """
            handle admin connection report. check conds in request
            and call n return method_name of searcher and if everything was ok
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("conds")
        requester=request.getAuthNameObj()
        conds=report_lib.fixConditionsDic(request["conds"])
        requester.canDo("SEE CONNECTION LOGS")
        role = "admin"
        
        searcher=connection.ConnectionSearcher(conds,requester,role)
        return apply(getattr(searcher,method_name),[])


    def getGroupUsages(self,request):
        return self.__adminConnectionReport(request,"getGroupUsages")

    def getRasUsages(self,request):
        return self.__adminConnectionReport(request,"getRasUsages")

    def getVoIPDisconnectCauses(self,request):
        return self.__adminConnectionReport(request,"getVoIPDisconnectCauses")

    def getSuccessfulCounts(self,request):
        return self.__adminConnectionReport(request,"getSuccessfulCounts")

    def getAdminUsages(self,request):
        return self.__adminConnectionReport(request,"getAdminUsages")


    ###########################################
    def getCreditChanges(self,request):
        request.needAuthType(request.ADMIN,request.NORMAL_USER,request.VOIP_USER)
        request.checkArgs("conds","from","to","sort_by","desc")
        requester=request.getAuthNameObj()
        conds=report_lib.fixConditionsDic(request["conds"])

        if request.hasAuthType(request.ADMIN):
            requester.canDo("SEE CREDIT CHANGES")
            role="admin"
        elif request.hasAuthType(request.NORMAL_USER) or request.hasAuthType(request.VOIP_USER):
            conds["user_ids"]=str(requester.getUserID())
            role="user"

        searcher=credit.CreditSearcher(conds,requester,role)
        credit_changes = searcher.getCreditChanges(request["from"],request["to"],request["sort_by"],request["desc"],request.getDateType())
    
        if role == "user":
            credit_changes = self.__filterCreditChangesForUser(credit_changes)
        
        return credit_changes
        

    def __filterCreditChangesForUser(self,credit_changes):
        for row in credit_changes["report"]:
            del(row["user_ids"])
            del(row["admin_id"])
            del(row["admin_name"])
            del(row["admin_credit"])
            del(row["comment"])
            del(row["remote_addr"])
        return credit_changes

    ##############################################
    
    def getUserAuditLogs(self,request):
        """
            return user audit logs, based on request["conds"] conditions
            return value is a dic in format {"total_rows":,"report":[]}
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("conds", "from", "to", "sort_by", "desc")
        requester = request.getAuthNameObj()
        conds = report_lib.fixConditionsDic(request["conds"])

        requester.canDo("SEE USER AUDIT LOGS")
        role = "admin"

        searcher = audit_log.UserAuditLogSearcher(conds, requester,role)
        audit_log_report = searcher.getUserAuditLogs(request["from"],
                                                     request["to"],
                                                     request["sort_by"],
                                                     request["desc"],
                                                     request.getDateType())
    
        return audit_log_report

    ################################################

    def getAdminDepositChangeLogs(self, request):
        """
            return admin change deposit logs
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("conds", "from", "to", "sort_by", "desc")
        requester = request.getAuthNameObj()
        
        conds = report_lib.fixConditionsDic(request["conds"])

        requester.canDo("CHANGE ADMIN DEPOSIT")
        role = "admin"

        searcher = admin_deposit_change_log.AdminDepositChangeLogsSearcher(conds, requester,role)
        audit_log_report = searcher.getAdminDepositChangeLogs(request["from"],
                                                     request["to"],
                                                     request["sort_by"],
                                                     request["desc"],
                                                     request.getDateType())

        return audit_log_report

    ################################################

    def delReports(self,request):
        """
            del reports of table, before date
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("table","date","date_unit")
        requester = request.getAuthNameObj()
        requester.canDo("DELETE REPORTS")
        
        report_main.getReportCleaner().cleanLogsFromSeconds(request["table"], 
                                                 RelativeDate(request["date"],request["date_unit"]).getDateSeconds() )

    ################################################
    def autoCleanReports(self, request):
        """
            auto clean the tables.
            if value is zero, it means that auto cleaning for that table is disabled
            unit should always be valid , even for zero values
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("connection_log_clean","connection_log_unit",
                          "credit_change_clean","credit_change_unit",
                          "user_audit_log_clean","user_audit_log_unit",
                          "snapshots_clean","snapshots_unit",
                          "web_analyzer_clean", "web_analyzer_unit")
                          
        requester = request.getAuthNameObj()
        requester.canDo("DELETE REPORTS")
        
        report_main.getReportCleaner().updateAutoCleanStates({"connection_log":(request["connection_log_clean"],request["connection_log_unit"]),
                                                              "credit_change":(request["credit_change_clean"],request["credit_change_unit"]),
                                                              "user_audit_log":(request["user_audit_log_clean"],request["user_audit_log_unit"]),
                                                              "snapshots":(request["snapshots_clean"],request["snapshots_unit"]),
                                                              "web_analyzer_log":(request["web_analyzer_clean"],request["web_analyzer_unit"])
                                                              })

    #################################################
    def getAutoCleanDates(self, request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("DELETE REPORTS")
        
        return report_main.getReportCleaner().getAutoCleanDates()

    ##################################################

    def __connectionUsageHandler(self, request, searcher_method):
        request.needAuthType(request.ADMIN)
        request.checkArgs("conds","from","to")
        requester=request.getAuthNameObj()
        conds=report_lib.fixConditionsDic(request["conds"])
        

        requester.canDo("SEE CONNECTION LOGS")
        role = "admin"
        
        searcher=connection_usage.ConnectionUsageSearcher(conds,requester,role)
        
        result = getattr(searcher,searcher_method)(request["from"],
                                                   request["to"])
        
        return result
        
    def getInOutUsages(self,request):
        return self.__connectionUsageHandler(request, "getInOutUsages")

    def getCreditUsages(self,request):
        return self.__connectionUsageHandler(request, "getCreditUsages")
        
    def getDurationUsages(self,request):
        return self.__connectionUsageHandler(request, "getDurationUsages")
