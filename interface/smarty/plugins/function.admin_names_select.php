<?php
function smarty_function_admin_names_select($params,&$smarty)
{/* parameter name(string,required): html select name

    parameter default_var(string,optional): see getSelectedAttrFromSmartyParams comments
    parameter default_request(string,optional):
    parameter default_smarty(string,optional):
    parameter default(string,optional)
    parameter target(string,optional):


    parameter add_all(string,optional): if set to TRUE add All option to list of selects
    return string of html select code for admin names select.
*/
    
    $selected=getSelectedAttrFromSmartyParams($smarty,$params);

    require_once($smarty->_get_plugin_filepath('function', 'html_options'));
    require_once(IBSINC."admin_face.php");
    $admins=getAdminNames($smarty);
    if(isset($params["add_all"]) and $params["add_all"]=="TRUE")
        $admins["All"]="All";
    
    return smarty_function_html_options(array("selected"=>$selected,"output"=>$admins,"values"=>$admins,"name"=>$params["name"]),$smarty);
}
?>