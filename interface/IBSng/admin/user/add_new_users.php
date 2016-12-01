<?php
require_once("../../inc/init.php");
require_once(IBSINC."user.php");
require_once(IBSINC."perm.php");
require_once(IBSINC."user_face.php");
require_once(IBSINC."admin_face.php");
require_once(IBSINC."group_face.php");
require_once("../plugins/edit_funcs.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();

if(isInRequest("count","credit","owner_name","group_name"))
    intAddNewUsers($smarty,$_REQUEST["count"],$_REQUEST["credit"],$_REQUEST["owner_name"],$_REQUEST["group_name"],"");
else
    face($smarty);

function intAddNewUsers(&$smarty,$count,$credit,$owner_name,$group_name,$credit_comment)
{
    $add_user_req=new AddNewUsers($count,$credit,$owner_name,$group_name,$credit_comment);
    list($success,$user_ids)=$add_user_req->send();
    if($success)
    {
        $user_id_param=largeUrlSave("user_id", join(",",$user_ids));
        redirect("/IBSng/admin/plugins/edit.php?edit_user=1&{$user_id_param}&".convertRequestToUrl());
//              intEditUser($smarty,join(",",$user_ids));
    }
    else
        face($smarty,$user_ids);
}

function face(&$smarty,$err=NULL)
{
    intAssignValues($smarty);
        
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/user/add_new_users.tpl");    
}

function intAssignValues(&$smarty)
{
    $smarty->assign_array(array("count"=>requestVal("count"),
                                "credit"=>requestVal("credit"),
                                "owner_name"=>requestVal("owner_name",getAuthUsername()),
                                "group_name"=>requestVal("group_name"),
                                "credit_comment"=>requestVal("credit_comment")
                              ));
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("count_err"=>array("COUNT_NOT_INTEGER","INVALID_USER_COUNT"),
                                  "credit_err"=>array("CREDIT_NOT_FLOAT","CREDIT_MUST_BE_POSITIVE"),
                                  "owner_err"=>array("ADMIN_USERNAME_INVALID"),
                                  "group_err"=>array("GROUP_NAME_INVALID"),
                                  "credit_comment_err"=>array()
                                    ),$err_keys);

}

?>