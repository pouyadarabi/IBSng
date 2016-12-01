<?php
require_once("../../inc/init.php");
require_once(IBSINC."charge.php");
require_once(IBSINC."perm.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
intChargeList($smarty);

function intChargeList(&$smarty)
{
    intSetChargeInfos($smarty);
    face($smarty);
}

function face(&$smarty)
{
    intSetErrors($smarty);
    $smarty->display("admin/charge/charge_list.tpl");
}

function intSetErrors(&$smarty)
{
    if(isInRequest("msg"))
        $smarty->set_page_error(array($_REQUEST["msg"]));
}

function intSetChargeInfos(&$smarty)
{
    $charge_infos=array();
    $charge_names=new ListCharges();
    list($success,$charge_names)=$charge_names->send();
    if (!$success)
        $smarty->set_page_error($charge_names->getErrorMsgs());
    else
    {
        $charge_info_req=new GetChargeInfo("");
        foreach ($charge_names as $charge_name)
        {
            $charge_info_req->changeParam("charge_name",$charge_name);
            list($success,$info)=$charge_info_req->send();
            if(!$success)
                $smarty->set_page_error($info->getErrorMsgs());
            else
                $charge_infos[$charge_name]=$info;
        }
    }
    $smarty->assign("charge_infos",$charge_infos);
}

?>