<?php
require_once("../../inc/init.php");
require_once(IBSINC."admin.php");
require_once(IBSINC."perm.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("password1","password2"))
    intChangePassword();
else
    face();




function face($err=null,$success=FALSE,$changed_self_password=FALSE,$changed_username="")
{
    $smarty=new IBSSmarty();
    intAssignSmartyVars($smarty,$err,$success,$changed_self_password,$changed_username);
    $smarty->display("admin/admins/change_password.tpl");    
}

function intAssignSmartyVars(&$smarty,$err,$success,$changed_self_password,$changed_username)
{
    if(!is_null($err))
    {
        $smarty->set_page_error($err->getErrorMsgs());
        intSetErrors($smarty,$err->getErrorKeys());
    }
    
    $can_change_others=canDo("CHANGE PASSWORD");
    $assign_arr=array("success"=>$success,
                      "changed_self_password"=>$changed_self_password,
                      "can_change_others"=>$can_change_others,
                      "changed_username"=>$changed_username,
                      "default_username"=>isInRequest("username")?$_REQUEST["username"]:getAuthUsername(),
                      "self_username"=>getAuthUsername()
                     );
    
    if($can_change_others)
    {
        $all_users_req=new GetAllAdminUsernames();
        list($success,$usernames)=$all_users_req->send();
        if(!$success)
        {
            toLog("Change Passwords:".$usernames);
            $smarty->set_page_error($usernames->getErrorMsgs());
            $usernames=array("ERROR"=>"ERROR");
        }
        $assign_arr["usernames"]=$usernames;
    }
        
    $smarty->assign_array($assign_arr);
}

function intChangePassword()
{
    $username=getAuthUsername();
    if (canDo("CHANGE PASSWORD"))
        if (isInRequest("username"))
            $username=$_REQUEST["username"];
    
    $change_pass_req=new AdminChangePassword($username,$_REQUEST["password1"],$_REQUEST["password2"]);
    list($success,$msg)=$change_pass_req->send();
    if(!$success)
        face($msg);
    else
    {
        if($username==getAuthUsername())
            $changed_self_password=TRUE;
        else
            $changed_self_password=FALSE;
        face(null,TRUE,$changed_self_password,$username);       
    }
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("username_err"=>array("ADMIN_USERNAME_INVALID",
                                                           "BAD_USERNAME"),
                                     "password_err"=>array("BAD_PASSWORD",
                                                           "PASSWORDS_NOT_MATCH")
                                    ),$err_keys);
}

?>