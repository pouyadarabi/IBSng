<?php
function smarty_function_attrUpdateMethod($params,&$smarty)
{/*
    return a hidden input that will tel the update php to use "update_method" for updating attrs too
    parameter update_method(string,required): update method that will be runned for update
    NOTE: string "PluginUpdate" will be concatanated to the method before actually running
*/
    $id=getAttrUpdateMethodID();
    return <<<END
    <input type=hidden name="attr_update_method_{$id}" value="{$params["update_method"]}">
END;
}


function getAttrUpdateMethodID()
{/*
    return a unique id for each attr update hidden input
*/
    global $attr_update_method_id;
    if (!isset($attr_update_method_id))
        $attr_update_method_id=0;
    else
        $attr_update_method_id+=1;
    return $attr_update_method_id;
}
?>