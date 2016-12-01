<?php
require_once("../../inc/init.php");
require_once(IBSINC."perm.php");
require_once(IBSINC."admin_face.php");

needAuthType(ADMIN_AUTH_TYPE);
if (isInRequest("admin_username","category","perm_name"))
    intAddPerm();
else if(isInRequest("category","admin_username"))
    intShowPerms();
else
    redirectToAdminList("show_perms: Invalid Request");


function intAddPerm()
{
    $value=requestVal("value","");
    $change_perm_req=new ChangePermission($_REQUEST["admin_username"],$_REQUEST["perm_name"],$value);
    list($success,$err)=$change_perm_req->send();
    if($success)
        intShowPerms(TRUE);
    else
        intShowPerms(FALSE,$err);
}


function intShowPerms($add_success=FALSE,$err=null)
{
    $smarty=new IBSSmarty();
    intAssignValues($smarty,$add_success,$err);
    $smarty->display("admin/admins/show_perms.tpl");
}

function intAssignValues(&$smarty,$add_success,$err)
{
    $smarty->assign("category",$_REQUEST["category"]);
    $smarty->assign("category_name","{#".$_REQUEST["category"]."#}");
    $smarty->assign("admin_username",$_REQUEST["admin_username"]);
    $smarty->assign("add_success",$add_success);
    $smarty->assign("can_change",canDo("CHANGE ADMIN PERMISSIONS"));
    

    intAssignMsgErr($smarty,$err);
    list($success,$perms)=getPermsOfCategory($_REQUEST["category"]);
    if(!$success)
        $smarty->set_page_error($perms->getErrorMsgs());
    else
    {
        intAssignSelectedPermVals($smarty);
        intAssignPerms($smarty,$perms);
    }
}

function intAssignMsgErr(&$smarty,$err)
{
    if(!is_null($err))
        $smarty->set_page_error($err->getErrorMsgs());
}

function getPermsOfCategory($category)
{
    $req=new GetAllPerms($category);
    return $req->send();
}

function intAssignPerms(&$smarty,$perms)
{
    $smarty->assign("perms",$perms);
}

function intAssignSelectedPermVals(&$smarty)
{
    if(isInRequest("selected"))
    {
        $has_perm=hasPerm($_REQUEST["selected"],$_REQUEST["admin_username"]);   
        $smarty->assign("selected",$_REQUEST["selected"]);
        $smarty->assign("has_selected_perm",$has_perm);
        $smarty->assign("selected_value",requestVal("value"));

        if($has_perm)
        {
            $perm_val_req=new AdminPermValue($_REQUEST["selected"],$_REQUEST["admin_username"]);
            list($success,$cur_val)=$perm_val_req->send();
            if($success)
                $smarty->assign("cur_val",$cur_val);
            else
            {
                $smarty->assign("cur_val","ERR");
                smartySetPageErr($smarty,$cur_val->getErrorMsgs());
            }
        }
    }
    else
        $smarty->assign("selected","");
}


?>