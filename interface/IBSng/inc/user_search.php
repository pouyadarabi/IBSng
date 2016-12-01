<?php
require_once("init.php");
require_once(IBSINC."user.php");
require_once(INTERFACE_ROOT."IBSng/admin/user/search_user_funcs.php");

class SearchUser extends Request
{
    function SearchUser($conds,$from,$to,$order_by,$desc)
    {
        parent::Request("user.searchUser",array("conds"=>$conds,
                                                "from"=>$from,
                                                "to"=>$to,
                                                "order_by"=>$order_by,
                                                "desc"=>$desc));
    }
}

function redirectToUserSearch($url_conds)
{
    $redirect_url="/IBSng/admin/user/search_user.php?search=1&show_defaults=1&show_reports=1";
    if($url_conds!="") 
        $redirect_url.="&{$url_conds}";
    redirect($redirect_url."#show_results");
}

function redirectToUserSearchInc($conds)
{
    if(!isInRequest("search"))
    {
        $_REQUEST["search"]=1;
        $_REQUEST["show_defaults"]=1;
        $_REQUEST["show_reports"]=1;
    }
    foreach($conds as $key=>$value)
        $_REQUEST[$key]=$value;

    intDoSearch();
}

?>