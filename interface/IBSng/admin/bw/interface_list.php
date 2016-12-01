<?php
require_once("../../inc/init.php");
require_once(IBSINC."bw_face.php");
require_once(IBSINC."bw.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
intInterfaceList($smarty);

function intSetInterfaceInfos(&$smarty)
{
    $req=new GetInterfaces();
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign_by_ref("interfaces",$resp->getResult());
    else
    {
        $resp->setErrorInSmarty($smarty);
        $smarty->assign("interfaces",array());
    }
}

function intInterfaceList(&$smarty)
{
    intSetInterfaceInfos($smarty);
    face($smarty);
}
function face(&$smarty)
{
    intSetErrors($smarty);
    $smarty->display("admin/bw/interface_list.tpl");
}

function intSetErrors(&$smarty)
{
    if(isInRequest("msg"))
        $smarty->set_page_error(array($_REQUEST["msg"]));
}


?>