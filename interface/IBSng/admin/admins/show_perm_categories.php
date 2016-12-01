<?php
require_once("../../inc/init.php");
require_once(IBSINC."admin_face.php");

needAuthType(ADMIN_AUTH_TYPE);

if(!isInRequest("admin_username"))
    redirectToAdminList("show_perm_categories: no username given");
else
    intShowCategories();
    
function intShowCategories()
{
    $smarty=new IBSSmarty();
    $smarty->assign("admin_username",$_REQUEST["admin_username"]);
    $smarty->display("admin/admins/perm_category_select.tpl");
}

?>