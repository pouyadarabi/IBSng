<?php
require_once("../../inc/init.php");
require_once(IBSINC."dialer.php");


if(isset($_SERVER["PHP_AUTH_USER"]) and isset($_SERVER["PHP_AUTH_PW"]) )
    doLogin($_SERVER["PHP_AUTH_USER"],$_SERVER["PHP_AUTH_PW"],NORMAL_USER_AUTH_TYPE);
else if(isInRequest("normal_username","normal_password"))
    doLogin($_REQUEST["normal_username"],$_REQUEST["normal_password"],NORMAL_USER_AUTH_TYPE);
else
{
    header("WWW-Authenticate: Basic realm=\"Private Area\"");
    header("Status: 401");
//    failResponse(error("ACCESS_DENIED"));
}

function doLogin($username,$password,$auth_type)
{
    list($success,$msg)=doAuth($username,$password,$auth_type);
    if($success)
        successResponse();
    else
        failResponse($msg);
}       

function successResponse()
{
    print answerDialer(TRUE,"");
}

function failResponse($msg)
{
    print answerDialer(FALSE,"",$msg->getErrorMsg());
}


?>
