<?php
function smarty_function_ifibserr($params,&$smarty)
{/*
    parameter varname: variable name that is tested
    parameter add: if varname is set and it's true, return this parameter as value of function
*/
    if ($smarty->is_assigned($params["varname"]) and $smarty->get_assigned_value($params["varname"])==TRUE)
        return $params["add"];
}

?>