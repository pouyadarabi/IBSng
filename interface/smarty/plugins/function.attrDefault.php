<?php
function smarty_function_attrDefault($params,&$smarty)
{/*

    param default_request(string,required): name of request key, that if has been set, will be returned as
                                            default, request is always prefered over other methods

    param target(string,required): attribute target, should be "user" or "group" that attribute default
                                    would be seek in it

    param default_var(string,required): name of target attribute, that if has been set, will be returned as
                                            default, this is preffered after default_request
                                            target attributes are searched through target array as set it target parameter
                                            

    param default(string,optional): optional string that will be returned if none of other default values matched

*/

    $target_attrs=getTargetAttrsFromSmarty($smarty,$params["target"]);
    $default=isset($params["default"])?$params["default"]:"";
    return attrDefault($target_attrs,$params["default_var"],$params["default_request"],$default);

}

?>