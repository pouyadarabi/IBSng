<?php

function smarty_function_userMenuIcon($params,&$smarty)
{/*
    return a linked image html tags of menu icon
    parameter name(string,required): name of icon can be one of:
        home,change_pass,connection_log,credit_log

    parameter url_params(string,optional): optionally send params to linked page
    
*/
    $menu_selected=$smarty->get_assigned_value("selected");
    $image=getMenuIconImageLink($params["name"],$menu_selected);
    $url_params=isset($params["url_params"])?"?".$params["url_params"]:"";
    return <<<END
    <a href="/IBSng/user/{$params["name"]}.php{$url_params}" style="text-decoration:none"><img height=24 border=0 src="{$image}"></a>
END;

}

function getMenuIconImageLink($name,$menu_selected)
{
    $lang = getLang();
    $image_link="/IBSng/images/menu/user/{$lang}/menu_icon_".$name;
    if($menu_selected==$name)
        $image_link.="_selected";
    $image_link.=".gif";
    return $image_link;
}
?>