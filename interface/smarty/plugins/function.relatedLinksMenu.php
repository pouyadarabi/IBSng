<?php
require_once(IBSINC."menu.php");

function smarty_function_relatedLinksMenu($params,&$smarty)
{/*
    return related link bar contents from previous addRelatedLink Calls
*/
    global $related_links_menu;
    $menu_temp=array();
    foreach($related_links_menu as $link)
        $menu_temp[]=relatedLinksLinkTD($link);
    return join(relatedLinksSpaceTD(),$menu_temp);
}


function relatedLinksLinkTD($content)
{
    return <<<END
        <tr>
                <td class="RightSide_Arrow"><img border="0" src="/IBSng/images/arrow/red_arrow.gif" width="6" height="10"></td>
                <td class="RightSide_links">{$content}</td>
        </tr>
END;
}

function relatedLinksSpaceTD()
{
    return <<<END
    <tr>
            <td colspan="2" class="RightSide_seperator"></td>
    </tr>
END;
}

?>