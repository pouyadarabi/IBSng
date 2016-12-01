<?php

function smarty_function_rasCheckBoxes($params,&$smarty)
{/*
    parameter prefix(str, required): prefix of all ras check box names
    parameter add_show_hide_table(integer, optional): default to true, will add a show hide table wrapper
    parameter selected_desc(array, optional): list of selected descriptions
*/
    require_once(IBSINC."ras.php");
    require_once($smarty->_get_plugin_filepath('block','multiTable'));
    require_once($smarty->_get_plugin_filepath('block','multiTableTD'));
    require_once($smarty->_get_plugin_filepath('function','multiTableTR'));
    require_once($smarty->_get_plugin_filepath('function','multiTablePad'));

    $selected_desc = isset($params["selected_desc"])?$params["selected_desc"]:array();

    $ras_table = createRasTable($smarty, $params["prefix"], $selected_desc);
    if(!isset($params["add_show_hide_table"]) or $params["add_show_hide_table"]!="0")
        return createShowHideTable($smarty,$params["prefix"],$ras_table);
    else
        return $ras_table;
}

function createRasTable(&$smarty, $prefix, $selected_desc)
{
    $req=new GetRasDescriptions();
    $resp=$req->sendAndRecv();

    if($resp->isSuccessful())
    {
        $content="";
        $i=0;
        foreach($resp->getResult() as $ras_tuple)
        {
            $ras_desc = $ras_tuple[0];
            $ras_ip = $ras_tuple[1];
            
            if($i%4==0)
                $content.=smarty_function_multiTableTR(array(),$smarty);
                
            $checked=checkBoxValue("{$prefix}_{$i}", in_array($ras_desc, $selected_desc), "submit");
            
            $content.=smarty_block_multiTableTD(array("type"=>"left","width"=>"25%"),
                                "<input type=checkbox name='{$prefix}_{$i}' value='{$ras_ip}' {$checked}>",$smarty);
            $content.=smarty_block_multiTableTD(array("type"=>"right","width"=>"25%"),"{$ras_desc}",$smarty);
            $i++;
        }
        $content.=smarty_function_multiTablePad(array("last_index"=>$i,"go_until"=>4,"width"=>"25%"),$smarty);
        $content=smarty_block_multiTable(array(),$content,$smarty);
    }
    else
    {
        $err=$resp->getError();
        $content=$err->getErrorMsg();
    }
    return $content;    
}

function createShowHideTable(&$smarty,$prefix,$rases_content)
{
    $content= <<<END
<table width=100% border=0 cellspacing=0 cellpadding=0>
    <tr>
      <td>
        <a href="#" onClick="{$prefix}_container.toggle('{$prefix}_select_ras'); return false;"><img src="/IBSng/images/icon/show_hide_rases.gif" border=0></a>
      </td>
    </tr>
    <tr id="{$prefix}_select_ras">
        <td>
            {$rases_content}
        </td>
    </tr>
</table>
<script>
    {$prefix}_container=new DomContainer();
    {$prefix}_container.setOnSelect("display","");
    {$prefix}_container.setOnUnSelect("display","none");

    {$prefix}_container.addByID("{$prefix}_select_ras");

    {$prefix}_container.select(null);
</script>

END;
    return $content;
}

?>