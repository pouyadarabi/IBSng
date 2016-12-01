<?php
require_once("../inc/init.php");
require_once(IBSINC."message.php");

needAuthType(NORMAL_USER_AUTH_TYPE,VOIP_USER_AUTH_TYPE);

$smarty=new IBSSmarty();

if (isInRequest("message"))
    postMessageToAdmin($smarty, $_REQUEST["message"]);
else
    postInterface($smarty);


function postMessageToAdmin(&$smarty, $message)
{
    $req=new PostMessageToAdmin($message);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $smarty->assign("post_message_success", TRUE);
        postInterface($smarty);
    }
    else
        postInterface($smarty, $resp->getError());
}       


function postInterface(&$smarty,$err=null)
{
    face($smarty,$err);
}

function face(&$smarty,$err)
{
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("user/".getLang()."/post_message_to_admin.tpl");
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("message_err"=>array("INVALID_MESSAGE_LENGTH"))
                                                       ,$err_keys);
}

?>