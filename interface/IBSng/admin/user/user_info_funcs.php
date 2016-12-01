<?php
require_once(IBSINC."user.php");
require_once(IBSINC."util.php");
require_once(IBSINC."perm.php");
require_once(IBSINC."user_face.php");
require_once(IBSINC."group_face.php");
require_once(IBSINC."user_search.php");

//*******************************************
function intShowMultiUserInfo(&$smarty,$user_id)
{
    if(!isMultiString($user_id))
        intShowSingleUserInfo($smarty,$user_id);
    else
        redirectToUserSearchInc(array("user_id"=>$user_id));
}
//********************************************
function intShowMultiNormalUserInfo(&$smarty,$normal_username)
{
    if(!isMultiString($normal_username))
        intShowSingleUserInfo($smarty,null,$normal_username);
    else
        redirectToUserSearch("normal_username={$normal_username}&normal_username_op=equals");
}
//********************************************
function intShowMultiVoIPUserInfo(&$smarty,$voip_username)
{
    if(!isMultiString($voip_username))
        intShowSingleUserInfo($smarty,null,null,$voip_username);
    else
        redirectToUserSearch("voip_username={$voip_username}&voip_username_op=equals");
}
//********************************************

function intShowSingleUserInfo(&$smarty,$user_id,$normal_username=null,$voip_username=null)
{
    $resp=intSetSingleUserInfo($smarty,$user_id,$normal_username,$voip_username);
    if($resp->isSuccessful())
    {
        $result=array_values($resp->getResult());
        $user_info=$result[0];
        intShowSingleUserInfoAssignValues($smarty,$user_info["basic_info"]["user_id"],$user_info);
        intShowSingleUserInfoInterface($smarty);
    }
    else
        intShowSingleUserInfoInput($smarty);
}

function intShowSingleUserInfoAssignValues(&$smarty,$user_id,&$user_info)
{
    $smarty->assign("can_change",canDo("CHANGE USER ATTRIBUTES",null,(int)$user_id,$user_info["basic_info"]["owner_id"]));
    $smarty->assign("can_change_normal",canDo("CHANGE NORMAL USER ATTRIBUTES",null,(int)$user_id,$user_info["basic_info"]["owner_id"]));
    $smarty->assign("can_change_voip",canDo("CHANGE VOIP USER ATTRIBUTES",null,(int)$user_id,$user_info["basic_info"]["owner_id"]));
    $smarty->assign("can_delete",canDo("DELETE USER",null,(int)$user_id,$user_info["basic_info"]["owner_id"]));
    intSetApproxDuration($smarty,$user_id);
    intSetSingleUserGroupAttrs($smarty,$user_info);
}

function intShowSingleUserInfoInterface(&$smarty)
{
    $smarty->display("admin/user/single_user_info.tpl");
}
//*********************************************

function intShowSingleUserInfoInput(&$smarty)
{
    $smarty->display("admin/user/single_user_info_input.tpl");
}

?>