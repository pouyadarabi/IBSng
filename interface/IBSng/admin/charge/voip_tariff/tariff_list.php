<?php
require_once("../../../inc/init.php");
require_once(IBSINC."voip_tariff_face.php");
require_once(IBSINC."voip_tariff.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
intTariffList($smarty);

function intSetTariffInfos(&$smarty)
{
    $req=new ListTariffs();
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $tariff_list=$resp->getResult();
        $smarty->assign_by_ref("tariffs", $tariff_list);
    }
    else
    {
        $resp->setErrorInSmarty($smarty);
        $smarty->assign("tariffs",array());
    }
}

function intTariffList(&$smarty)
{
    intSetTariffInfos($smarty);
    face($smarty);
}
function face(&$smarty)
{
    intSetErrors($smarty);
    $smarty->display("admin/charge/voip_tariff/tariff_list.tpl");
}

function intSetErrors(&$smarty)
{
    if(isInRequest("msg"))
        $smarty->set_page_error(array($_REQUEST["msg"]));
}


?>