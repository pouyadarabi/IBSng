<?php
require_once("init.php");
require_once("admin.php");

function redirectToAdminList($msg="")
{
    redirect("/IBSng/admin/admins/admin_list.php?msg={$msg}");
}

function redirectToAdminInfo($admin_username)
{
    redirect("/IBSng/admin/admins/admin_info.php?admin_username={$admin_username}");
}

function getAdminNames(&$smarty)
{ /* return  admin names in  an array. Array is a number indexed.
     On error, return an empty array and a message is set in smarty object
  */
    $admin_names_req=new GetAllAdminUsernames();
    list($success,$admins)=$admin_names_req->send();
    if($success)
        return $admins;
    else
    {
        $smarty->set_page_error($admins->getErrorMsgs());
        return array();
    }
}

?>