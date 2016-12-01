<?php

function smarty_block_listTable($params,$content,&$smarty)
{
/*
    create header and footer of an List Style table
    parameter table_width(string,optional): width of table, if not set, defaults are used
    parameter cols_num(integer,required): number of table columns, not required for no_header tables
    parameter title(string,optional): Title of table that will be printed on top of table
    parameter no_header(any,optional): if set, no header will be included in table
    parameter no_footer(any,optional): if set, no footer will be included in table

*/
    if(!is_null($content))
    {
        $title=isset($params["title"])?$params["title"]:"";
        $table_width=isset($params["table_width"])?"width={$params["table_width"]}":"";
        $header=<<<END
<table border="0"  class="List_Main" cellspacing="1" bordercolor="#FFFFFF" cellpadding="0" {$table_width}>
END;
    if(!isset($params["no_header"]))
    {
        $header.=<<<END
        <tr>
                <td colspan="{$params["cols_num"]}" valign="bottom">
                <!-- List Title Table -->
                <table border="0" cellspacing="0" cellpadding="0" class="List_Title">
                        <tr>
                                <td class="List_Title_Begin" rowspan="2"><img border="0" src="/IBSng/images/form/begin_form_title_red.gif"></td>
                                <td class="List_Title" rowspan="2">{$title} <img border="0" src="/IBSng/images/arrow/arrow_orange_on_red.gif" width="10" height="10"></td>
                                <td class="List_Title_End" rowspan="2"><img border="0" src="/IBSng/images/list/end_of_list_title_red.gif" width="5" height="20"></td>
                                <td class="List_Title_Top_Line">&nbsp;</td>
                        </tr>
                        <tr>
                                <td class="List_Title_End_Line"></td>
                        </tr>
                </table>
                <!-- End List Title Table -->
                </td>
END;
    }
    if(isset($params["no_foot"]))
        $footer="</table>";
    else
        $footer=<<<END
        <!-- List Foot -->
        <tr class="List_Foot_Line_red">
                <td colspan=30></td>
        </tr>
        <!-- End List Foot-->
</table>
<br>
END;
    return $header.$content.$footer;    
    }
    
}
?>