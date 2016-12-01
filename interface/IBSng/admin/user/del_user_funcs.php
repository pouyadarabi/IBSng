<?php
require_once(IBSINC."user.php");
require_once(IBSINC."user_face.php");
require_once(IBSINC."user_search.php");

function intDeleteUser(&$smarty,$user_id,$delete_comment,$del_connection_logs,$del_audit_logs)
{
    $req=new DelUser($user_id,$delete_comment,$del_connection_logs,$del_audit_logs);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("delete_successful",TRUE);
    else
        $resp->setErrorInSmarty($smarty);
    intShowDeleteUserFace($smarty,$user_id);
}

function intShowDeleteUserFace(&$smarty,$user_id)
{
    $smarty->assign("user_id",$user_id);
    $smarty->display("admin/user/del_user.tpl");
}

?>