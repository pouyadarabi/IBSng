<?php

function smarty_block_ifUserHasAttr($params,$content,&$smarty,&$repeat)
{
/*
    SERIOUS WARNING: only usable with normal or voip auth types
    
    
    parameter user_id(integer, required): user_id that attribute will be checked for
    parameter attr_name(string, required): if attr_name is available in user_attrs content will be shown
*/
    require_once(IBSINC."user.php");

    if(is_null($content))
    {
        $user_id = $params["user_id"];
        $attr_name = $params["attr_name"];
        
        if(isInCache($user_id, $attr_name))
            $has_attr = getCacheValue($user_id, $attr_name);
        else
            $has_attr = userHasAttr($user_id, $attr_name);
        
        $repeat=FALSE;
        if(!is_null($has_attr)) // error occured
        {
            cacheValue($user_id, $attr_name, $has_attr);
            if($has_attr)
                $repeat=TRUE;
        }
    }
    else
        return $content;    
}

function userHasAttr($user_id, $attr_name)
{
    $user_info_req=new GetUserInfo($user_id);
    $resp=$user_info_req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $user_info=$resp->getResult();
        return isset($user_info["attrs"][$attr_name]);
    }
    else
    {
        toLog("ifUserHasAttr: " . $resp->getErrorMsg() );
        return null;
    }
}

function isInCache($user_id, $attr_name)
{
    return isset($_SESSION["{$user_id}_has_{$attr_name}"]);
}

function getCacheValue($user_id, $attr_name)
{
    return $_SESSION["{$user_id}_has_{$attr_name}"];
}

function cacheValue($user_id, $attr_name, $value)
{
    $_SESSION["{$user_id}_has_{$attr_name}"] = $value;
}


?>