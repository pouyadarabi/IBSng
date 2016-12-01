<?php
require_once("init.php");
require_once("report_lib.php");


class GetOnlineUsers extends Request
{
    function GetOnlineUsers($normal_sort_by, $normal_desc, $voip_sort_by, $voip_desc, $conds)
    {
        parent::Request("report.getOnlineUsers",array("normal_sort_by"=>$normal_sort_by,
                                                      "normal_desc"=>$normal_desc,
                                                      "voip_sort_by"=>$voip_sort_by,
                                                      "voip_desc"=>$voip_desc,
                                                      "conds"=>$conds));
    }
}

class GetConnections extends Request
{
    function GetConnections($conds,$from,$to,$sort_by,$desc)
    {
        parent::Request("report.getConnections",array("conds"=>$conds,
                                                      "from"=>$from,
                                                      "to"=>$to,
                                                      "sort_by"=>$sort_by,
                                                      "desc"=>$desc));
    }    
}

class GetDurations extends Request
{
    function GetDurations($conds)
    {
        parent::Request("report.getDurations",array("conds"=>$conds));
    }    
}

class GetGroupUsages extends Request
{
    function GetGroupUsages($conds)
    {
        parent::Request("report.getGroupUsages",array("conds"=>$conds));
    }    
}

class GetRasUsages extends Request
{
    function GetRasUsages($conds)
    {
        parent::Request("report.getRasUsages",array("conds"=>$conds));
    }    
}

class GetAdminUsages extends Request
{
    function GetAdminUsages($conds)
    {
        parent::Request("report.getAdminUsages",array("conds"=>$conds));
    }    
}

class GetVoIPDisconnectCausesCount extends Request
{
    function GetVoIPDisconnectCausesCount($conds)
    {
        parent::Request("report.getVoIPDisconnectCauses",array("conds"=>$conds));
    }    
}

class GetSuccessfulCounts extends Request
{
    function GetSuccessfulCounts($conds)
    {
        parent::Request("report.getSuccessfulCounts",array("conds"=>$conds));
    }    
}

class GetCreditChanges extends Request
{
    function GetCreditChanges($conds,$from,$to,$sort_by,$desc)
    {
        parent::Request("report.getCreditChanges",array("conds"=>$conds,
                                                      "from"=>$from,
                                                      "to"=>$to,
                                                      "sort_by"=>$sort_by,
                                                      "desc"=>$desc));
    }    
}

class GetUserAuditLogs extends Request
{
    function GetUserAuditLogs($conds,$from,$to,$sort_by,$desc)
    {
        parent::Request("report.getUserAuditLogs",array("conds"=>$conds,
                                                      "from"=>$from,
                                                      "to"=>$to,
                                                      "sort_by"=>$sort_by,
                                                      "desc"=>$desc));
    }    
}

class GetAdminDepositChangeLogs extends Request
{
    function GetAdminDepositChangeLogs($conds,$from,$to,$sort_by,$desc)
    {
        parent::Request("report.getAdminDepositChangeLogs",array("conds"=>$conds,
                                                      "from"=>$from,
                                                      "to"=>$to,
                                                      "sort_by"=>$sort_by,
                                                      "desc"=>$desc));
    }    
}


class DeleteReports extends Request
{
    function DeleteReports($table, $date, $date_unit)
    {
        parent::Request("report.delReports",array("table"=>$table,
                                                  "date"=>$date,
                                                  "date_unit"=>$date_unit));
    }    
}

class AutoCleanReports extends Request
{
    function AutoCleanReports($connection_log_clean, $connection_log_unit,
                              $credit_change_clean, $credit_change_unit,
                              $user_audit_log_clean, $user_audit_log_unit,
                              $snapshots_clean, $snapshots_unit,
                              $web_analyzer_clean, $web_analyzer_unit)
    {
        parent::Request("report.autoCleanReports",array("connection_log_clean"=>$connection_log_clean,
                                                        "connection_log_unit"=>$connection_log_unit,
                                                        "credit_change_clean"=>$credit_change_clean,
                                                        "credit_change_unit"=>$credit_change_unit,
                                                        "user_audit_log_clean"=>$user_audit_log_clean,
                                                        "user_audit_log_unit"=>$user_audit_log_unit,
                                                        "snapshots_clean"=>$snapshots_clean,
                                                        "snapshots_unit"=>$snapshots_unit,
                                                        "web_analyzer_clean"=>$web_analyzer_clean,
                                                        "web_analyzer_unit"=>$web_analyzer_unit));
    }    
}

class GetReportAutoCleanDates extends Request
{
    function GetReportAutoCleanDates()
    {
        parent::Request("report.getAutoCleanDates",array());
    }    
}

class GetWebAnalyzerReport extends Request
{
    function GetWebAnalyzerReport($conds,$from,$to,$sort_by,$desc)
    {
        parent::Request("web_analyzer.getWebAnalyzerLogs",array("conds"=>$conds,
                                                                "from"=>$from,
                                                                "to"=>$to,
                                                                "sort_by"=>$sort_by,
                                                                "desc"=>$desc));
    }    
}

class GetTopVisitedReport extends Request
{
    function GetTopVisitedReport($conds, $from,$to)
    {
        parent::Request("web_analyzer.getTopVisited",array("conds"=>$conds,
                                                                "from"=>$from,
                                                                "to"=>$to
                                                                ));
    }  
}

class GetConsoleBuffer extends Request
{
    function GetConsoleBuffer()
    {
        parent::Request("log_console.getConsoleBuffer",array());
    }    
}

class GetInOutUsages extends Request
{
    function GetInOutUsages($conds,$from,$to)
    {
        parent::Request("report.getInOutUsages",array("conds"=>$conds,
                                                      "from"=>$from,
                                                      "to"=>$to));
    }    
}

class GetCreditUsages extends Request
{
    function GetCreditUsages($conds,$from,$to)
    {
        parent::Request("report.getCreditUsages",array("conds"=>$conds,
                                                      "from"=>$from,
                                                      "to"=>$to));
    }    
}

class GetDurationUsages extends Request
{
    function GetDurationUsages($conds,$from,$to)
    {
        parent::Request("report.getDurationUsages",array("conds"=>$conds,
                                                      "from"=>$from,
                                                      "to"=>$to));
    }    
}


?>