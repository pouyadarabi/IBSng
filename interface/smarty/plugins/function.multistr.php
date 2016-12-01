<?php
function smarty_function_multistr($params,&$smarty)
{/* 
    parameter form_name(string,required): name of form, multi string input text exists in
    parameter input_name(string,required): name of input text field
    parameter left_pad(boolean,optional): default to TRUE, tell the multi str to left pad numbers


    return string, a linked image that will show dicomposed multi string
*/
    if((isset($params["left_pad"]) and $params["left_pad"]=="TRUE") or !isset($params["left_pad"]))
        $left_pad="t";
    else
        $left_pad="f";
    return <<<EOF
<a href="javascript:showMultiStr('{$params["form_name"]}','{$params["input_name"]}','{$left_pad}')" title="Show All Strings" style="text-decoration: none">
    <img src="/IBSng/images/icon/multistr_icon.gif" border=0>
</a>
EOF;
}
?>