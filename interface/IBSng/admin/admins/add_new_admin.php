<?php
require_once("../../inc/init.php");
require_once(IBSINC."admin.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("username","password1","password2","name","comment"))
    intAddAdmin();
else
    face();

function face($err=NULL)
{
    $smarty=new IBSSmarty();
    intAssignValues($smarty);
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/admins/add_new_admin.tpl");    

}

function intAddAdmin()
{
    $add_new_admin=new addNewAdmin($_REQUEST["username"],$_REQUEST["password1"],$_REQUEST["password2"],
                                    $_REQUEST["name"],$_REQUEST["comment"]);
    list($success,$arg)=$add_new_admin->send();
    if($success)
        redirectToAdminInfo($_REQUEST["username"]);
    else
        face($arg);
}

function redirectToAdminInfo($admin_username)
{
    redirect("/IBSng/admin/admins/admin_info.php?admin_username={$admin_username}");
}


function intAssignValues(&$smarty)
{
    $smarty->assign_array(array("username"=>requestVal("username"),
                               "name"=>requestVal("name"),
                               "comment"=>requestVal("comment")
                              )
                );
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("username_err"=>array("ADMIN_USERNAME_TAKEN",
                                                           "BAD_USERNAME"),
                                     "password_err"=>array("BAD_PASSWORD",
                                                           "PASSWORDS_NOT_MATCH")
                                    ),$err_keys);

}


?>