<?php
require_once("../../inc/init.php");
require_once(IBSINC."group.php");
require_once(IBSINC."group_face.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("group_name","comment"))
    intAddGroup($_REQUEST["group_name"],$_REQUEST["comment"]);
else
    face();

function intAddGroup($group_name,$comment)
{
    $add_group_req=new AddNewGroup($group_name,$comment);
    list($success,$err)=$add_group_req->send();
    if($success)
        redirectToGroupInfo($group_name);
    else
        face($err);
}

function face($err=NULL)
{
    $smarty=new IBSSmarty();
    intAssignValues($smarty);
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/group/add_new_group.tpl");    
}

function intAssignValues(&$smarty)
{
    $smarty->assign_array(array("group_name"=>requestVal("group_name"),
                               "comment"=>requestVal("comment")
                              ));
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("group_name_err"=>array("GROUP_NAME_TAKEN","GROUP_NAME_INVALID"),
                                    ),$err_keys);

}

?>