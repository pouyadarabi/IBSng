<?php
require_once("voip_tariff.php");

function redirectToTariffList($msg="")
{
    $url="/IBSng/admin/charge/voip_tariff/tariff_list.php";
    if($msg)
        $url.="?msg={$msg}";
    redirect($url);
}

function redirectToTariffInfo($tariff_name)
{
    redirect("/IBSng/admin/charge/voip_tariff/tariff_info.php?tariff_name={$tariff_name}");
}


function intSetTariffInfo(&$smarty,$tariff_name,$include_prefixes=True,$name_regex="")
{
    $req=new GetTariffInfo($tariff_name,$include_prefixes,$name_regex);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign_array($resp->getResult());
    else
        $resp->setErrorInSmarty($smarty);
}

function intAssignTariffNames(&$smarty)
{/*assign name of all voip tariff names, in an array with name "tariff_names"
*/
    $req=new ListTariffs();
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $tariff_names=array();
        foreach($resp->getResult() as $arr)
            $tariff_names[]=$arr["tariff_name"];
        $smarty->assign_by_ref("tariff_names",$tariff_names);
    }
    else
    {
        $resp->setErrorInSmarty($smarty);
        $smarty->assign("tariff_names",array());
    }
}
?>