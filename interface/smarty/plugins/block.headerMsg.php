<?php

function smarty_block_headerMsg($params,$content,&$smarty,&$repeat)
{
/*
    used for messages on header of files, usually when some actions was done, and we want to inform user
    parameter var_name(string,optional): smarty variable name that if has been set to True, 
            the message will be shown

*/
    if(!is_null($content))
    {

        return <<<END
<table align=center border=0>
        <tr>
            <td align=left>
                <img border="0" src="/IBSng/images/msg/before_successful_msg.gif">
            </td>
            <td align=left class="error_messages">          
                {$content}
            </td>
        </tr>
</table>
<br>            
END;
    }
    else
    {
        if(isset($params["var_name"]))
        {
            $var_name=$params["var_name"];
            if(!($smarty->is_assigned($var_name) and $smarty->get_assigned_value($var_name)))
                $repeat=False;
        }
    }
}
?>