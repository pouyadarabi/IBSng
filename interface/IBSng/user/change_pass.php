<?php
require_once("../inc/init.php");
require_once(IBSINC."user.php");
require_once(IBSINC."user_face.php");

needAuthType(NORMAL_USER_AUTH_TYPE,VOIP_USER_AUTH_TYPE);

$smarty=new IBSSmarty();
if(isInRequest("old_normal_password","new_normal_password1","new_normal_password2"))
    intChangeNormalPassword($smarty,$_REQUEST["old_normal_password"],$_REQUEST["new_normal_password1"],
                            $_REQUEST["new_normal_password2"]);
else if (isInRequest("old_voip_password","new_voip_password1","new_voip_password2"))
    intChangeVoIPPassword($smarty,$_REQUEST["old_voip_password"],$_REQUEST["new_voip_password1"],
                            $_REQUEST["new_voip_password2"]);
else
    intShowChangePassword($smarty);

function intChangeNormalPassword(&$smarty,$old_password,$new_password1,$new_password2)
{
    $req=new ChangeNormalPassword("",$new_password1,$new_password2,$old_password);
    $resp=$req->sendAndRecv();

    if($resp->isSuccessful())
    {
        $smarty->assign("normal_change_success",TRUE);
        reAuthUser(NORMAL_USER_AUTH_TYPE,$new_password1);
    }
    else
        $resp->setErrorInSmarty($smarty);
    
    intShowChangePassword($smarty);    
}

function intChangeVoIPPassword(&$smarty,$old_password,$new_password1,$new_password2)
{
    $req=new ChangeVoIPPassword("",$new_password1,$new_password2,$old_password);
    $resp=$req->sendAndRecv();

    if($resp->isSuccessful())
    {
        $smarty->assign("voip_change_success",TRUE);
        reAuthUser(VOIP_USER_AUTH_TYPE,$new_password1);
    }
    else
        $resp->setErrorInSmarty($smarty);
    
    intShowChangePassword($smarty);    
}

function reAuthUser($auth_type,$new_password)
{
    $auth=getAuth();
    if($auth->getAuthType()==$auth_type)
        doAuth(getAuthUsername(),$new_password,$auth_type);
}


function intShowChangePassword(&$smarty)
{
    intSetValues($smarty);
    face($smarty);
}

function intSetValues(&$smarty)
{
    list($normal_username,$voip_username)=getNormalAndVoIPUsernames();
    intSetSingleUserInfo($smarty,null,$normal_username,$voip_username,FALSE);
}

function face(&$smarty)
{
    $smarty->display("user/".getLang()."/change_pass.tpl");
}

?>