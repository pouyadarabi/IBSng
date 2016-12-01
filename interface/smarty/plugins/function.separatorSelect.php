<?php
function smarty_function_separatorSelect($params,&$smarty)
{/* return string of html select code for seperator selects.

    parameter name(string,required): html select name
    parameter id(string,optional): set optional dom ID

    parameter default_var(string,optional): see getSelectedAttrFromSmartyParams comments
    parameter default_request(string,optional):
    parameter default_smarty(string,optional):
    parameter default(string,optional)
    parameter target(string,optional):

    
*/
    require_once($smarty->_get_plugin_filepath('function', 'html_options'));
    
    $selected=getSelectedAttrFromSmartyParams($smarty,$params);
        
    $seps=array(",",";","TAB");
    $seps_out=array("Comma","Semi Colon","Tab");
    $select_arr=array("selected"=>$selected,"output"=>$seps_out,"values"=>$seps,"name"=>$params["name"]);

    if(isset($params["id"]))
        $select_arr["id"]=$params["id"];

    return smarty_function_html_options($select_arr,$smarty);
}
?>