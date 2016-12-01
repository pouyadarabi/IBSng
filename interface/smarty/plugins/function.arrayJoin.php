<?php
function smarty_function_arrayJoin($params,&$smarty)
{/*

    param array(array,required): array that members will be joined
    param glue(string,required): glue of join
    param truncate_each(integer,optional): if set, truncate each member to this length
    param truncate(integer,optional): if set, truncate the result string to this length

*/

    require_once $smarty->_get_plugin_filepath('modifier', 'truncate');
    $arr=$params["array"];
    if (isset($params["truncate_each"]))
    {
        $new_arr=array();
        foreach($arr as $member)
            $new_arr[]=smarty_modifier_truncate($member,$params["truncate_each"],"",true);
        $arr=$new_arr;
    }
    
    $str=join($arr,$params["glue"]);
    
    if(isset($params["truncate"]))
        $str=smarty_modifier_truncate($str,$params["truncate"],"...",false);

    return $str;
}

?>