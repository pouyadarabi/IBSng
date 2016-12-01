<?php

require_once("../../inc/init.php");
require_once(IBSINC."report.php");


needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
session_write_close();

if(isInRequest("auto_clean_submit"))
    intAutoClean($smarty);

else if(isInRequest("delete_connection_logs","connection_log_date","connection_log_unit"))
    intDelTable($smarty,"connection_log",$_REQUEST["connection_log_date"],$_REQUEST["connection_log_unit"]);

else if(isInRequest("delete_credit_changes","credit_change_date","credit_change_unit"))
    intDelTable($smarty,"credit_change",$_REQUEST["credit_change_date"],$_REQUEST["credit_change_unit"]);

else if(isInRequest("delete_user_audit_logs","user_audit_log_date","user_audit_log_unit"))
    intDelTable($smarty,"user_audit_log",$_REQUEST["user_audit_log_date"],$_REQUEST["user_audit_log_unit"]);

else if(isInRequest("delete_snapshots","snapshots_date","snapshots_unit"))
    intDelTable($smarty,"snapshots",$_REQUEST["snapshots_date"],$_REQUEST["snapshots_unit"]);

else if(isInRequest("delete_web_analyzer","web_analyzer_date","web_analyzer_unit"))
    intDelTable($smarty,"web_analyzer_log",$_REQUEST["web_analyzer_date"],$_REQUEST["web_analyzer_unit"]);

else
    face($smarty);

/////////////////////////
function intAutoClean(&$smarty)
{
    list($con_date,$con_unit) = getDatesForTable("connection_log");
    list($credit_date,$credit_unit) = getDatesForTable("credit_change");
    list($ua_date,$ua_unit) = getDatesForTable("user_audit_log");
    list($snp_date,$snp_unit) = getDatesForTable("snapshots");
    list($web_analyzer_date,$web_analyzer_unit) = getDatesForTable("web_analyzer");

    $req=new AutoCleanReports($con_date,$con_unit,$credit_date,$credit_unit,$ua_date,$ua_unit,$snp_date,$snp_unit,
                                $web_analyzer_date, $web_analyzer_unit);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("auto_clean_commit_success",TRUE);
    else
        $resp->setErrorInSmarty($smarty);

    face($smarty);
}

function getDatesForTable($table_name)
{// return date,unit for table_name from request
    if(isInRequest("auto_clean_{$table_name}"))
        return array(requestVal("{$table_name}_date",0),requestVal("{$table_name}_unit","Seconds"));
    else
        return array(0,"Seconds");
}
///////////////////////////////////////////
function intDelTable(&$smarty,$table_name,$date,$date_unit)
{
    $req = new DeleteReports($table_name,$date,$date_unit);
    $resp = $req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("manual_delete_success",TRUE);
    else
        $resp->setErrorInSmarty($smarty);

    face($smarty);
}

///////////////////////////////////////////
function face(&$smarty)
{
    intAssignAutoCleanDates($smarty);
    $smarty->display("admin/report/clean_reports.tpl");
}

function intAssignAutoCleanDates(&$smarty)
{
    $req = new GetReportAutoCleanDates();
    $resp = $req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign_array($resp->getResult());
    else
        $resp->setErrorInSmarty($smarty);
}

?>