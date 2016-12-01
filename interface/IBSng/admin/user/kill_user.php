<?php
require_once("../../inc/init.php");
require_once(IBSINC."user.php");


needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();

if(isInRequest("user_id","username","ras_ip","unique_id_val","kill"))
    intKillUser($smarty,$_REQUEST["user_id"],$_REQUEST["username"],$_REQUEST["ras_ip"],$_REQUEST["unique_id_val"]);
elseif(isInRequest("user_id","username","ras_ip","unique_id_val","clear"))
    intClearUser($smarty,$_REQUEST["user_id"],$_REQUEST["username"],$_REQUEST["ras_ip"],$_REQUEST["unique_id_val"]);
else
    face($smarty,"","Invalid Input");

function face(&$smarty,$username,$err="")
{
    $smarty->assign("username",$username);
    if($err!="")
        $smarty->set_page_error($err);
    $smarty->display("admin/user/kill_user.tpl");
}

function intKillUser(&$smarty,$user_id,$username,$ras_ip,$unique_id_val)
{
    $req=new KillUser($user_id,$ras_ip,$unique_id_val,TRUE);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("kill_success",TRUE);
    else
        $resp->setErrorInSmarty($smarty);
    face($smarty,$username);
}

function intClearUser(&$smarty,$user_id,$username,$ras_ip,$unique_id_val)
{
    $req=new KillUser($user_id,$ras_ip,$unique_id_val,FALSE);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("clear_success",TRUE);
    else
        $resp->setErrorInSmarty($smarty);
    face($smarty,$username);
}
?>