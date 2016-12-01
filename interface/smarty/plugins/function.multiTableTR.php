<?php
function smarty_function_multiTableTR($params,&$smarty)
{/*
    return <tr> close and opens for multiTables, this function should be positioned in special if in iterations to create
    trs

*/
    global $multi_table_color;
    changeMultiTableColor();
    $tr="";
    if(isset($params["begin_close_tr"]))
        $tr.="</tr>";
        
    $tr.=<<<END
        <tr>
            <td bgcolor="#FFFFFF" colspan=30 height=2></td>
        </tr>
        <tr class="list_row_{$multi_table_color}color"}>
END;
    return $tr;
}

function changeMultiTableColor()
{
    global $multi_table_color;
    if(!isset($multi_table_color))
        $multi_table_color="light";
    else
    {
        if($multi_table_color=="light")
            $multi_table_color="dark";
        else
            $multi_table_color="light";
    }
}


?>