<?php
require_once("init.php");

class AddNewGroup extends Request
{
    function AddNewGroup($name,$comment)
    {
        parent::Request("group.addNewGroup",array("group_name"=>$name,
                                                 "comment"=>$comment,
                                                 ));
    }
}

class ListGroups extends Request
{
    function ListGroups()
    {
        parent::Request("group.listGroups",array());
    }
}

class GetGroupInfo extends Request
{
    function GetGroupInfo($group_name)
    {
        parent::Request("group.getGroupInfo",array("group_name"=>$group_name));
    }
}

class UpdateGroup extends Request
{
    function UpdateGroup($group_id,$group_name,$comment,$owner_name)
    {
        parent::Request("group.updateGroup",array("group_id"=>$group_id,
                                                  "group_name"=>$group_name,
                                                  "comment"=>$comment,
                                                  "owner_name"=>$owner_name));
    }
}

class UpdateGroupAttrs extends Request
{
    function UpdateGroupAttrs($group_name,$attrs,$to_del_attrs)
    {
        parent::Request("group.updateGroupAttrs",array("group_name"=>$group_name,
                                                       "attrs"=>$attrs,
                                                       "to_del_attrs"=>$to_del_attrs));
    }
}

class DelGroup extends Request
{
    function DelGroup($group_name)
    {
        parent::Request("group.delGroup",array("group_name"=>$group_name));
    }
}


function getAllGroupInfos()
{
    /*
        returns (TRUE,group_infos) or (FALSE,$err_obj)
        group_infos: a list of associative dictionaries containing all group informations
    */
    $group_infos=array();
    $group_names_request=new ListGroups();
    list($success,$group_names)=$group_names_request->send();
    if(!$success)
        return array(FALSE,$group_names);
    $group_info_request=new GetGroupInfo("");
    foreach($group_names as $group_name)
    {
        $group_info_request->changeParam("group_name",$group_name);
        list($success,$group_info)=$group_info_request->send();
        if(!$success)
            return array(FALSE,$group_info);
        $group_infos[]=$group_info;
    }
    return array(TRUE,$group_infos);
}

?>