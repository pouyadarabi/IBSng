<?php

function smarty_block_listTableHeader($params,$content,&$smarty,&$repeat)
{
/*
    create header of list table headers
    type(string,required): can be "left" or "right"
    cols_num(string,required): number of columns, required for left types

*/
    if(!is_null($content))
    {
        if($params["type"]=="left")
        {
            return <<<END
        <tr>
                <td colspan="{$params["cols_num"]}" valign="bottom">
                <!-- List Title Table -->
                <table border="0" cellspacing="0" cellpadding="0" class="List_Title">
                        <tr>
                                <td class="List_Title_Begin" rowspan="2"><img border="0" src="/IBSng/images/form/begin_form_title_red.gif"></td>
                                <td class="List_Title" rowspan="2">{$content}
END;
        }
        else
        {
            return <<<END
                                    <img border="0" src="/IBSng/images/arrow/arrow_orange_on_red.gif" width="10" height="10"></td>
                                <td class="List_Title_End" rowspan="2"><img border="0" src="/IBSng/images/list/end_of_list_title_red.gif" width="5" height="20"></td>
                                <td class="List_Title_Top_Line" align="right">{$content}</td>
                        </tr>
                        <tr>
                                <td class="List_Title_End_Line"></td>
                        </tr>
                </table>
                <!-- End List Title Table -->
                </td>
        </tr>
END;
        }
    }
}
?>