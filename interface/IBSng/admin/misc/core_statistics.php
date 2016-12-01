<?php
require_once("../../inc/init.php");
require_once(IBSINC."stats.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();
intShowStats($smarty);


function intShowStats(&$smarty)
{
    $req = new GetStatistics();
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("stats",$resp->getResult());
    else
        $resp->setErrorInSmarty($smarty);
    
    face($smarty);
}

function face(&$smarty)
{
    $smarty->display("admin/misc/core_statistics.tpl");
}

?>