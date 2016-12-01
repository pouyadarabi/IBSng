<?php

require_once("online_users_funcs.php");
require_once(IBSINC."ras_face.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
intShowOnlineUsers($smarty);

function intShowOnlineUsers(&$smarty)
{
    list($internet_onlines, $voip_onlines) = intGetOnlineUsers($smarty);
    if(isInRequest("js"))
        intShowJSOnlines($smarty,$internet_onlines,$voip_onlines);
    else
        intShowOnlinesByType($smarty,$internet_onlines,$voip_onlines);
}

function intShowOnlinesByType(&$smarty,&$internet_onlines,&$voip_onlines)
{
    $smarty->assign_by_ref("internet_onlines",$internet_onlines);
    $smarty->assign_by_ref("voip_onlines",$voip_onlines);

    $smarty->assign("refresh_times",array(5,10,20,30,60));
    $smarty->assign("refresh_default",requestVal("refresh",20));

    $smarty->assign("hide_menu",TRUE);
    $smarty->display("admin/report/online_users_by_type.tpl");
}

function intShowJSOnlines(&$smarty,&$internet_onlines,&$voip_onlines)
{
    $smarty->assign_by_ref("internet_onlines",$internet_onlines);
    $smarty->assign_by_ref("voip_onlines",$voip_onlines);

    intSetRasDescs($smarty);
    $smarty->assign("start_with_chars",intGetStartsWithChars());
    $smarty->assign("hide_menu",TRUE);
    $smarty->display("admin/report/online_users_js.tpl");
}

function intGetStartsWithChars()
{
    $chars=array();
    for($i=ord("A");$i<=ord("Z");$i++)
        $chars[]=chr($i);
    
    for($i=0;$i<=9;$i++)
        $chars[]="{$i}";
    
    return $chars;
}


?>