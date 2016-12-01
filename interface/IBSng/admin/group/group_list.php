<?php
require_once("../../inc/init.php");
require_once(IBSINC."group.php");
require_once(IBSINC."perm.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
intGroupList($smarty);

function intGroupList(&$smarty)
{
    intSetGroupInfos($smarty);
    face($smarty);
}

function face(&$smarty)
{
    intSetErrorMsg($smarty);
    $smarty->display("admin/group/group_list.tpl");
}

function intSetErrorMsg(&$smarty)
{
    if(isInRequest("msg"))
        $smarty->set_page_error(array($_REQUEST["msg"]));
}

function intSetGroupInfos(&$smarty)
{
    list($success,$group_infos)=getAllGroupInfos();
    if (!$success)
    {
        $smarty->set_page_error($group_infos->getErrorMsgs());
        $smarty->assign("group_infos",array());
    }
    else
        $smarty->assign("group_infos",$group_infos);
}

?>