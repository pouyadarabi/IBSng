<?php
require_once("../../inc/init.php");
require_once(IBSINC."perm.php");
require_once(IBSINC."admin_face.php");

needAuthType(ADMIN_AUTH_TYPE);
if (isInRequest("template_name"))
    intShowTemplatePerms($_REQUEST["template_name"]);


function intShowTemplatePerms($template_name)
{
    $smarty=new IBSSmarty();
    intSetTemplatePerms($smarty,$template_name);
    intSetVars($smarty,$template_name);
    $smarty->display("admin/admins/show_permtemplate_perms.tpl");
}

function intSetVars(&$smarty,$template_name)
{
    $smarty->assign("template_name",$template_name);
}


function intSetTemplatePerms(&$smarty,$template_name)
{
    list($success,$categorized_perms)=getPermsOfTemplateByCategory($template_name);
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

function getPermsOfTemplateByCategory($template_name)
{
    $template_perms_req=new getPermsOfTemplate($template_name);
    list($success,$perms)=$template_perms_req->send();
    if(!$success)
        return array(FALSE,$perms);
    $categorized_perms=getPermsByCategory($perms);
    return array(TRUE,$categorized_perms);
}

?>