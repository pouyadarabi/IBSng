<?php
require_once("init.php");

class GetRealTimeSnapShot extends Request
{
    function GetRealTimeSnapShot($name)
    {
        parent::Request("snapshot.getRealTimeSnapShot",array("name"=>$name));
    }
}

class GetBWSnapShotForUser extends Request
{
    function GetBWSnapShotForUser($user_id,$ras_ip,$unique_id_val)
    {
        parent::Request("snapshot.getBWSnapShotForUser",array("user_id"=>$user_id,
                                                              "ras_ip"=>$ras_ip,
                                                              "unique_id_val"=>$unique_id_val));
    }
}

class GetOnlinesSnapShot extends Request
{
    function GetOnlinesSnapShot($conds,$type)
    {
        parent::Request("snapshot.getOnlinesSnapShot",array("conds"=>$conds,
                                                           "type"=>$type));
    }
}

class GetBWSnapShot extends Request
{
    function GetBWSnapShot($conds)
    {
        parent::Request("snapshot.getBWSnapShot",array("conds"=>$conds));
    }
}

?>