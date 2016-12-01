<?php
function smarty_function_radioButtonValue($params,&$smarty)
{/*
    param name(string,required): name of radio that will be search through the request
    param value(string,required): if value of name in request in equal to this return checked
    param default_checked(string,optional): if name is not available in request, return "checked" or not
*/
    return radioBoxValue($params["name"],$params["value"],isset($params["default_checked"]));
}

?>