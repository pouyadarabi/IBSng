<?php

function smarty_block_tabTable($params,$content,&$smarty,&$repeat)
{
    require_once(IBSINC."tab.php");
/*
    create header and footer of an tab constructs
    parameter tabs(string,required): "," seperated list of tab ids. tab ids are used for labling tabs and also used for
                                     dom ids, so they must be unique. They can contain white spaces 
        
    parameter form_name(string, optional): form name, tab contents beloging to. This form is used
                                           to preserve selected tab after page submission

    parameter content_height(integer,optional): set height of contents, if this value is small, you'll see tab goes
                                                up n down

    parameter action_icon(boolean,optional): Tells which icon to use for form submit
                                             Can be on of "edit" "delete" "add" "load" "save" or "ok"
                                             default is "ok"

    parameter bgcolor(string,optional): set background color of table
    
    parameter tab_each_row(integer, optional): set number of tabs in each row, default 10
    parameter table_width(integer,optional): set table width, default is 430

    parameter tab_color(string,optional): set tab color between red and orange, default is red
*/
    if(!is_null($content))
    {
        $table_id=getTabTableID(FALSE);

        $tab_each_row = isset($params["tab_each_row"])?(int)$params["tab_each_row"]:10;
        $height=isset($params["content_height"])?$params["content_height"]:200;
        $width=isset($params["table_width"])?$params["table_width"]:430;

        $tab_color=isset($params["tab_color"])?$params["tab_color"]:"red";

        $bgcolor=isset($params["bgcolor"])?$params["bgcolor"]:"#efefef";
        $form_name=isset($params["form_name"])?$params["form_name"]:"";

        $tabs=explode(",",$params["tabs"]);

        $buttons=createButtons($tabs,$table_id, $tab_each_row, $tab_color);
        $tab_table=createTabTable($buttons,$content,$table_id,$height,$width,$params["action_icon"],$bgcolor,$tab_color,$form_name);
        return checkSelectedTab($table_id, $tab_table, $tabs);
    }
    else
        $table_id=getTabTableID(TRUE);
        
}


function createBeginButton($tab_name, $table_id, $init_color )
{
    $tab_id=tabName2TabID($tab_name);
    $tab_name=fixTabName($tab_name);
    return <<<END
                <!-- Begin Button -->
                <tr>

                <td rowspan="2" class="Tab_Title_begin">
                        <img border="0" src="/IBSng/images/tab/begin_of_tab_{$init_color}.gif" width="8" height="20" id="{$table_id}_{$tab_id}_begin"></td>
                <td rowspan="2" class="Tab_Title" id="{$table_id}_{$tab_id}_td" onMouseDown="return false;">{$tab_name}</td>
                <td rowspan="2" class="Tab_Title_end">
                        <img border="0" src="/IBSng/images/tab/end_of_tab_{$init_color}.gif" width="5" height="20" id="{$table_id}_{$tab_id}_end"></td>
        
                <!-- End Begin Button -->
                <script>
                    {$table_id}.addTab("{$table_id}_{$tab_id}");
                </script>
END;

}

function createMidButton($tab_name,$table_id,$tab_color)
{
    $tab_id=tabName2TabID($tab_name);
    $tab_name=fixTabName($tab_name);
    return <<<END
                <!-- mid button -->
                <td rowspan="2" class="Tab_Title_begin">
                        <img border="0" src="/IBSng/images/tab/begin_of_tab_gray_{$tab_color}.gif" width="8" height="20" id="{$table_id}_{$tab_id}_begin"></td>
                <td  rowspan="2" class="Tab_Title" id="{$table_id}_{$tab_id}_td" onMouseDown="return false;">{$tab_name}</td>
                <td rowspan="2" class="Tab_Title_end">
                        <img border="0" src="/IBSng/images/tab/end_of_tab_gray_{$tab_color}.gif" width="5" height="20" id="{$table_id}_{$tab_id}_end"></td>
                <!--end mid button -->
                <script>
                    {$table_id}.addTab("{$table_id}_{$tab_id}");
                </script>
END;

}

function createButtons(&$tab_names,$table_id, $tab_each_row, $tab_color)
{
    $c = 0;
    $ret = "";
    
    foreach ($tab_names as $tab_name)
    {
        if($c == 0)
        {
            $ret .= "<tr>";
            $ret .= createBeginButton($tab_name, $table_id, $tab_color);
        }
        else if($c % $tab_each_row == 0)
        {
            $ret .= "</tr><tr>";
            $ret .= createBeginButton($tab_name, $table_id, "gray_{$tab_color}");
        }
        else
            $ret .= createMidButton($tab_name, $table_id, $tab_color);
        $c ++ ;
    }
    return $ret;
}

function createTabTable($buttons,$content,$table_id,$height,$width,$action_icon,$bgcolor,$tab_color,$form_name)
{
        $ret=<<<END
<script>
    {$table_id}=new Tab('{$tab_color}');
    {$table_id}.setFormName('$form_name');
</script>

<table border="0" cellspacing="0" cellpadding="0" width="{$width}" valign="top">
        <tr><td>
            <table border="0" cellspacing="0" cellpadding="0" width="100%" valign="top">
                {$buttons}
                <td class="Tab_Title_Top_Line" colspan=20></td></tr>    
                <tr>
                <td class="Tab_Title_End_Line_{$tab_color}" colspan=20 rowspan=3></td></tr>
                </table>
        </td></tr>
        <tr>
                <td  height=1></td>
        </tr>
        <tr>
                <td  height={$height} valign=top bgcolor="{$bgcolor}" width="100%">
                    {$content}
                </td>
        </tr>

        <tr>
                <td>
                        <table border="0" cellspacing="0" cellpadding="0" class="Form_Foot">
                                <tr>
                                        <td class="Form_Foot_Begin_Line_red"></td>
END;
        if($action_icon=="")
        {
        
        }       
        else
        {
            $ret .= <<<END
                <td rowspan="2" class="Form_Foot_End"><img border="0" src="/IBSng/images/list/end_of_line_bottom_of_table.gif"></td>
                <td rowspan="2" class="Form_Foot_Buttons"><input type=image src="/IBSng/images/icon/{$action_icon}.gif"></td>
END;
        }

            $ret .= <<<END
                                </tr>
                                <tr>
                                        <td class="Form_Foot_Below_Line_red"></td>
                                </tr>
                        </table>
                        <!-- End Form Foot Table -->
                </td>
        </tr>
</table>
END;
    return $ret;
}

function checkSelectedTab($table_id, &$tab_table, &$tabs)
{
    $selected_key = "{$table_id}_selected";
    if(isInRequest($selected_key) and in_array(tabID2TabName($_REQUEST[$selected_key]), $tabs))
        $tab_table .= "<script> 
                        {$table_id}.handleOnClick('{$table_id}_{$_REQUEST[$selected_key]}_td');
                        </script>";

    return $tab_table;
}

?>