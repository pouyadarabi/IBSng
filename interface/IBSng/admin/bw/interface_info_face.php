<?php
function createSubTree(&$smarty,&$node,$line)
{
    $req=new GetNodeInfo($node[0]);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $node_info=$resp->getResult();
    else
    {
        $resp->setErrorInSmarty($smarty);
        return "";
    }

    $rate_kbits=price($node_info["rate_kbits"]);
    $ceil_kbits=price($node_info["ceil_kbits"]);
    $n_table="<table align=center cellspacing=0 cellpadding=0 border=0 width=100%>";
    $n_table.="<tr>
                    <td align=center>"
                    .getLine($line).
                    "</td>
               </tr>";
    if($line!="nothing")
        $n_table.="<tr><td align=center>".verticalLineImage()."</td>";

    $n_table.="<tr>
                <td align=center>";
    $color="aqua";
    $n_table.=<<<END
                <table border="0" cellspacing="0" cellpadding="0" >
                        <tr>
                                <td class="Form_Title_Begin"><img border="0" src="/IBSng/images/form/begin_form_title_{$color}.gif"></td>
                                <td class="Form_Title_{$color}">
                                    <a href="#" id='{$node_info["node_id"]}_node_link' onClick="showReportLayer('{$node_info["node_id"]}_node_id',this,'right'); return false;" class="bw_node">
                                        R:{$rate_kbits}|C:{$ceil_kbits}&nbsp;kbits
                                    </a>
                                </td>
                                <td class="Form_Title_End"><img border="0" src="/IBSng/images/form/end_form_title_{$color}.gif"></td>
                        </tr>
                </table>
END;
    $n_table.=createNodeLayer($smarty,$node_info);
    $n_table.="</td></tr>";
    if(sizeof($node[2])!=0 or sizeof($node[1])!=0) //if node has no children
        $n_table.="<tr><td align=center>".verticalLineImage()."</td>";
        
    $n_table.="<tr><td><table cellspacing='0' cellpadding='0' width=100% border=0 bordercolor=blue align=center><tr>";
    for($i=0;$i<sizeof($node[1]);$i++)
    {
        $n_table.="<td valign=top>";
        if(sizeof($node[1])==1 and sizeof($node[2])==0)
            $nline="up";
        else if($i==0)
            $nline="left";
        else if (sizeof($node[2])==0 and $i==sizeof($node[1])-1)
            $nline="right";
        else
            $nline="all";

        $n_table.=createSubTree($smarty,$node[1][$i],$nline);
        $n_table.="</td>";

    }
    
    for($j=0;$j<sizeof($node[2]);$j++)
    {
        $n_table.="<td valign=top>";

        if(sizeof($node[1])==0 and sizeof($node[2])==1)
            $nline="up";
        else if(sizeof($node[1])==0 and $j==0)
            $nline="left";
        else if($j==sizeof($node[2])-1)
            $nline="right";
        else
            $nline="all";
        $n_table.=createLeafTable($smarty,$node[2][$j],$nline);

        $n_table.="</td>";
    }
    $n_table.="</tr></table></td></tr></table>";
    return $n_table;
}       

function getLine($line)
{
    switch($line)
    {
        case "left":
            return "<table align=right width=50% cellspacing=0 cellpadding=0 border=0><tr><td bgcolor='#757575' height=2></td></tr></table>";
        case "right":
            return "<table align=left width=50% cellspacing=0 cellpadding=0 border=0><tr><td bgcolor='#757575' height=2></td></tr></table>";
        case "up":
            return "<img src='/IBSng/images/bw/vertical_line_empty.gif'>";
        case "all":
            return "<table align=right width=100% cellspacing=0 cellpadding=0 border=0><tr><td bgcolor='#757575' height=2></td></tr></table>";
        case "nothing":
            return "";      
    }
}

function verticalLineImage()
{
    return "<img src='/IBSng/images/bw/vertical_line.gif'>";
}

function createLeafTable(&$smarty,$leaf_name,$line)
{
    $req=new GetLeafInfo($leaf_name);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $leaf_info=$resp->getResult();
    else
    {
        $resp->setErrorInSmarty($smarty);
        return "";
    }
    return createLeafHtml($smarty,$leaf_info,$line);
}

