<?php
function smarty_function_absDateSelect($params,&$smarty)
{/* return text input, calendar select, and date unit select html codes
    WARNING: util/calendar.tpl should be included in smarty before this method called
    parameter name (required,string): name of text input. _unit will be appended to this name, for select name of date unit
*/
    $select=createSelect($params,$smarty);
    $text_default=getSelectedAttrFromSmartyParams($smarty,$params);
    return <<<END
<input type=text name="{$params["name"]}" value="{$text_default}" id="{$params["name"]}_input" class="text">
<input type=image id="{$params["name"]}_calendar" onclick="ibs_setup_calendar('{$params["name"]}_input', '{$params["name"]}_calendar', '{$params["name"]}_select'); return false;" src="/IBSng/images/icon/calendar.gif">
{$select}
END;

}

function createSelect(&$params,&$smarty)
{
    require_once $smarty->_get_plugin_filepath('function', 'html_options');
    $new_params=array("default"=>"days");
    if(isset($params["default_request"]))
        $new_params["default_request"]=$params["default_request"]."_unit";

    if(isset($params["default_var"]))
        $new_params["default_var"]=$params["default_var"]."_unit";

    if(isset($params["target"]))
        $new_params["target"]=$params["target"];

    $select_default=getSelectedAttrFromSmartyParams($smarty,$new_params);
    $date_units=array("Minutes","Hours","Days","Months","Years","Gregorian","Jalali");
    $date_values=array("minutes","hours","days","months","years","gregorian","jalali");
    $select_arr=array("output"=>$date_units,
                      "values"=>$date_values,
                      "name"=>$params["name"]."_unit",
                      "selected"=>$select_default,
                      "id"=>"{$params["name"]}_select");
    return smarty_function_html_options($select_arr,$smarty);
}
?>