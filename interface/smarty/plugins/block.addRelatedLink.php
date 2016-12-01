<?php

function smarty_block_addRelatedLink($params,$content,&$smarty,&$repeat)
{
/*
    add a related link to related link side bar.
    related links will be shown in order they added
    return nothing so nothing will be printed 
*/
    if(!is_null($content))
    {
        global $related_links_menu;
        if(!isset($related_links_menu))
            $related_links_menu=array();
        $related_links_menu[]=$content;
    }
    
}
?>