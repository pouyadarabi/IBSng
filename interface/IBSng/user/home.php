<?php
require_once("../inc/init.php");
require_once(IBSINC."user_face.php");

needAuthType(NORMAL_USER_AUTH_TYPE,VOIP_USER_AUTH_TYPE);

$smarty=new IBSSmarty();
intShowUserInfo($smarty);

function intShowUserInfo(&$smarty)
{
    intSetValues($smarty);
    face($smarty);
}

function intSetValues(&$smarty)
{
    list($normal_username,$voip_username)=getNormalAndVoIPUsernames();
    intSetSingleUserInfo($smarty,null,$normal_username,$voip_username,FALSE);
    intSetApproxDuration($smarty,-1);
}

function face(&$smarty)
{
    $smarty->display("user/".getLang()."/home.tpl");
}

?>