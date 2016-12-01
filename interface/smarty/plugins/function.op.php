<?php
function smarty_function_op($params,&$smarty)
{/* return a select html code of operands for a type of class 
    parameter class (required,string): can be on of "ltgteq", "likestr"
    parameter name (required,string): name of the select
    parameter selected (optional,string): optionally set the selected value of to the request value of this 
                                            param if set
    parameter id (optional,string): dom id
*/

    require_once $smarty->_get_plugin_filepath('function', 'html_options');
    $class=$params["class"];
    if($class=="ltgteq")
    {
        $face=array("=",">","<",">=","<=");
        $val=array("=",">","<",">=","<=");
    }
    else if ($class=="likestr")
    {
        $val=array("equals","like","ilike","starts_with","ends_with");
        $face=array("Equals","Like","ILike","Starts With","Ends With");
    }
    $selected=(isset($params["selected"]) and isset($_REQUEST[$params["selected"]]))?$_REQUEST[$params["selected"]]:"";
    $select_arr=array("output"=>$face,"values"=>$val,"name"=>$params["name"],"selected"=>$selected);
    if(isset($params["id"]))
        $select_arr["id"]=$params["id"];
    return smarty_function_html_options($select_arr,$smarty);
}
?>