function createLeafHtml(&$smarty,$leaf_info,$line)
{
    $total_rate_kbits=price($leaf_info["total_rate_kbits"]);
    $default_rate_kbits=price($leaf_info["default_rate_kbits"]);
    $total_ceil_kbits=price($leaf_info["total_ceil_kbits"]);
    $default_ceil_kbits=price($leaf_info["default_ceil_kbits"]);

    $n_table="<table cellspacing=0 cellpadding=0 align=center border=0 width=100%>";
    $n_table.="<tr><td align=center>".getLine($line)."</td></tr>";
    $n_table.="<tr><td align=center>".verticalLineImage()."</td>";
    $n_table.="<tr><td>";
    $color="blue";
    $n_table.=<<<END
                <table border="0" cellspacing="0" cellpadding="0" align=center>
                        <tr>
                                <td class="Form_Title_Begin"><img border="0" src="/IBSng/images/form/begin_form_title_{$color}.gif"></td>
                                <td class="Form_Title_{$color}">
                                    <a href="#" id='{$leaf_info["leaf_id"]}_leaf_link' onClick="showReportLayer('{$leaf_info["leaf_id"]}_leaf_id',this,'right'); return false;" class="bw_node">
                                        {$leaf_info["leaf_name"]}
                                    </td>
                                </td>
                                <td class="Form_Title_End"><img border="0" src="/IBSng/images/form/end_form_title_{$color}.gif"></td>
                        </tr>
END;
    $n_table.=leafLimitTR("Total limit: <b>R:{$total_rate_kbits}|C:{$total_ceil_kbits}</b> kbits");
    $n_table.=leafLimitTR("Default limit: <b>R:{$default_rate_kbits}|C:{$default_ceil_kbits}</b> kbits");
    $n_table.="</table></td></tr>";
    $n_table.="</table>";
    return $n_table.createLeafLayer($smarty,$leaf_info);
}

function leafLimitTR($content)
{
    return <<<END
        <tr>
                <td class="Form_Content_Row_Begin"><img border="0" src="/IBSng/images/row/begin_of_row_light.gif"></td>
                <td class="bw_leaf_limit_content">{$content}</td>
                <td class="Form_Content_Row_End"><img border="0" src="/IBSng/images/row/end_of_row_light.gif"></td>
        </tr>
        <tr>
                <td colspan="3" class="Form_Content_Row_Space"></td>
        </tr>
END;
}       
function createLeafLayer(&$smarty,$leaf_info)
{
    require_once($smarty->_get_plugin_filepath('block', 'reportDetailLayer'));

    $params=array("name"=>$leaf_info["leaf_id"]."_leaf_id","title"=>"Leaf {$leaf_info["leaf_name"]} Informations");
    $content=<<<END
<table>
    <tr>
      <td>
        <a class="bw_layer" href="/IBSng/admin/bw/add_leaf.php?edit=1&leaf_name={$leaf_info["leaf_name"]}&interface_name={$leaf_info["interface_name"]}">
            <img src="/IBSng/images/arrow/arrow_menu.gif" border=0> Edit Leaf {$leaf_info["leaf_name"]}
        </a>
      </td>
    </tr>
    <tr>
      <td>
        <a class="bw_layer" href="/IBSng/admin/bw/interface_info.php?delete_leaf=1&leaf_name={$leaf_info["leaf_name"]}&interface_name={$leaf_info["interface_name"]}&leaf_id={$leaf_info["leaf_id"]}" onClick='return confirm("Are you sure?");'>
            <img src="/IBSng/images/arrow/arrow_menu.gif" border=0> Delete Leaf {$leaf_info["leaf_name"]}
        </a>
      </td>
    </tr>

    <tr>
      <td>
        <a class="bw_layer" href="/IBSng/admin/bw/leaf_charges.php?leaf_name={$leaf_info["leaf_name"]}&interface_name={$leaf_info["interface_name"]}">
            <img src="/IBSng/images/arrow/arrow_menu.gif" border=0> Charges with Leaf {$leaf_info["leaf_name"]}
        </a>
      </td>
    </tr>

    <tr>
      <td>
        <a class="bw_layer" href="/IBSng/admin/bw/leaf_charges.php?redirect_to_user_search=1&leaf_name={$leaf_info["leaf_name"]}&interface_name={$leaf_info["interface_name"]}">
            <img src="/IBSng/images/arrow/arrow_menu.gif" border=0> Users with Leaf {$leaf_info["leaf_name"]}
        </a>
      </td>
    </tr>

    <tr>
      <td>
        <a class="bw_layer" href="/IBSng/admin/bw/add_leaf_service.php?add=1&leaf_name={$leaf_info["leaf_name"]}&interface_name={$leaf_info["interface_name"]}">
            <img src="/IBSng/images/arrow/arrow_menu.gif" border=0> Add a new service
        </a>
      </td>
    </tr>

        <tr>
            <td>
END;
    $content.=createServicesTable($smarty,$leaf_info["services"],$leaf_info["interface_name"]);
    $content.=<<<END
            </td>
        </tr>
</table>
END;
    return smarty_block_reportDetailLayer($params,$content,$smarty);
}

