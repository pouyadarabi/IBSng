<?php
function smarty_function_reportToShowCheckBox($params,&$smarty)
{/*
    create and return html code for checkboxes used in report forms, to tell which attribute should be shown in
        retport
    param name(string,required): name of checkbox that will be set
    param output(string,required): string that will be shown aside of checkbox
    param default_checked(string,optional): default to false, see function.checkBoxValue
    param always_in_form(string,optional): see function.checkBoxValue
    param value(string,optional): optionally set value of check box
    param container_name(string,optional): optionally add this check box to javascript container
    param form_name(string,optional): used with container_name to add this checkbox in javascript container

*/
    require_once($smarty->_get_plugin_filepath('function', 'checkBoxValue'));

    require_once($smarty->_get_plugin_filepath('block', 'multiTableTD'));

    $checked=smarty_function_checkBoxValue($params,$smarty);
    if(isset($params["container_name"]) and isset($params["form_name"]))
        $javascript=<<<END
            <script>
                {$params["container_name"]}.addByName('{$params["form_name"]}','{$params["name"]}');
            </script>
END;
    else
        $javascript="";
    $value=isset($params["value"])?$params["value"]:"";
    $ret=smarty_block_multiTableTD(array("type"=>"left"),"<input type=checkbox name={$params["name"]} {$checked} value='{$value}'>",$smarty);
    $ret.=smarty_block_multiTableTD(array("type"=>"right"),"{$params["output"]}",$smarty);
    return $ret.=$javascript;
}

?>