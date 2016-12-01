<?php
function smarty_function_jsconfirm($params,&$smarty)
{/* return an onClick javascript statement, useful for confirming something.
    if parameter msg is passed, it will be shown as confirm message.
    if parameter raw_msg is passed, it will be shown without putting ' (qoute) before and after msg
        this is useful when caller wants to call javascript methos withing the message
    if no parameter passed, it will show "are you sure?" message
*/
    if(isset($params["msg"]))
        $msg="\"".$params["msg"]."\"";
    else if (isset($params["raw_msg"]))
        $msg=$params["raw_msg"];
    else
        $msg="\"Are You Sure?\"";
    return " onClick='return confirm({$msg})' ";
}

?>