function createServicesTable(&$smarty,$services,$interface_name)
{
    require_once($smarty->_get_plugin_filepath('block', 'listTable'));
    require_once($smarty->_get_plugin_filepath('block', 'listTR'));
    require_once($smarty->_get_plugin_filepath('block', 'listTD'));
    require_once($smarty->_get_plugin_filepath('function', 'listTableHeaderIcon'));
    require_once($smarty->_get_plugin_filepath('function', 'listTableBodyIcon'));


    $content=smarty_function_listTableHeaderIcon(array("action"=>"edit"),$smarty);
    $content.=smarty_function_listTableHeaderIcon(array("action"=>"delete","close_tr"=>"TRUE"),$smarty);
    

    $header=smarty_block_listTD(array(),"protocol",$smarty);
    $header.=smarty_block_listTD(array(),"filter",$smarty);
    $header.=smarty_block_listTD(array(),"rate&nbsp;kbits",$smarty);
    $header.=smarty_block_listTD(array(),"ceil&nbsp;kbits",$smarty);

    $content.=smarty_block_listTR(array("type"=>"header"),$header,$smarty);
    foreach($services as $service)
    {
        $tr=smarty_block_listTD(array(),$service["protocol"],$smarty);
        $tr.=smarty_block_listTD(array(),$service["filter"],$smarty);
        $tr.=smarty_block_listTD(array(),price($service["rate_kbits"]),$smarty);
        $tr.=smarty_block_listTD(array(),price($service["ceil_kbits"]),$smarty);
        $edit="<a href='/IBSng/admin/bw/add_leaf_service.php?edit=1&leaf_name={$service["leaf_name"]}&leaf_service_id={$service["leaf_service_id"]}&interface_name={$interface_name}' style='text-decoration:none'>";
        $edit.=smarty_function_listTableBodyIcon(array("action"=>"edit"),$smarty);
        $edit.="</a>";
        $tr.=smarty_block_listTD(array("icon"=>"TRUE"),$edit,$smarty);
        $delete="<a href='/IBSng/admin/bw/interface_info.php?delete_leaf_service=1&leaf_service_id={$service["leaf_service_id"]}&interface_name={$interface_name}&leaf_name={$service["leaf_name"]}&leaf_id={$service["leaf_id"]}' style='text-decoration:none' onClick='return confirm(\"Are you sure?\");'>";
        $delete.=smarty_function_listTableBodyIcon(array("action"=>"delete","close_tr"=>"TRUE","cycle_color"=>"TRUE"),$smarty);
        $delete.="</a>";
        $tr.=smarty_block_listTD(array("icon"=>"TRUE"),$delete,$smarty);
        $content.=smarty_block_listTR(array("type"=>"body"),$tr,$smarty);
    }
    return smarty_block_listTable(array("title"=>"services","cols_num"=>"4"),
                                      $content,
                                      $smarty
                                      );
}

function createNodeLayer(&$smarty,$node_info)
{
    require_once($smarty->_get_plugin_filepath('block', 'reportDetailLayer'));
    $params=array("name"=>$node_info["node_id"]."_node_id","title"=>"Node {$node_info["node_id"]} Informations");
    $content=<<<END
<table>
    <tr>
      <td>
        <a class="bw_layer" href="/IBSng/admin/bw/add_node.php?edit=1&node_id={$node_info["node_id"]}&interface_name={$node_info["interface_name"]}">
           <img src="/IBSng/images/arrow/arrow_menu.gif" border=0> Edit Node {$node_info["node_id"]}
        </a>
      </td>
    </tr>
    <tr>
      <td>
        <a class="bw_layer" href="/IBSng/admin/bw/interface_info.php?delete_node=1&node_id={$node_info["node_id"]}&interface_name={$node_info["interface_name"]}" onClick='return confirm("Are you sure?");'>
            <img src="/IBSng/images/arrow/arrow_menu.gif" border=0> Delete Node {$node_info["node_id"]}
        </a>
      </td>
    </tr>
    <tr>
      <td>
        <a class="bw_layer" href="/IBSng/admin/bw/add_node.php?add=1&parent_id={$node_info["node_id"]}&interface_name={$node_info["interface_name"]}">
            <img src="/IBSng/images/arrow/arrow_menu.gif" border=0> Add Child Node to {$node_info["node_id"]}
        </a>
      </td>
    </tr>
    <tr>
      <td>
        <a class="bw_layer" href="/IBSng/admin/bw/add_leaf.php?add=1&parent_id={$node_info["node_id"]}&interface_name={$node_info["interface_name"]}">
            <img src="/IBSng/images/arrow/arrow_menu.gif" border=0> Add Child Leaf to {$node_info["node_id"]}
        </a>
      </td>
    </tr>
</table>
END;
    return smarty_block_reportDetailLayer($params,$content,$smarty);
}
?>