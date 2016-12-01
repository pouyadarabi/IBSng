<?php

function smarty_block_addEditTable($params,$content,&$smarty,&$repeat)
{
/*
    create header and footer of an Add Edit Style table

    parameter title(string,optional): Title of table that will be printed on top of table
    parameter table_width(string,optional): width of table, if not set, defaults are used
    parameter double(boolean,optional): Set Double table, double tables has two usable areas in 
                        each row. Also Double TR s should be used for content
    parameter action_icon(boolean,optional): Tells which icon to use for form submit
                                             Can be on of "edit" "delete" "add" "load" "save" or "ok"
                                             default is "ok"

    parameter action_onclick(string,optional): optional javascript method that will be called on onClick event of
                                                action icon
    parameter nofoot(boolean,optional): if set to TRUE, do not print the last footer of table
    parameter color(string,optional): Set color of table header, default is red
    parameter arrow_color(string,optional): Set color of arrow

    parameter cancel_icon(boolean,optional): optionally add a cancel button


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

        $action_icon="ok";
        if(isset($params["action_icon"]) and in_array($params["action_icon"],array("edit","delete","add","ok","load","save")))
            $action_icon=$params["action_icon"];

        $table_width=isset($params["table_width"])?$params["table_width"]:$table_width_default;

        $header=<<<END

<table class="Form_Main" width="{$table_width}" border="0" cellspacing="0" bordercolor="#000000" cellpadding="0">
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

        if(!isset($params["nofoot"]))
        {
        $action_onclick=isset($params["action_onclick"])?"OnClick='return {$params["action_onclick"]}'":"";
        if(isset($params["cancel_icon"]))
            $cancel_icon=<<<END
                <td rowspan="2" class="Form_Foot_Buttons" valign=top>
                    <input type=image src="/IBSng/images/icon/cancel.gif" name="cancel">
                </td>
END;
        else
            $cancel_icon="";
        
        $footer=<<<END
        <tr>
                <td colspan="{$colspans}">
                        <table border="0" cellspacing="0" cellpadding="0" class="Form_Foot">
                            <tr>
                                        <td class="Form_Foot_Begin_Line_{$color}"></td>
                                        <td valign=top rowspan="2" class="Form_Foot_End"><img border="0" src="/IBSng/images/list/end_of_line_bottom_of_table.gif"></td>
                                        {$cancel_icon}
                                        <td rowspan="2" class="Form_Foot_Buttons">
                                            <input type=image src="/IBSng/images/icon/{$action_icon}.gif" {$action_onclick}>
                                        </td>
                                </tr>
                                <tr>
                                        <td class="Form_Foot_Below_Line_{$color}"></td>
                                </tr>
                        </table>
                        <!-- End Form Foot Table -->
                </td>
        </tr>
        {$footer}
        <br />
END;
      }

    return $header.$content.$footer;    
    }
    
}
?>