<?php
require_once("init.php");
require_once("group.php");


function redirectToGroupList($msg="")
{
    redirect("/IBSng/admin/group/group_list.php?msg={$msg}");
}

function redirectToGroupInfo($group_name,$extra_param="")
{
    $url_params=array("group_name={$group_name}");
    if(isInRequest("tab1_selected"))
        $url_params[]="tab1_selected={$_REQUEST["tab1_selected"]}";

    if($extra_param!="")
        $url_params[]=$extra_param;
    
    $redirect_str="/IBSng/admin/group/group_info.php?".join("&",$url_params);
    redirect($redirect_str);
}

function getGroupNames(&$smarty)
{ /* return number indexed(starting from 0... not group_id) array of group_names 
    on error an empty array is returned and a message is set in smart object
  */
    $group_names_req=new ListGroups();
    list($success,$groups)=$group_names_req->send();
    if($success)
        return $groups;
    else
    {
        $smarty->set_page_error($groups->getErrorMsgs());
        return array();
    }
}

function intSetGroupInfo(&$smarty,$group_name)
{
    $group_info_req=new GetGroupInfo($group_name);
    list($success,$group_info)=$group_info_req->send();
    if($success)
    {
        $smarty->assign_array($group_info);
        $smarty->assign("group_attrs",parseAttrs($smarty,$group_info["attrs"]));
    }
    else
        $smarty->set_page_error($group_info->getErrorMsgs());
}

function getGroupInfoWithCache($group_name)
{/*
    return array($success,$group_info) of group with name $group_name
    of failuer $success is false, and second member of returned array is error message
*/
    global $group_info_cache;
    if(!isset($group_info_cache))
        $group_info_cache=array();
    if(isset($group_info_cache[$group_name]))
        return array(TRUE,$group_info_cache[$group_name]);
    else
    {
        $req=new GetGroupInfo($group_name);
        $resp=$req->sendAndRecv();
        if($resp->isSuccessful())
        {
            $group_info_cache[$group_name]=$resp->getResult();
            return array(TRUE,$resp->getResult());
        }
        else
            return array(FALSE,$resp->getError());
    }
}

?>