<?php
require_once("../../inc/init.php");
require_once(IBSINC."dialer.php");
require_once(IBSINC."message.php");
require_once(IBSINC."xml.php");

needDialerAuth();

if (isInRequest("get_last_message_id"))
    intGetLastMessageID();
else if(isInRequest("send_message","message_text"))
    intPostMessage($_REQUEST["message_text"]);
else if (isInRequest("get_messages","from_message_id"))
    intGetMessages($_REQUEST["from_message_id"]);
else if (isInRequest("delete_message","message_id"))
    intDelMessages($_REQUEST["message_id"]);
else
    print answerDialer(FALSE,"","Access Denied");
    
/////////////////////////////////////////
function intGetLastMessageID()
{
    $last_message_id = getLastMessageID();
    print answerDialer(TRUE,"<last_message_id>{$last_message_id}</last_message_id>");
}

function getLastMessageID()
{
    $req=new GetUserLastMessageID();
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        return $resp->getResult();
    else
        return -1;
}
/////////////////////////////////////////
function intPostMessage($message_text)
{
    $req=new PostMessageToAdmin(unicode_decode($message_text));
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        print answerDialer(TRUE,"");
    else
    {
        $err_obj=$resp->getError();
        print answerDialer(FALSE,"",$err_obj->getErrorMsg());
    }   
}

function unicode_decode($txt) {
  return ereg_replace('%u0([[:alnum:]]{3})', '&#x\1;',$txt);
}
//////////////////////////////////////


function intGetMessages($from_message_id)
{
    $conds=array("message_id"=>$from_message_id,
                 "message_id_op"=>">");
    $req=new GetUserMessages($conds,
                            0,
                            100,
                            "message_id",
                            False);

    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        print answerDialer(TRUE,encodeMessages($resp->getResult()));
    else
    {
        $err_obj=$resp->getError();
        print answerDialer(FALSE,"",$err_obj->getErrorMsg());
    }   
}

function encodeMessages($result)
{
    $ret = "";
    foreach($result["messages"] as $message)
    {
        if($message["user_id"]=="ALL USERS")
            $to = "ALL USERS";
        else
            $to = "USER";

        $title = cdataEscape(getTitleFromMessageText($message["message_text"]));
        $text = cdataEscape($message["message_text"]);
        $ret .= <<<END
        <message>
            <message_id>{$message["message_id"]}</message_id>
            <title><![CDATA[{$title}]]></title>
            <body><![CDATA[{$text}]]></body>
            <to>{$to}</to>
            <date>{$message["post_date_formatted"]}</date>
        </message>
END;
    }
    return $ret;
}

function getTitleFromMessageText($message_text, $min = 8, $max = 15)
{
    $stripped_message = strip_tags($message_text);
    $len = mb_strlen($stripped_message,"UTF-8");
    if($len <= $min)
        return $stripped_message;
        
    $break_point = mb_strpos($stripped_message, ' ', $min, "UTF-8");
    if($break_point === false)
        $break_point = $max;
    else
        $break_point = min($max,$break_point);
            
    $title=mb_substr($stripped_message, 0, $break_point, "UTF-8");
    if (strlen($title) < $len)
        $title .= " ...";
        
    return $title;
}
        
///////////////////////////////////

function intDelMessages($message_id)
{
    $req=new DeleteUserMessages(array($message_id));
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
