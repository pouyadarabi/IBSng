<?php
require_once("init.php");

function answerDialer($success,$xml_response,$reason="")
{
    header("Content-Type: text/xml");

    $dtd="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n
    ";
    $head="<dialer><result>";
    if($success)
        $head.="SUCCESS";
    else
        $head.="FAILURE";

    $head.="</result>";
    
    if(!$success)
        $head.="<reason>{$reason}</reason>";
    
    return $dtd.$head.$xml_response."</dialer>";
}

function needDialerAuth()
{
    $auth=getAuth();
    if($auth->getAuthType()!=NORMAL_USER_AUTH_TYPE)
        showDialerAccessDenied();
}

function showDialerAccessDenied()
{
    print answerDialer(FALSE,"","Access Denied");
    exit();
}

?>