<?php

function smarty_block_layerTable($params,$content,&$smarty)
{/*     Create an Layer Table
*/
    
    if(!is_null($content))
    {
            return <<<END
            <table width=100% border=0 cellspacing=0 cellpadding=0>
                {$content}
            </table>    
            
END;
    }
}

?>