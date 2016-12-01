<?php
require_once("../../inc/init.php");
require_once(IBSINC."user.php");
require_once(IBSINC."dialer.php");


if(isset($_SERVER["PHP_AUTH_USER"]) and isset($_SERVER["PHP_AUTH_PW"]) and isInRequest("new_password"))
    intChangePassword($_SERVER["PHP_AUTH_USER"],$_SERVER["PHP_AUTH_PW"],$_REQUEST["new_password"]);
else
    print answerDialer(FALSE,"","Access Denied");

function intChangePassword($username,$old_password,$new_password)
{
    $req=new ChangeNormalPassword($username,$new_password,$new_password,$old_password);
    $resp=$req->sendAndRecv();

    if($resp->isSuccessful())
        print answerDialer(TRUE,"");
    else
    {
        $err_obj=$resp->getError();
        print answerDialer(FALSE,"",$err_obj->getErrorMsg());
    }
}


?>
