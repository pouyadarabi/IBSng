<?php
function smarty_function_multiTablePad($params,&$smarty)
{/*
    enter arbitary amount of multiTableTDs, until index%go_until==0
    parameter last_index(integer,required): last index of multiTableTDs
    parameter go_until(integer,required): go until last_index is dividable by this
    parameter width(string,optional): optionally set width of right td

*/
    require_once($smarty->_get_plugin_filepath('block', 'multiTableTD'));
    $ret="";
    while($params["last_index"]%$params["go_until"])
    {
        $td_params=array("type"=>"left");
        $ret.=smarty_block_multiTableTD($td_params,"&nbsp;",$smarty);
        $td_params["type"]="right";
        if(isset($params["width"]))
            $td_params["width"]=$params["width"];
        $ret.=smarty_block_multiTableTD($td_params,"&nbsp;",$smarty);
        $params["last_index"]++;
    }
    return $ret;
}



?>