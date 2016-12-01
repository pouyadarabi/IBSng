<?php

function smarty_block_ifHasAttr($params,$content,&$smarty,&$repeat)
{
/*
    return some dashes "---" if attribute doesn't exists in attributes array.
    attributes array are selected based on "object" parameter is one of "group_attrs" or "user_attrs"    

    parameter object(string,required): can be "user" or "group"
    parameter var_name(string,required): variable name that will be checked that if exists
                                         and set !== FALSE and is not null , we suppose we have the attribute 
    parameter alternate(string,optional): string that will be shown if object has not attr
                                          if not specified default it used
*/
    if(is_null($content))
    {
        if(hasAttr($params,$smarty))
            $repeat=TRUE;
        else
        {
            $repeat=FALSE;
            if(isset($params["alternate"]))
                $alternate=$params["alternate"];
            else
                $alternate="---------------";
            print "{$alternate}";
        }
    }
    else
        return $content;
    
}

function hasAttr(&$params,&$smarty)
{
        $attrs=getAttrsArray($params,$smarty);
        return (isset($attrs[$params["var_name"]]) and $attrs[$params["var_name"]]!==FALSE and !is_null($attrs[$params["var_name"]]));
}

function getAttrsArray(&$params,&$smarty)
{
    if($params["object"]=="user")
        return $smarty->get_assigned_value("user_attrs");
    else if ($params["object"]=="group")
        return $smarty->get_assigned_value("group_attrs");
}
?>