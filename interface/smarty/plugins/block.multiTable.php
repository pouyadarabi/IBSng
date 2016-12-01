<?php

function smarty_block_multiTable($params,$content,&$smarty)
{/*     Create an Multi Style Table
    parameter id(str,optional): set dom id
    parameter style(str,optional): set table style
*/
    
    if(!is_null($content))
    {
    $id=isset($params["id"])?"id={$params["id"]}":"";
    $style=isset($params["style"])?"style={$params["style"]}":"";
    return <<<END
<table cellpadding=0 cellspacing=0 border=0 width=100% {$id} {$style}>
    {$content}
    </tr>
    <tr>
        <td bgcolor="#FFFFFF" colspan=30 height=2></td>
</tr>

</table>

END;

    }
}

?>