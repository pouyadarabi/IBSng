<?php
function smarty_function_listTableHeaderIcon($params,&$smarty)
{/*     return a string, an image that will show the action text
        WARNING: this should be put before header listTR
        parameter action(string,required): action that will be showed in header
                                           options: "add","delete","edit","view", "detail", "enable", "disable", "kick", "clear"
        parameter close_tr(boolean,optional): optionally add an </tr> at the end. Useful when 
                                              it's the last icon in row

*/
    
    $action=$params["action"];
    $close_tr=(isset($params["close_tr"]) and $params["close_tr"]=="TRUE")?"</tr>":"";
    $link="/IBSng/images/list/list_header_{$action}.gif";

    return <<<EOF
                
                <td valign="bottom" Rowspan=2 class="List_Title_Icon">
                <img border="0" src="{$link}" title="{$action}"></td>   
            {$close_tr}
EOF;
}
?>