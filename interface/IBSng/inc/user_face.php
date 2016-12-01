<?php
require_once("init.php");
require_once("user.php");
require_once("attr_parser.php");
require_once("large_url.php");

function redirectToUserInfo($user_id)
{
    $url_params=array();
    if(isInRequest("tab1_selected"))
        $url_params[]="tab1_selected={$_REQUEST["tab1_selected"]}";
    $url_params[]=largeUrlSave("user_id_multi",$user_id);
        
    $redirect_str="/IBSng/admin/user/user_info.php?".join("&",$url_params);
    redirect($redirect_str);
}

function intSetSingleUserInfo(&$smarty,$user_id,$normal_username=null,$voip_username=null,$admin_caller=TRUE)
{
    $user_info_req=new GetUserInfo($user_id,$normal_username,$voip_username);
    $resp=$user_info_req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $user_info=$resp->getResult();
        if($admin_caller)
        {
            $user_info=array_values($user_info);
            $user_info=$user_info[0];
        }
        intSetSingleUserInfoIntoSmarty($smarty,$user_info);
    }
    else
        $resp->setErrorInSmarty($smarty);
    return $resp;
}

function intSetSingleUserInfoIntoSmarty(&$smarty,$user_info)
{
    $smarty->assign("user_id",$user_info["basic_info"]["user_id"]);
    $smarty->assign("user_info",$user_info);
    $smarty->assign("user_attrs",$user_info["attrs"]);
}

function intSetSingleUserGroupAttrs(&$smarty,$user_info)
{
    intSetGroupInfo($smarty,$user_info["basic_info"]["group_name"]);
}

function redirectToSearchAddUserSaves($msg="")
{
    $redirect_str="/IBSng/admin/user/search_add_user_saves.php";
    if($msg!="")
        $redirect_str.="?msg={$msg}";
    redirect($redirect_str);
}

function getNormalAndVoIPUsernames()
{ /* return a list of ($normal_username , $voip_username), based on authenticated user.
     one of usernames is null
  */
    $auth=getAuth();
    $normal_username = $voip_username = null;
    switch($auth->getAuthType())
    {
        case NORMAL_USER_AUTH_TYPE:
            $normal_username = getAuthUsername();
            break;
        case VOIP_USER_AUTH_TYPE:
            $voip_username = getAuthUsername();
    }
    return array($normal_username,$voip_username);
}

function intSetApproxDuration(&$smarty,$user_id)
{/* Set approx_duration in smarty object, 
    format is [[duration_seconds,ras_ip,day_of_weeks,interval_from,interval_to],...]
 */
    $req=new CalcApproxDuration($user_id);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $result=$resp->getResult();
        if(sizeof($result))
            $smarty->assign_by_ref("approx_duration",$result);
    }
    else        
        $resp->setErrorInSmarty($smarty);
}


?>
