<?php

function smarty_block_multiTableTD($params,$content,&$smarty)
{/*     Create an Multi Style Table, TD
        parameter type(string,required): can be either of "left" or "right"
        parameter width(string,optional): optionally set width of right tds
*/
    
    if(!is_null($content))
    {
        global $multi_table_color;
        if($params["type"]=="left")
        {
            return <<<END
        <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_{$multi_table_color}.gif"></td>
        <td class="Form_Content_multi_left"><nobr>{$content}</nobr></td>
END;
        }
        else
        {
            if(isset($params["width"]))
                $width="style='width:{$params["width"]}'";
            else
                $width="";
            return <<<END
        <td class="Form_Content_multi_right" {$width}>{$content}</td>
        <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_{$multi_table_color}.gif"></td>
END;
        }

    }
}

?>