<?php
function smarty_function_ippool_names_select($params,&$smarty)
{/* return string of html select code for ippool selects.

    parameter name(string,required): html select name
    parameter id(string,optional): set optional dom ID
    parameter add_empty(boolean,optional): add an empty entry in select


    parameter default_var(string,optional): see getSelectedAttrFromSmartyParams comments
    parameter default_request(string,optional):
    parameter default_smarty(string,optional):
    parameter default(string,optional)
    parameter target(string,optional):

    
*/
    require_once($smarty->_get_plugin_filepath('function', 'html_options'));
    require_once(IBSINC."ippool.php");
    
    $req=new GetIPpoolNames();
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $names=$resp->getResult();
    else
        $names=array();
    
    if(isset($params["add_empty"]) and $params["add_empty"]=="TRUE")
        $names[]="";
        
    $selected=getSelectedAttrFromSmartyParams($smarty,$params);

    $select_arr=array("selected"=>$selected,"output"=>$names,"values"=>$names,"name"=>$params["name"]);

    if(isset($params["id"]))
        $select_arr["id"]=$params["id"];

    return smarty_function_html_options($select_arr,$smarty);
}
?>