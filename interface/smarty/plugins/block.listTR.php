<?php

function smarty_block_listTR($params,$content,&$smarty)
{/*     Create list style row(TR)
        parameter type(text,required): Can be either of "header" or "body"
                                       "header" creates a header style TR and
                                       "body" creates a body style TR
        parameter cycle_color(boolean,optional): if set to "TRUE", call getTRColor with true argument so new
                                                 color is generated, only should be used with "body" type

        if type is "body" this arguments can be used too
        parameter hover_color(string,optional): new color that will be set when mouse is over TR
        parameter hover_location(string,optional): location of onClick attribute
*/
    
    if(!is_null($content))
        if($params["type"]=="header")
            return "<tr class=\"List_Head\">".$content."</tr>";
        else if ($params["type"]=="body")
        {
            $cycle_color=(isset($params["cycle_color"]) and $params["cycle_color"]=="TRUE")?True:False;
            $color=getTRColor($cycle_color);
            $hover="";
            if(isset($params["hover_location"]))
            {
                $hover_color=isset($params["hover_color"])?$params["hover_color"]:"#FFAA00";
                $hover=TRHover($hover_color,$params["hover_location"]);
            }
            return "<tr class=\"List_Row_{$color}Color\" {$hover}>".$content."</tr>";
        }
}

function TRHover($color,$location)
{
    return <<<END
    onMouseover="changeTRColor(this,'{$color}');" 
    onMouseout="changeTRColor(this,null);" 
    style="cursor: pointer;" 
    onClick="window.location='{$location}'"
END;
}

?>