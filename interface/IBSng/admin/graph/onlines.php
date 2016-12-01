<?php
require_once("../../inc/init.php");
require_once(IBSINC."graph.php");
require_once(IBSINC."snapshot.php");


needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();

if(isInRequest("show"))
    intShowGraph($smarty);
else
    face($smarty);

function intShowGraph(&$smarty)
{
    $url = convertRequestToUrl();
    $smarty->assign("img_path","/IBSng/admin/graph/onlines_img.php?{$url}");
    face($smarty);
}

function face(&$smarty)
{
    $smarty->display("admin/graph/onlines.tpl");
}
    
?>