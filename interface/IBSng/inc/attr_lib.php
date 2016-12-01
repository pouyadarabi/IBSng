<?php
function attrDefault($target_attrs,$default_var,$default_request,$default="")
{/*
    return attribute default value, see attrDefault smarty plugin function for info about argumentes
*/
    if(isInRequest($default_request))
        return $_REQUEST[$default_request];
    else if (isset($target_attrs[$default_var]) and !is_null($target_attrs[$default_var]))
        return $target_attrs[$default_var];
    else
        return $default;
}

function getTargetAttrsFromSmarty(&$smarty,$target)
{
    if($target=="user")
        $target_attrs=$smarty->get_assigned_value("user_attrs");
    else if ($target=="group")
        $target_attrs=$smarty->get_assigned_value("group_attrs");
    else if ($target=="user_info")
        $target_attrs=$smarty->get_assigned_value("user_info");
    
    return $target_attrs;
}

function getSelectedAttrFromSmartyParams(&$smarty,&$params)
{/* Get selected value of an attr, from smarty object and smarty params.
    This function is useful for smarty plugins that needs to get what is value of selected

    param default_request(string,optional): name of request key, that if has been set, will be returned as
                                            default, request is always prefered over other methods

    param target(string,optional): attribute target, should be "user" or "group" that attribute default
                                    would be seek in it

    param default_var(string,optional): name of target attribute, that if has been set, will be returned as
                                            default, this is preffered after default_request
                                            target attributes are searched through target array as set it target parameter


    param default_smarty(string,optional): name of smarty variable that if has been set will be set after above 
                                            conditions failed

    param default(string,optional): optional string that will be returned if none of other default values matched
*/
    if(isset($params["default_var"]) and isset($params["default_request"]) and isset($params["target"]))
        $selected=attrDefault(getTargetAttrsFromSmarty($smarty,$params["target"]),
                              $params["default_var"],
                              $params["default_request"]);
    else if (isset($params["default_request"]) and isInRequest($params["default_request"]))
        $selected=$_REQUEST[$params["default_request"]];
    else if(isset($params["default_smarty"]) and $smarty->is_assigned($params["default_smarty"]))
        $selected=$smarty->get_assigned_value($params["default_smarty"]);
    else if(isset($params["default"]))
        $selected=$params["default"];
    else
        $selected="";

    return $selected;
}
?>