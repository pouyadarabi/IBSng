<?php

function smarty_block_layerTR($params,$content,&$smarty)
{/*     Create an Layer TR
        parameter cycle_color(boolean,optional): if set to "TRUE", call getTRColor with true argument so new
                                                 color is generated, only should be used with "body" type
*/
    
    if(!is_null($content))
    {
            $cycle_color=(isset($params["cycle_color"]) and $params["cycle_color"]=="TRUE")?True:False;
            $color=getTRColor($cycle_color,"layer_last_color");
            return <<<END
                    <tr class='Layer_Row_{$color}Color'>
                        {$content}
                    </tr>
END;
    }
}

?>