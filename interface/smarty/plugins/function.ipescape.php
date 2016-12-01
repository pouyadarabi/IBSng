<?php
function smarty_function_ipescape($params,&$smarty)
{/*
    escape ip address so it can be used in input names
    param ip(string,required): ip address that will be escaped
    param assign(string,required): escaped ip will be assigned with this name
*/
    $smarty->assign($params["assign"],escapeIP($params["ip"]));
}

?>