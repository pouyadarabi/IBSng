<?php
require_once("init.php");
require_once(IBSINC."group_face.php");
require_once(IBSINC."attrs.php");

function runUpdateMethod($update_methods,&$update_helper)
{/*     All user plugin udpate function should be named "{$update_method}PluginUpdate"
        $update_methods are set in smarty templates and will be passed to this function.
            it contains an array of update methods
        All update methods will get an $update_helper instance as their first argument. It must be 
            passed as refrence.
        The update method should just update update_helper attributes. update function will be called by caller

        pluginUpdateTest(&$update_helper)
*/
    foreach($update_methods as $update_method)
        eval("{$update_method}PluginUpdate(\$update_helper);");
}

function getUpdateMethodsArray()
{
    $update_methods=array();    
    foreach($_REQUEST as $key=>$value)
        if (preg_match("/^attr_update_method_[0-9]+$/",$key))
            $update_methods[]=$value;
    return $update_methods;
}


class BaseUpdateAttrsHelper
{
    function BaseUpdateAttrsHelper()
    {
        $this->to_update_attrs=array();
        $this->to_del_attrs=array();
    }

    function getToUpdateAttrs()
    {
        return $this->to_update_attrs;
    }

    function mustBeInRequest()
    {/* check if all needed arguments are in $_REQUEST array.
        if one of arguments aren't in $_REQUEST, show the interface again, with "INCOMPLETE REQUEST"
        error on top of page
    */
        $args=func_get_args();
        if(!call_user_func_array("isInRequest",$args))
            $this->showEditInterface(error("INCOMPLETE_REQUEST"));
    }

    function getGroupAttrs($group_name)
    {
        $group_info_req=new GetGroupInfo($group_name);
        list($success,$group_info)=$group_info_req->send();
        if($success)
            return $group_info["attrs"];
        else
            $this->showEditInterface($group_info);
    }

    function addToDelAttrs($attr_name)
    {
        $this->to_del_attrs[]=$attr_name;
    }

    function addToUpdateAttrs($attr_name,$attr_value)
    {
        $this->to_update_attrs[$attr_name]=$attr_value;
    }

    function addToUpdateFromRequest($key)
    {/* add $key and $_REQUEST["key"] as value to list of update attrs */
        $this->addToUpdateAttrs($key,$_REQUEST[$key]);
    }
}


class UpdateAttrsHelper extends BaseUpdateAttrsHelper
{       
    function UpdateAttrsHelper(&$smarty,$target,$target_id)
    {
        parent::BaseUpdateAttrsHelper();
        $this->smarty=&$smarty;
        $this->target=$target;
        $this->target_id=$target_id;
    }
    
    function updateTargetAttrs($return_after_send=TRUE)
    {
        return $this->_updateTargetAttrs($this->to_update_attrs,$this->to_del_attrs,$return_after_send);
    }

    function _updateTargetAttrs($updated_attrs,$to_del_attrs,$return_after_send=TRUE)
    {/*
        
        $return_after_send(boolean): if set to TRUE, function will return after executation of request
                                            and return array of ($success,$ret)
                                     if set to FALSE, function will redirect client based on reponse 
                                            of request.
    */
        if($this->target=="group")
            list($success,$ret)=$this->updateGroupAttrs($this->target_id,$updated_attrs,$to_del_attrs);
        else if($this->target=="user")
            list($success,$ret)=$this->updateUserAttrs($this->target_id,$updated_attrs,$to_del_attrs);

        if($return_after_send)
            return array($success,$ret);
        else
            $this->redirectBasedOnResponse($success,$ret);
    }
    
    function redirectBasedOnResponse($success,$ret)
    {
        if($success)
            $this->redirectToTargetInfo();
        else
            $this->showEditInterface($ret);
    }
    function updateGroupAttrs($group_name,$attrs,$to_del_attrs)
    {
        $update_grp_attrs=new UpdateGroupAttrs($group_name,$attrs,$to_del_attrs);
        list($success,$ret)=$update_grp_attrs->send();
        return array($success,$ret);
    }

    function updateUserAttrs($user_id,$attrs,$to_del_attrs)
    {
        $update_usr_attrs=new UpdateUserAttrs($user_id,$attrs,$to_del_attrs);
        list($success,$ret)=$update_usr_attrs->send();
        return array($success,$ret);
    }
    
    function redirectToTargetInfo()
    {/* redirect to Target info, normally called when update was sucessful
    */
        intRedirectToTarget($this->target,$this->target_id);
    }
    
    function setPageError($err)
    {
        if(!is_null($err))
            $this->smarty->set_page_error($err->getErrorMsgs());
    }
    
    function showEditInterface($err=null)
    {/* show target edit interface, normally called when update failed
        
    */
        $this->setPageError($err);
        if($this->target=="group")
            intEditGroup($this->smarty,$this->target_id);
        else if($this->target=="user")
            intEditUser($this->smarty,$this->target_id);

        exit();
    }
    
    function getTargetAttrs()
    {
        if($this->target=="group")
            return $this->getGroupAttrs($this->target_id);
    }
    
}

function intRedirectToTarget($target, $target_id)
{
    if($target=="group")
        redirectToGroupInfo($target_id);
    else if($target=="user")
        redirectToUserInfo($target_id);

}

?>