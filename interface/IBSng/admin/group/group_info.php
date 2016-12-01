<?php
require_once("../../inc/init.php");
require_once(IBSINC."group.php");
require_once(IBSINC."group_face.php");
require_once(IBSINC."perm.php");
require_once(IBSINC."attr_parser.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();

if(isInRequest("group_name","delete_group"))
    intDelGroup($smarty,$_REQUEST["group_name"]);
else if(isInRequest("group_name"))
    intGroupInfo($smarty,$_REQUEST["group_name"]);
else
{
    $err=new error("INVALID_INPUT");
    redirectToGroupList($err->getErrorMsg());
}

function intDelGroup(&$smarty,$group_name)
{
    $req=new DelGroup($group_name);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToGroupList("Group Deleted Successfully");
    else
    {
        $resp->setErrorInSmarty($smarty);
        intGroupInfo($smarty,$group_name);
    }
}

function intGroupInfo(&$smarty,$group_name)
{
    intSetGroupInfo($smarty,$group_name);
  
	if($smarty->is_assigned("owner_name"))
	    $can_change = getCanChangeGroup($group_name, $smarty->get_assigned_value("owner_name"));    
	
	else	    
		$can_change = FALSE;
    
    $smarty->assign("can_change", $can_change);
    $smarty->assign("can_del",canDo("ADD NEW GROUP"));
    face($smarty);
}

function getCanChangeGroup($group_name, $group_owner)
{
	if(getAuthUsername() == $group_owner)
		return TRUE;

	else if(canDo("ACCESS ALL GROUPS"))
		return TRUE;
		
	else if(canDo("CHANGE GROUP",null,$group_name))
		return TRUE;
	
	return FALSE;			
}

function face(&$smarty)
{
    $smarty->display("admin/group/group_info.tpl");
}

?>