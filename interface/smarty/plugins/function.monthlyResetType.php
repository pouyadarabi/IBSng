<?php
function smarty_function_monthlyResetType($params,&$smarty)
{/* return html code for monthly reset type
    parameter name (required,string): name of select

    parameter default_var(string,optional): see getSelectedAttrFromSmartyParams comments
    parameter default_request(string,optional):
    parameter default_smarty(string,optional):
    parameter default(string,optional)
    parameter target(string,optional):
*/
    require_once $smarty->_get_plugin_filepath('function', 'html_options');
    $select_default=getSelectedAttrFromSmartyParams($smarty,$params);
    $face=array("Gregorian","Jalali");
    $value=array("gregorian","jalali");
    return smarty_function_html_options(array("output"=>$face,
                                              "values"=>$value,
                                              "name"=>$params["name"],
                                              "id"=>$params["name"],
                                              "selected"=>$select_default)
                                        ,$smarty);    
}

?>