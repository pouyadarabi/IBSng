<?php

require_once("../../inc/init.php");
require_once(IBSINC."report.php");
require_once(IBSINC."message.php");


needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();


if(isInRequest("delete","table"))
    intDeleteMessage($smarty,array($_REQUEST["delete"]),$_REQUEST["table"]);
else if(isInRequest("bulk_delete_messages","table","delete_page"))
    intBulkDeleteMessages($smarty,$_REQUEST["table"]);
else
    intViewMessages($smarty);

function intBulkDeleteMessages(&$smarty, $table)
{
    $message_ids = intGetSelectedMessageIDs();
    if(sizeof($message_ids))
        intDeleteMessage($smarty, $message_ids, $table);
    else
        intViewMessages($smarty);
}

function intGetSelectedMessageIDs()
{
    $message_ids=array();
    foreach($_REQUEST as $key=>$value)
        if(preg_match("/^delete_message_id_[0-9]+$/",$key))
            $message_ids[]=$value;
    
    return $message_ids;
}

function intDeleteMessage(&$smarty, $message_id, $table)
{
    $req=new DeleteAdminMessages($message_id, $table);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("delete_message_success",TRUE);
    else
        $resp->setErrorInSmarty($smarty);

    if(isInRequest("delete_page"))
        $_REQUEST["page"]=$_REQUEST["delete_page"];

    intViewMessages($smarty);
}

function intViewMessages(&$smarty)
{
    if(isInRequest("show"))
        intSetReport($smarty);
    intAssignVars($smarty);
    $smarty->display("admin/message/view_messages.tpl");
}

function intAssignVars(&$smarty)
{
    $smarty->assign("order_bys",array("message_id"=>"Message ID",
                                      "user_id"=>"User ID",
                                      "post_date"=>"Post Date"));
    $smarty->assign("order_by_default",requestVal("order_by","message_id"));
}

function intSetReport(&$smarty)
{
    $do_empty=TRUE;
    $smarty->assign("show_report",TRUE);
    $conds=collectConditions();
    $report_helper=new ReportHelper();
    $req=new GetAdminMessages($conds,
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
    $collector->addToCondsFromRequest(TRUE,"user_ids");
    $collector->addToCondsFromRequest(TRUE,"table");

    $collector->addToCondsFromRequest(TRUE,"post_date_from","post_date_from_unit");
    $collector->addToCondsFromRequest(TRUE,"post_date_to","post_date_to_unit");

    return $collector->getConds();    
}


?>