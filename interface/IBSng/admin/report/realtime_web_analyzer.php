<?php

require_once("../../inc/init.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();

intShowRealTimeWebAnalyzer($smarty);

function intShowRealTimeWebAnalyzer(&$smarty)
{
    intSetVars($smarty);
    $smarty->display("admin/report/realtime_web_analyzer.tpl");
}

function intSetVars(&$smarty)
{
    if(isInRequest("user_id","username"))
    {
        $smarty->assign("user_id",$_REQUEST["user_id"]);
        $smarty->assign("username",$_REQUEST["username"]);
        $smarty->assign("default_query","user_ids={$_REQUEST["user_id"]}");
    }
    else
    {
        $smarty->assign("username","All Users");
        $smarty->assign("default_query","");
    }   
    
    $smarty->assign("start_date",date("Y-m-d H:i:s"));
}