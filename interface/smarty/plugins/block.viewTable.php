<?php

function smarty_block_viewTable($params,$content,&$smarty,&$repeat)
{
/*
    create header and footer of an View Style table
    parameter title(string,optional): Title of table that will be printed on top of table
    parameter table_width(string,optional): width of table, if not set, defaults are used
    parameter double(boolean,optional): Set Double table, double tables has two usable areas in 
                        each row. Also Double TR s should be used for content
    parameter nofoot(boolean,optional): if set to TRUE, do not print the last footer of table

    parameter arrow_color(string,optional): Set color of arrow
    parameter color(string,optional): Set color of table header, default is red
    parameter id(string,optional): set id of table

*/
    if(!is_null($content))
    {
        $title=isset($params["title"])?$params["title"]:"";
        if(isset($params["double"]) and $params["double"]=="TRUE")
        {
            $table_width_default=480;
            $colspans=9;
        }
        else
        {
            $table_width_default=280;
            $colspans=4;
        }

        if(isset($params["color"]))
            $color=$params["color"];
        else
            $color="red";

        if(isset($params["arrow_color"]))
            $arrow_color=$params["arrow_color"];
        else
            $arrow_color="orange";

        $table_width=isset($params["table_width"])?$params["table_width"]:$table_width_default;

        $id=isset($params["id"])?"id={$params["id"]}":"";
        $header=<<<END

<table class="Form_Main" width="{$table_width}" border="0" cellspacing="0" bordercolor="#000000" cellpadding="0" {$id}>
        <tr>
                <td colspan="{$colspans}">
                <!-- Form Title Table -->
                <table border="0" cellspacing="0" cellpadding="0" class="Form_Title">
                        <tr>
                                <td class="Form_Title_Begin"><img border="0" src="/IBSng/images/form/begin_form_title_{$color}.gif"></td>
                                <td class="Form_Title_{$color}">{$title} <img border="0" src="/IBSng/images/arrow/arrow_{$arrow_color}_on_{$color}.gif"></td>
                                <td class="Form_Title_End"><img border="0" src="/IBSng/images/form/end_form_title_{$color}.gif"></td>
                        </tr>
                </table>
                <!-- End Form Title Table  -->
                </td>
        </tr>
        <tr>
                <td colspan="{$colspans}" class="Form_Content_Row_Space"></td>
        </tr>

END;
        $footer=<<<END
            </table>
END;
        if(!isset($params["nofoot"]) or $params["nofoot"]!="TRUE")
        {
        $footer=<<<END
        <!-- view table Foot -->
        <tr class="List_Foot_Line_{$color}">
                <td colspan=30></td>
        </tr>
        <!-- End view table Foot-->
    {$footer}
<br />
END;
        }
    return $header.$content.$footer;    
    }
    
}
?>