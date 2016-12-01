<?php
require_once("init.php");

class PostMessageToUser extends Request
{
    function PostMessageToUser($user_ids, $message)
    {
        parent::Request("message.postMessageToUser",array("user_ids"=>$user_ids,
                                                          "message"=>$message));
    }
}

class PostMessageToAdmin extends Request
{
    function PostMessageToAdmin($message)
    {
        parent::Request("message.postMessageToAdmin",array("message"=>$message));
    }
}

class GetAdminMessages extends Request
{
    function GetAdminMessages($conds, $from, $to, $sort_by, $desc)
    {
        parent::Request("message.getAdminMessages",array("conds"=>$conds,
                                                         "from"=>$from,
                                                         "to"=>$to,
                                                         "sort_by"=>$sort_by,
                                                         "desc"=>$desc));
    }
}

class GetUserMessages extends Request
{
    function GetUserMessages($conds, $from, $to, $sort_by, $desc)
    {
        parent::Request("message.getUserMessages",array("conds"=>$conds,
                                                         "from"=>$from,
                                                         "to"=>$to,
                                                         "sort_by"=>$sort_by,
                                                         "desc"=>$desc));
    }
}

class DeleteUserMessages extends Request
{
    function DeleteUserMessages($message_ids)
    {
        parent::Request("message.deleteUserMessages",array("message_ids"=>$message_ids));
    }
}

class DeleteAdminMessages extends Request
{
    function DeleteAdminMessages($message_ids, $table)
    {
        parent::Request("message.deleteMessages",array("message_ids"=>$message_ids,
                                                            "table"=>$table
                                                            ));
    }
}

class GetUserLastMessageID extends Request
{
    function GetUserLastMessageID()
    {
        parent::Request("message.getLastMessageID",array());
    }
}

?>