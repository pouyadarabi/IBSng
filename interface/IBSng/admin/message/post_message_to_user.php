<?php
require_once("../../inc/init.php");
require_once(IBSINC."message.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();

if (isInRequest("message","user_id"))
    postMessageToUser($smarty, $_REQUEST["user_id"], $_REQUEST["message"]);
else if (isInRequest("user_id"))
    postInterface($smarty, $_REQUEST["user_id"]);
else
    postInterface($smarty, "ALL USERS");


function postMessageToUser(&$smarty, $user_id, $message)
{
    $req=new PostMessageToUser($user_id, $message);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $smarty->assign("post_message_success", TRUE);
        postInterface($smarty, $user_id);
    }
    else
        postInterface($smarty, $user_id, $resp->getError());
}       


function postInterface(&$smarty, $user_id,$err=null)
{
    $smarty->assign("user_id",$user_id);
    face($smarty,$err);
}

function face(&$smarty,$err)
{
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/message/post_message_to_user.tpl");
}
function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("user_id_err"=>array("INVALID_USER_ID",
                                                       "USERID_DOESNT_EXISTS"),
                                  "message_err"=>array("INVALID_MESSAGE_LENGTH")
                                                       ),$err_keys);
}

?>