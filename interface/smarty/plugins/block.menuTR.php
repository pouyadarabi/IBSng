<?php

function smarty_block_menuTR($params,$content,&$smarty,&$repeat)
{/*
*/
    
    if(!is_null($content))
    {
        $ret=<<<END
        <tr>
                <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_light.gif"></td>
                <td class="Menu_Content_Row_light"> <img border="0" src="/IBSng/images/arrow/arrow_menu.gif"> {$content}</td>
                <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_light.gif"></td>
        </tr>
        <tr>
                <td colspan="3" class="Form_Content_Row_Space"></td>
        </tr>
END;
        return $ret;
    }
    
}

