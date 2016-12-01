<?php

function smarty_block_listTD($params,$content,&$smarty)
{/*     Create an Add edit style column (TD).
        icon(boolean,optional): set style suitable for icon TDs
        extra(str,optional): optionally add extra attributes to td tag
*/
    
    if(!is_null($content))
    {
        $extra=isset($params["extra"])?$params["extra"]:"";
        if(isset($params["icon"]) and $params["icon"]=="TRUE")
        {
            $style="List_col_Body_Icon";
            $valign="Top";
        }
        else
        {
            $style="list_col";
            $valign="Middle";
        }
        
        return <<<END
    <td class="{$style}" valign="{$valign}" {$extra}>{$content}</td>
END;

    }


}

?>