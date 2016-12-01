<?php
require_once("../inc/init.php");

if (isInRequest("logout"))
    doLogout();
else if (isInRequest("username","password"))
    doLogin($_REQUEST["username"],$_REQUEST["password"]);
else
    face();

function doLogin($username,$password)
{
    list($success,$msg)=adminAuth($username,$password);
    if($success)
        goAdminIndex();
    else
        face($msg);
}

function goAdminIndex()
{
    if(isInRequest("target") and preg_match("/^\/[a-zA-Z0-9_\/=\?\.]+$/",$_REQUEST["target"]))
        redirect($_REQUEST["target"]);
    else
        redirect("/IBSng/admin/admin_index.php");
}


function face($err=NULL)
{
    $smarty=new IBSSmarty();
    if(!is_null($err))
        $smarty->set_page_error($err->getErrorMsgs());
    $smarty->display("admin/index.tpl");    
}


?>
