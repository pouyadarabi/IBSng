<?php
function smarty_function_listTableBodyIcon($params,&$smarty)
{/*     return a string, an image that will show the action
        return an empty string if action argument is not valid
        parameter action(string,required): action that will be showed in header
                                           options: "add","delete","edit","view", "details", "active", "deactive", "kick", "clear"
        parameter close_tr(boolean,optional): optionally add an </tr> at the end. Useful when 
                                              it's the last icon in row
        parameter cycle_color(boolean,optional): if set to "TRUE", call getTRColor with true argument so new
                                                 color is generated
*/
    
    $action=$params["action"];
    if(!in_array($action,array("add","delete","edit","view","active","deactive","details","kick","clear","enable","disable","graph","history","reply")))
        return "";
    $cycle_color=(isset($params["cycle_color"]) and $params["cycle_color"]=="TRUE")?TRUE:FALSE;
    $color=getTRColor($cycle_color);
    $link="/IBSng/images/list/list_body_{$action}_{$color}.gif";
    
    return <<<EOF
<img border="0" src="{$link}" width="25" height="20" title="{$action}">
EOF;
}
?>