<?php
function smarty_function_checkBoxValue($params,&$smarty)
{/*
    return "checked" or "" (empty string), based on params.
    param name(string,required): name of checkbox that will be search through the request, if this is set, always return "checked
    param always_in_form(string,optional): name of a form element, that's guranteed to be in submitted form
                                           normally can be an hidden input that is always in request when form submitted
    param default_checked(string,optional): if it's first time we see the form, default_checked is used.
                                            first time is determined by checked, always_in_form param
*/
    if(isInRequest($params["name"]))
        return "checked";
    else if (isset($params["always_in_form"]) and isset($params["default_checked"]))
        if(!isInRequest($params["always_in_form"]) and $params["default_checked"]=="TRUE")
            return "checked";
    return "";
}

?>