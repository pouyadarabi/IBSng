<?php

require_once("../inc/init.php");
require_once(IBSINC."report.php");
require_once(IBSINC."message.php");


needAuthType(NORMAL_USER_AUTH_TYPE,VOIP_USER_AUTH_TYPE);
$smarty=new IBSSmarty();

if(isInRequest("delete"))
    intDeleteMessage($smarty,array($_REQUEST["delete"]));
else
    intViewMessages($smarty);

function intDeleteMessage(&$smarty, $message_id)
{
    $req=new DeleteUserMessages($message_id);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("delete_message_success",TRUE);
    else
        $resp->setErrorInSmarty($smarty);
    intViewMessages($smarty);
}


function intViewMessages(&$smarty)
{
    if(isInRequest("show"))
        intSetReport($smarty);
    intAssignVars($smarty);
    $smarty->display("user/".getLang()."/view_messages.tpl");
}

function intAssignVars(&$smarty)
{
    $smarty->assign("order_bys",array("message_id"=>"Message ID",
                                      "post_date"=>"Post Date"));
    $smarty->assign("order_by_default",requestVal("order_by","message_id"));
}

function intSetReport(&$smarty)
{
    $do_empty=TRUE;
    $smarty->assign("show_report",TRUE);
    $conds=collectConditions();
    $report_helper=new ReportHelper();
    $req=new GetUserMessages($conds,
                            $report_helper->getFrom(),
                            $report_helper->getTo(),
                            $report_helper->getOrderBy(),
                            $report_helper->getDesc());
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $result=$resp->getResult();
        $messages=$result["messages"];
        $total_rows=$result["total_rows"];
        $do_empty=FALSE;
    }
    else
        $resp->setErrorInSmarty($smarty);
        
    if($do_empty)
    {
        $messages=array();
        $total_rows=0;
    }
    $smarty->assign_by_ref("messages",$messages);
    $smarty->assign("total_rows",$total_rows);
}

function collectConditions() 
{ 
    $collector=new ReportCollector();
    $collector->addToCondsFromRequest(TRUE,"message_id","message_id_op");

    $collector->addToCondsFromRequest(TRUE,"post_date_from","post_date_from_unit");
    $collector->addToCondsFromRequest(TRUE,"post_date_to","post_date_to_unit");

    return $collector->getConds();    
}


?>