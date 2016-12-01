<?php
require_once("../../inc/init.php");
require_once(IBSINC."admin.php");
require_once(IBSINC."perm.php");
require_once(IBSINC."admin_face.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();

if (isInRequest("lock","admin_username","reason"))
    intLockAdmin($smarty,$_REQUEST["admin_username"],$_REQUEST["reason"]);
else if (isInRequest("lock","admin_username"))
    intLockInterface($smarty,$_REQUEST["admin_username"]);
else if(isInRequest("unlock","admin_username","lock_id"))
    intUnlockAdmin($smarty,$_REQUEST["admin_username"],$_REQUEST["lock_id"]);
else if (isInRequest("delete","admin_username"))
    intDeleteAdmin($smarty,$_REQUEST["admin_username"]);
else if (isInRequest("edit","admin_username"))
    intAdminInfo($smarty,$_REQUEST["admin_username"],TRUE);
else if(isInRequest("name","comment","admin_username"))
    intUpdateAdminInfo($smarty,$_REQUEST["admin_username"],$_REQUEST["name"],$_REQUEST["comment"]);
else if(isInRequest("admin_username"))
    intAdminInfo($smarty, $_REQUEST["admin_username"]);
else
{
    $err=new error("INVALID_INPUT");
    redirectToAdminList($err->getErrorMsg());
}

function intLockAdmin(&$smarty,$admin_username,$reason)
{
    $req=new LockAdmin($admin_username,$reason);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $smarty->assign("lock_success",TRUE);
        intAdminInfo($smarty,$admin_username);
    }
    else
    {
        $resp->setErrorInSmarty($smarty);
        intLockInterface($smarty,$admin_username);
    }
}

function intLockInterface(&$smarty,$admin_username)
{
    $smarty->assign("admin_username",$admin_username);
    $smarty->display("admin/admins/admin_lock.tpl");
}

function intUnlockAdmin(&$smarty,$admin_username,$lock_id)
{
    $req=new UnlockAdmin($admin_username,$lock_id);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("unlock_success",TRUE);
    else
        $resp->setErrorInSmarty($smarty);
    
    intAdminInfo($smarty,$admin_username);
}

function intDeleteAdmin(&$smarty,$admin_username)
{
    $req = new DeleteAdmin($admin_username);
    $resp = $req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToAdminList("Admin Deleted Successfully");
    else
    {
        $resp->setErrorInSmarty($smarty);
        intAdminInfo($smarty,$admin_username);
    }
}

function intUpdateAdminInfo(&$smarty,$admin_username,$name,$comment)
{
    $update_req=new UpdateAdminInfo($admin_username,$name,$comment);
    list($success,$err)=$update_req->send();
    if($success)
    {
        $smarty->assign("update_success",TRUE);
        intAdminInfo($smarty,$admin_username);
    }
    else
    {
        $smarty->set_page_error($err->getErrorMsg());
        intAdminInfo($smarty,$admin_username,TRUE);
    }

}

function face(&$smarty,$info_arr,$is_editing)
{
    intAssignValues($smarty,$info_arr,$is_editing);
    $smarty->display("admin/admins/admin_info.tpl");
}

function intAssignValues(&$smarty,$info_arr,$is_editing)
{
    $smarty->assign_array($info_arr);
    $smarty->assign("is_editing",$is_editing);
}

function intAdminInfo(&$smarty,$admin_username,$is_editing=FALSE)
{
    $admin_info=new GetAdminInfo($admin_username);
    list($success,$info)=$admin_info->send();
    if($success)
        face($smarty,$info,$is_editing);
    else
        redirectToAdminList($info->getErrorMsg());
}

?>