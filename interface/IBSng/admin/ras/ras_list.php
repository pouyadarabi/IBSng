<?php
require_once("../../inc/init.php");
require_once(IBSINC."ras.php");
require_once(IBSINC."perm.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
if(isInRequest("deactive"))
    deActiveRas($smarty,$_REQUEST["deactive"]);
else if(isInRequest("reactive"))
    reActiveRas($smarty,$_REQUEST["reactive"]);
else
    intRasList($smarty);

function deActiveRas(&$smarty,$ras_ip)
{
    $deactive_req=new DeActiveRas($ras_ip);
    list($success,$err)=$deactive_req->send();
    if($success)
        $smarty->assign("deactive_success",TRUE);
    else
        $smarty->set_page_error($err->getErrorMsgs());
    intRasList($smarty);
}

function reActiveRas(&$smarty,$ras_ip)
{
    $reactive_req=new ReActiveRas($ras_ip);
    list($success,$err)=$reactive_req->send();
    if($success)
        $smarty->assign("reactive_success",TRUE);
    else
        $smarty->set_page_error($err->getErrorMsgs());
    intRasList($smarty);
}

function intRasList(&$smarty)
{
    list($success,$active_ras_infos)=getAllActiveRasInfos();
    if(!$success)
    {
        $smarty->set_page_error($active_ras_infos->getErrorMsgs());
        $active_ras_infos=array();
    }
    $inactive_ras_req=new GetInActiveRases();
    list($success,$inactive_ras_infos)=$inactive_ras_req->send();
    if(!$success)
    {
        $smarty->set_page_error($inactive_ras_infos->getErrorMsgs());
        $inactive_ras_infos=array();
    }
    face($smarty,$active_ras_infos,$inactive_ras_infos);
}

function face(&$smarty,$active_ras_infos,$inactive_ras_infos)
{
    intSetErrors($smarty);
    $smarty->assign("ras_infos",$active_ras_infos);
    $smarty->assign("can_change",canDo("CHANGE RAS"));
    $smarty->assign("inactive_ras_infos",$inactive_ras_infos);
    $smarty->display("admin/ras/ras_list.tpl");
}

function intSetErrors(&$smarty)
{
    if(isInRequest("msg"))
        $smarty->set_page_error(array($_REQUEST["msg"]));
}

?>