<?php

require_once("../../inc/init.php");
require_once(IBSINC."report.php");
require_once(IBSINC."user.php");


needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
intShowAddUserSaves($smarty);

function intShowAddUserSaves(&$smarty)
{
    intSetReport($smarty);
    intAssignVars($smarty);
    $smarty->display("admin/user/search_add_user_saves.tpl");
}

function intAssignVars(&$smarty)
{
    $smarty->assign("type_options",array("Normal","VoIP","All"));
    $smarty->assign("type_default",requestVal("type","All"));
    $smarty->assign("order_bys",array("add_date"=>"Date",
                                      "type"=>"Type",
                                      "admin_id"=>"Admin ID"));
    $smarty->assign("order_by_default",requestVal("order_by","date"));
    if(isInRequest("msg"))
        $smarty->set_page_error($_REQUEST["msg"]);
}

function intSetReport(&$smarty)
{
    $do_empty=TRUE;
    if(isInRequest("show"))
    {
        $conds=collectConditions();
        $conds["users_from"]=0;
        $conds["users_to"]=20;
        $conds["get_counts"]=TRUE;
        $report_helper=new ReportHelper(0,30,"add_date",TRUE);
        $req=new SearchAddUserSaves($conds,
                                $report_helper->getFrom(),
                                $report_helper->getTo(),
                                $report_helper->getOrderBy(),
                                $report_helper->getDesc());
        $resp=$req->sendAndRecv();
        if($resp->isSuccessful())
        {
            $result=$resp->getResult();
            $report=$result["result"];
            $total_rows=$result["total_rows"];
            $do_empty=FALSE;
        }
        else
            $resp->setErrorInSmarty($smarty);
    }   
    
    if($do_empty)
    {
        $report=array();
        $total_rows=0;
    }
    $smarty->assign_by_ref("results",$report);
    $smarty->assign("total_rows",$total_rows);
}

function collectConditions() 
{ 
    $collector=new ReportCollector();

    $collector->addToCondsFromRequest(TRUE,"add_user_save_id");

    $collector->addToCondsIfNotEq("type","All");

    $collector->addToCondsFromRequest(TRUE,"date_from","date_from_unit");

    $collector->addToCondsFromRequest(TRUE,"date_to","date_to_unit");

    $collector->addToCondsFromRequest(TRUE,"user_id");

    $collector->addToCondsFromRequest(TRUE,"username","username_op");

    $collector->addToCondsFromRequest(TRUE,"comment","comment_op");

    $collector->addToCondsIfNotEq("admin","All");

    return $collector->getConds();    
}


