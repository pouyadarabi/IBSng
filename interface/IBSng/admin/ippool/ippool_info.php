<?php
require_once("../../inc/init.php");
require_once(IBSINC."ippool.php");
require_once(IBSINC."ippool_face.php");
require_once(IBSINC."perm.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();
$smarty->assign("is_editing",FALSE);


if(isInRequest("ippool_name","delete"))
    intDelIPpool($smarty,$_REQUEST["ippool_name"]);
else if (isInRequest("ippool_name","del_ip","del_submit"))
    intDelIPfromPool($smarty,$_REQUEST["ippool_name"],$_REQUEST["del_ip"]);
else if (isInRequest("ippool_name","add_ip","add_submit"))
    intAddIPtoPool($smarty,$_REQUEST["ippool_name"],$_REQUEST["add_ip"]);
else if (isInRequest("ippool_id","new_ippool_name","old_ippool_name","comment","update"))
    intUpdateIPpoolInfo($smarty,$_REQUEST["ippool_id"],$_REQUEST["new_ippool_name"],$_REQUEST["old_ippool_name"],$_REQUEST["comment"]);
else if (isInRequest("ippool_name","edit"))
    intEditIPpoolInfo($smarty,$_REQUEST["ippool_name"]);
else if(isInRequest("ippool_name"))
    intIPpoolInfo($smarty,$_REQUEST["ippool_name"]);
else
{
    $err=new error("INVALID_INPUT");
    redirectToIPpoolList($err->getErrorMsg());
}


function intDelIPpool(&$smarty,$ippool_name)
{
    $del_ippool_req=new DeleteIPpool($ippool_name);
    list($success,$err)=$del_ippool_req->send();
    if($success)
        redirectToIPpoolList();
    else
    {
        $smarty->set_page_error($err->getErrorMsgs());
        intIPpoolInfo($smarty,$ippool_name);
    }
}

function intDelIPfromPool(&$smarty,$ippool_name,$ip)
{
    $del_ip_req=new DelIPfromPool($ippool_name,$ip);
    list($success,$err)=$del_ip_req->send();
    if($success)
        $smarty->assign("ip_deleted_successfull",TRUE);
    else
        $smarty->set_page_error($err->getErrorMsgs());
    intIPpoolInfo($smarty,$ippool_name);
}

function intAddIPtoPool(&$smarty,$ippool_name,$ip)
{
    $add_ip_req=new AddIPtoPool($ippool_name,$ip);
    list($success,$err)=$add_ip_req->send();
    if($success)
        $smarty->assign("ip_added_successfull",TRUE);
    else
        $smarty->set_page_error($err->getErrorMsgs());
    intIPpoolInfo($smarty,$ippool_name);
}

function intUpdateIPpoolInfo(&$smarty,$ippool_id,$new_ippool_name,$old_ippool_name,$comment)
{
    $update_ippool_req=new UpdateIPpool($ippool_id,$new_ippool_name,$comment);
    list ($success,$err)=$update_ippool_req->send();
    if($success)
    {
        $smarty->assign("update_successfull",TRUE);
        $ippool_name=$new_ippool_name;
    }
    else
    {
        $smarty->set_page_error($err->getErrorMsgs());
        $ippool_name=$old_ippool_name;
    }
    intIPpoolInfo($smarty,$ippool_name);
}

function intEditIPpoolInfo(&$smarty,$ippool_info)
{
    $smarty->assign("is_editing",TRUE);
    intIPpoolInfo($smarty,$ippool_info);
}

function intIPpoolInfo(&$smarty,$ippool_name)
{
    $ippool_info_req=new GetIPpoolInfo($ippool_name);
    list($success,$info)=$ippool_info_req->send();
    if(!$success)
//      redirectToIPpoolList($info->getErrorMsg());
        $smarty->set_page_error($info->getErrorMsgs());
    face($smarty,$info);
}

function face(&$smarty,$ippool_info)
{
    intAssignValues($smarty,$ippool_info);
    $smarty->display("admin/ippool/ippool_info.tpl");
}

function intAssignValues(&$smarty,$ippool_info)
{
    $smarty->assign_array($ippool_info);
    $smarty->assign("can_change",canDo("CHANGE IPPOOL"));
}

?>
