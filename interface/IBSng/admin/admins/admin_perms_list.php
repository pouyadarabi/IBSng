<?php
require_once("../../inc/init.php");
require_once(IBSINC."perm.php");
require_once(IBSINC."admin_face.php");

needAuthType(ADMIN_AUTH_TYPE);
if (isInRequest("admin_username","template_name","action"))
    intHandleTemplateRequest($_REQUEST["admin_username"],$_REQUEST["template_name"],$_REQUEST["action"]);
else if(isInRequest("admin_username","delete_perm","delete_perm_val"))
    intDelPermValue($_REQUEST["admin_username"],$_REQUEST["delete_perm"],$_REQUEST["delete_perm_val"]);
else if(isInRequest("admin_username","delete_perm"))
    intDelPerm($_REQUEST["admin_username"],$_REQUEST["delete_perm"]);
else if(isInRequest("admin_username"))
    intShowAdminPerms($_REQUEST["admin_username"]);
else
    redirectToAdminList("admin_perms_list: No username given");


function intHandleTemplateRequest($admin_username,$template_name,$action)
{
    switch($action)
    {
        case "save":
            intSavePermsToTemplate($admin_username,$template_name);
            break;
        case "load":
            intLoadTemplateToAdmin($admin_username,$template_name);
            break;
        case "delete":
            intDeleteTemplate($admin_username,$template_name);
            break;
        default:
            print "ohoooooooooooooy";
            break;
    }
    
}

function intSavePermsToTemplate($admin_username,$template_name)
{
    $save_perms_req=new SavePermsOfAdminToTemplate($admin_username,$template_name);
    list($success,$err)=$save_perms_req->send();
    if($success)
        intShowAdminPerms($admin_username,null,FALSE,FALSE,TRUE);
    else
        intShowAdminPerms($admin_username,$err);
}

function intLoadTemplateToAdmin($admin_username,$template_name)
{
    $load_template_req=new LoadPermTemplateToAdmin($admin_username,$template_name);
    list($success,$err)=$load_template_req->send();
    if($success)
        intShowAdminPerms($admin_username,null,FALSE,FALSE,FALSE,TRUE);
    else
        intShowAdminPerms($admin_username,$err);
    
}

function intDeleteTemplate($admin_username,$template_name)
{
    $del_template_req=new DeletePermTemplate($template_name);
    list($success,$err)=$del_template_req->send();
    if($success)
        intShowAdminPerms($admin_username,null,FALSE,FALSE,FALSE,FALSE,TRUE);
    else
        intShowAdminPerms($admin_username,$err);
}

function intDelPerm($admin_username,$perm_name)
{
    $del_req=new DeletePermission($admin_username,$perm_name);
    list($success,$err)=$del_req->send();
    if(!$success)
        intShowAdminPerms($admin_username,$err,FALSE);
    else
        intShowAdminPerms($admin_username,null,TRUE);
}

function intDelPermValue($admin_username,$perm_name,$perm_value)
{
    $del_val_req=new DeletePermissionValue($admin_username,$perm_name,$perm_value);
    list($success,$err)=$del_val_req->send();
    if(!$success)
        intShowAdminPerms($admin_username,$err,FALSE,FALSE);
    else
        intShowAdminPerms($admin_username,null,FALSE,TRUE);

}
function intShowAdminPerms($admin_username,$err=null,$del_success=FALSE,$del_val_success=FALSE,
                           $save_template_success=FALSE,$load_template_success=FALSE,
                           $del_template_success=FALSE)
{
    $smarty=new IBSSmarty();
    intSetAdminPerms($smarty,$admin_username);
    intSetVars($smarty,$admin_username,$err,$del_success,$del_val_success,$save_template_success,
               $load_template_success,$del_template_success);
    $smarty->display("admin/admins/admin_perms_list.tpl");
}

function intSetVars(&$smarty,$admin_username,$err,$del_success,$del_val_success,$save_template_success,
               $load_template_success,$del_template_success)
{
    $can_change=canDo("CHANGE ADMIN PERMISSIONS");
    $smarty->assign("admin_username",$admin_username);
    $smarty->assign("can_change",$can_change);
    $smarty->assign("del_perm_success",$del_success);
    $smarty->assign("del_perm_val_success",$del_val_success);
    $smarty->assign_array(array("save_template_success"=>$save_template_success,
                          "load_template_success"=>$load_template_success,
                          "del_template_success"=>$del_template_success));
    
    if($can_change)
        intSetTemplatesList($smarty);
    if(!is_null($err))
        $smarty->set_page_error($err->getErrorMsgs());
}

function intSetTemplatesList(&$smarty)
{
    $template_lists_req=new GetListOfPermTemplates();
    list($success,$templates_list)=$template_lists_req->send();
    if($success)
        $smarty->assign("templates_list",$templates_list);
    else
    {
        $smarty->set_page_error($templates_list->getErrorMsgs());
        $smarty->assign("templates_list",array());
    }
}

function intSetAdminPerms(&$smarty,$admin_username)
{
    list($success,$categorized_perms)=getAdminPermsByCategory($admin_username);
    if(!$success)
    {
        $smarty->set_page_error($categorized_perms->getErrorMsgs());
        $smarty->assign("perms",array());
    }
    else
    {
        $categories=array_keys($categorized_perms);
        $smarty->config_load("perm_category_names.conf");
        $category_names=array();
        foreach($categories as $category)
            $category_names[$category]=$smarty->get_config_vars($category);
        $smarty->assign("category_names",$category_names);
        $smarty->assign("perms",$categorized_perms);
    }
}


function getAdminPermsByCategory($admin_username)
{
    $admin_perms_req=new GetPermsOfAdmin($admin_username);
    list($success,$perms)=$admin_perms_req->send();
    if(!$success)
        return array(FALSE,$perms);
    $categorized_perms=getPermsByCategory($perms);
    return array(TRUE,$categorized_perms);
}

?>