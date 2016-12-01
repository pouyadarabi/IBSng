<?php
require_once("../inc/init.php");

if (isInRequest("logout"))
    doLogout();
else if (isInRequest("normal_username","normal_password"))
    doLogin($_REQUEST["normal_username"],$_REQUEST["normal_password"],NORMAL_USER_AUTH_TYPE);

else if (isInRequest("voip_username","voip_password"))
    doLogin($_REQUEST["voip_username"],$_REQUEST["voip_password"],VOIP_USER_AUTH_TYPE);

else
    face();

function doLogin($username,$password,$auth_type)
{
    list($success,$msg)=doAuth($username, $password, $auth_type);

    if($success)
    {
        setPreferredLang();
        goUserIndex();
    }
    else
        face($msg);
}

function goUserIndex()
{
    if(isInRequest("target") and !preg_match("/[^a-z_]/",$_REQUEST["target"]))
        $target_page=$_REQUEST["target"];
    else
        $target_page="home";
        
    redirect("/IBSng/user/{$target_page}.php");
}

function setPreferredLang()
{
    if(isInRequest("lang"))
        setSessionLang($_REQUEST["lang"]);
}


function face($err=NULL)
{
    $smarty=new IBSSmarty();
    if(!is_null($err))
        $smarty->set_page_error($err->getErrorMsgs());
    $smarty->display("user/".getLang()."/index.tpl");    
}


?>