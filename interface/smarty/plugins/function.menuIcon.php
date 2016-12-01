<?php
require_once(IBSINC."menu.php");

function smarty_function_menuIcon($params,&$smarty)
{/*
    return a linked image html tags of menu icon
    parameter name(string,required): name of icon can be one of:
        user,group,admin,setting,report
    
*/
    $menu_selected=get1stLvlSelected($smarty->get_assigned_value("selected"));
    $image=getMenuIconImageLink($params["name"],$menu_selected);
    $link=get1stLvlLink($params["name"]);
    return <<<END
    <a href="{$link}" style="text-decoration:none"><img height=24 border=0 src="{$image}"></a>
END;

}

function getMenuIconImageLink($name,$menu_selected)
{
    $image_link="/IBSng/images/menu/menu_icon_".$name;
    if($menu_selected==$name)
        $image_link.="_selected";
    $image_link.=".gif";
    return $image_link;
}
?>