<?php
require_once("../inc/init.php");
require_once(IBSINC."user.php");
require_once(IBSINC."user_face.php");
require_once(IBSINC."report_lib.php");
require_once(IBSINC."report.php");

needAuthType(NORMAL_USER_AUTH_TYPE,VOIP_USER_AUTH_TYPE);

$smarty=new IBSSmarty();

if(isInRequest("show"))
    intSetReport($smarty);

intShowCreditChanges($smarty);

function intShowCreditChanges(&$smarty)
{
    $smarty->display("user/".getLang()."/credit_log.tpl");
}


function intSetReport(&$smarty)
{
    $do_empty=TRUE;
    $smarty->assign("show_report",TRUE);
    $conds=collectConditions();
    $report_helper=new ReportHelper();
    $req=new GetCreditChanges($conds,
                            $report_helper->getFrom(),
                            $report_helper->getTo(),
                            "change_time",
                            $report_helper->getDesc());
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $result=$resp->getResult();
        $report=$result["report"];
        $total_rows=$result["total_rows"];
        $total_per_user_credit=$result["total_per_user_credit"];
        $total_admin_credit=$result["total_admin_credit"];
        $do_empty=FALSE;
    }
    else
        $resp->setErrorInSmarty($smarty);
        
    if($do_empty)
    {
        $report=array();
        $total_rows=0;
        $total_per_user_credit=0;
        $total_admin_credit=0;
    }
    $smarty->assign_by_ref("report",$report);
    $smarty->assign("total_rows",$total_rows);
    $smarty->assign("total_per_user_credit",$total_per_user_credit);
    $smarty->assign("total_admin_credit",$total_admin_credit);
}

function collectConditions() 
{ 
    $collector=new ReportCollector();
    $collector->addToCondsFromRequest(TRUE,"change_time_from","change_time_from_unit");
    $collector->addToCondsFromRequest(TRUE,"change_time_to","change_time_to_unit");

    $collector->addToCondsFromRequest(FALSE,"show_total_per_user_credit");


    return $collector->getConds();    
}





?>
