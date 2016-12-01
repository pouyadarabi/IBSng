<?php
function smarty_function_ifisinrequest($params,&$smarty)
{/*
    param name(string,required): name of key that is searched through request
    param default_var(string,optional): if name is not in request, return value of smarty variable
                                        default_var if it's available. if this param is not available or 
                                        value is not set in smarty, default will be returned

    param default(string,optional): default value, if name is not in request, and default var is not set in smarty
                                    default is returned.
                                    if this param is not available , return an empty string
    param value(string,optional): if this param is available , and name is in request or default_var was available
                                 , this param value will be returned. default behaviour is return value of name in $_REQUEST
                                  when this param is not available
*/
    if(isInRequest($params["name"]))
    {
        if (isset($params["value"]))
            return $params["value"];
        else
            return $_REQUEST[$params["name"]];
    }
    else
    {
        if(isset($params["default_var"]) and $smarty->is_assigned($params["default_var"]))
        {
            if (isset($params["value"]))
                return $params["value"];
            else
                return $smarty->get_assigned_value($params["default_var"]);
        }
        else
            return isset($params["default"])?$params["default"]:"";
    }
}

?>