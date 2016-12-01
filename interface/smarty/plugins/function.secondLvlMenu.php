<?php
require_once(IBSINC."menu.php");

function smarty_function_secondLvlMenu($params,&$smarty)
{/*
    return secondLevel Menu from selected variable in smarty.
    selected should be set while including admin_header template
*/
    $menu_selected=get1stLvlSelected($smarty->get_assigned_value("selected"));
    $second_lvl_menu=get2ndLvlMenu($menu_selected);
    return create2ndLvlMenuFace($second_lvl_menu);
}

function create2ndLvlMenuFace($second_lvl_menu)
{
    $second_lvl_menu_tds=array();
    foreach($second_lvl_menu as $name=>$link)
        $second_lvl_menu_tds[]=secondLvlmenuTD($name,$link);
    return join(lineSpaceTD(),$second_lvl_menu_tds);
}

function secondLvlMenuTD($name,$link)
{
    return <<<END
    <td>
        <a class="Header_Submenu" href="{$link}">
            {$name}    
        </a>
    </td>
    
END;
}


function lineSpaceTD()
{
    return <<<END
    <td class="Header_Line_Between_Submenus"><img border="0" src="/IBSng/images/menu/line_between_submenus.gif"></td>
END;
}

?>