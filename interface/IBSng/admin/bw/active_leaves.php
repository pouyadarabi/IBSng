<?php
require_once("../../inc/init.php");
require_once(IBSINC."bw_face.php");
require_once(IBSINC."bw.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
intActiveLeavesInterface($smarty);

function intSetAllActiveLeaves(&$smarty)
{
    $req=new GetAllActiveLeaves();
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign_by_ref("active_leaves",$resp->getResult());
    else
    {
        $resp->setErrorInSmarty($smarty);
        $smarty->assign("active_leaves",array());
    }
}

function intActiveLeavesInterface(&$smarty)
{
    intSetAllActiveLeaves($smarty);
    face($smarty);
}
function face(&$smarty)
{
    $smarty->assign("refresh_times",array(5,10,20,30,60));
    $smarty->assign("refresh_default",requestVal("refresh",20));
    $smarty->display("admin/bw/active_leaves.tpl");
}

?>