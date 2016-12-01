<?php
require_once("../../inc/init.php");
require_once("search_user_funcs.php");
require_once("change_credit_funcs.php");
require_once("del_user_funcs.php");
require_once("../plugins/edit_funcs.php");
require_once(IBSINC."report.php");


needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
$user_ids=getSelectedUserIDsFromRequest();
if(sizeof($user_ids)==0)
{
    $smarty->set_page_error("No users selected!");
    intShowUserSearch($smarty);
}
else if(isInRequest("edit"))
    searchUserEdit($smarty,$user_ids);
else if (isInRequest("change_credit"))
    changeUserCredit($smarty,$user_ids);
else if (isInRequest("connection_log"))
    showConnectionLogs($smarty,$user_ids);
else if (isInRequest("credit_change"))
    showCreditChanges($smarty,$user_ids);
else if (isInRequest("audit_log"))
    showAuditLogs($smarty,$user_ids);
else if (isInRequest("delete_users"))
    showDeleteUserFace($smarty,$user_ids);


function showCreditChanges(&$smarty,$user_ids)
{
    redirect("/IBSng/admin/report/credit_changes.php?user_ids=".join(",",$user_ids));
}

function showConnectionLogs(&$smarty,$user_ids)
{
    redirect("/IBSng/admin/report/connections.php?user_ids=".join(",",$user_ids));
}

function showAuditLogs(&$smarty,$user_ids)
{
    redirect("/IBSng/admin/report/user_audit_logs.php?user_ids=".join(",",$user_ids));
}

function changeUserCredit(&$smarty,$user_ids)
{
    intShowChangeCreditFace($smarty,join(",",$user_ids));
}

function searchUserEdit(&$smarty,$user_ids)
{
    intEditUser($smarty,join(",",$user_ids));
}

function showDeleteUserFace(&$smarty,$user_ids)
{
    intShowDeleteUserFace($smarty,join(",",$user_ids));
}


function getSelectedUserIDsFromRequest()
{
    $user_ids=array();
    foreach($_REQUEST as $key=>$value)
        if(preg_match("/^edit_user_id_[0-9]+$/",$key))
            $user_ids[]=$value;
    
    return $user_ids;
}

?>