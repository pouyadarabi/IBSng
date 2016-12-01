<?php

function smarty_function_requestToUrl($params,&$smarty)
{/*
    Convert Request to url, return the url string
    parameter ignore(str,optional): ignore this key in request, can be a list of keys, seperated by ","
    
*/
    $ignore_arr=array();
    if(isset($params["ignore"]))
        $ignore_arr=split($params["ignore"],",");
    return $_SERVER["PHP_SELF"]."?".convertRequestToUrl($ignore_arr);
}



?>