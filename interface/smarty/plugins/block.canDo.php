<?php

function smarty_block_canDo($params,$content,&$smarty,&$repeat)
{
/*
    print block only if admin canDo "perm_name"
    if optional argument "username" is passed to this function it will checked with currently logged in user
    and block will be shown if "username" and authenticated user was the same. This is Useful 
    for pages that admin can see his info always, and other admin infos when he has permission.
    
    WARNING: perm.php and auth.php should be included by smarty object creator

*/
    if(is_null($content))
    {
        if(isset($params["username"]) and getAuthUsername()==$params["username"])
            return;
            
        if(canDo($params["perm_name"]))
            return;
            
        $repeat=FALSE;
    }
    else
        return $content;
    
}
?>