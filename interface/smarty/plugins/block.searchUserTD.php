<?php
function smarty_block_searchUserTD($params,$content,&$smarty,&$repeat)
{/*
    create a search user td.

    parameter attr_name(str,required): name of attribute, if available on group or user attrs, it will be printed
                                       can be multiple attributes, seperated by ",".
                                       multiple attribute names are only useful if you have 2 or more relative attributes,
                                       that always happened to be together, ex. rel_exp_date and rel_exp_date_unit
    parameter user_id(int,required): user_id we're showing
    parameter attr_type(string,required): can be "attrs" or "basic"
*/

    if(is_null($content))
    {
        $user_attrs=getUserAttrs($smarty,$params["user_id"]);
        $val=getUserAttrValues($user_attrs,$params["attr_name"],$params["attr_type"]);
        $class="";
        $prefix="";
        if(is_null($val[0]) and $params["attr_type"]=="attrs")
        {
            $group_val=getGroupAttrValues($user_attrs,$params["attr_name"]);
            if(!is_null($group_val[0]))
            {
                $class="List_Col_Group";
                $prefix="<font size=1 color='#800000'>G-</font>";
                $val=$group_val;
            }
        }
    
        if(is_null($val[0]))
        {
            $repeat=FALSE;
            print "<td align=center>-------</td>";
        }
        else
        {
            $smarty->assign("search_value",$prefix.implode(" ",$val));
            $smarty->assign("search_class",$class);
        }
    }
    else
    {
        $class=$smarty->get_assigned_value("search_class");
        if(trim($content)=="")
            $content=$smarty->get_assigned_value("search_value");
        return <<<END
            <td class="{$class}" >{$content}</td>
END;
    }
}

function getUserAttrs(&$smarty,$user_id)
{
    $user_attrs=$smarty->get_assigned_value("user_infos");
    return $user_attrs[$user_id];
}

function getUserAttrValues(&$user_attrs,$attr_name,$attr_type)
{
    $attr_names=explode(",",$attr_name);
    $ret=array();
    foreach($attr_names as $attr_name)
        $ret[]=getUserAttrValue($user_attrs,$attr_name,$attr_type);
    return $ret;
}       

function getUserAttrValue(&$user_attrs,$attr_name,$attr_type)
{
    
    if($attr_type=="basic" and isset($user_attrs["basic_info"][$attr_name]))
        return $user_attrs["basic_info"][$attr_name];
    else if ($attr_type=="attrs" and isset($user_attrs["attrs"][$attr_name]))
        return $user_attrs["attrs"][$attr_name];
    else
        return null;
}

function getGroupAttrValues(&$user_attrs,$attr_name)
{
    $attr_names=explode(",",$attr_name);
    $ret=array();
    foreach($attr_names as $attr_name)
        $ret[]=getGroupAttrValue($user_attrs,$attr_name);
    return $ret;
}       

function getGroupAttrValue(&$user_attrs,$attr_name)
{
    $group_name=$user_attrs["basic_info"]["group_name"];
    list($success,$group_info)=getGroupInfoWithCache($group_name);
    if(!$success or !isset($group_info["attrs"][$attr_name]))
        return null;
    else
        return $group_info["attrs"][$attr_name];
}

?>