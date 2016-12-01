<?php
require_once("bw.php");

function redirectToInterfaceList($msg="")
{
    $url="/IBSng/admin/bw/interface_list.php";
    if($msg!="")
        $url.="?msg={$msg}";
    redirect($url);
}

function redirectToBwStaticIPList($msg="")
{
    $url="/IBSng/admin/bw/static_ip_list.php";
    if($msg!="")
        $url.="?msg={$msg}";
    redirect($url);
}

function redirectToInterfaceInfo($interface_name)
{
    redirect("/IBSng/admin/bw/interface_info.php?interface_name={$interface_name}");
}

function intAssignBwLeafNames(&$smarty,$add_empty_leaf=TRUE)
{/*
    set all leaf names in smarty variable leaf_names
    $add_empty_leaf tells if we should add an empty leaf name(means we don't want to use bandwidth management)
*/
    $req=new GetAllLeafNames();
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $names=$resp->getResult();
        if($add_empty_leaf)
            array_unshift($names,'');
        $smarty->assign_by_ref("leaf_names",$names);
    }
    else
    {
        $resp->setErrorInSmarty($smarty);
        $smarty->assign("leaf_names",array());
    }
}


function intSetInterfaceInfo(&$smarty,$interface_name)
{
    $req=new GetInterfaces();
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $result=$resp->getResult();
        $smarty->assign_array($result[$interface_name]);
    }
    else
        $resp->setErrorInSmarty($smarty);
}

function intSetAllBwStaticIPsInfo(&$smarty)
{
    $req=new GetAllBwStaticIPs();
    $resp=$req->sendAndRecv();
    if(!$resp->isSuccessful())
    {
        $resp->setErrorInSmarty($smarty);
        $smarty->assign("bw_static_ips",array());
        return;
    }
    $req=new GetBwStaticIPInfo("");
    $ips=$resp->getResult();
    $infos=array();
    foreach($ips as $ip)
    {
        $req->changeParam("ip_addr",$ip);
        $resp=$req->sendAndRecv();
        if($resp->isSuccessful())
            $infos[$ip]=$resp->getResult();
        else
            $resp->setErrorInSmarty($smarty);
    }
    $smarty->assign("bw_static_ips",$infos);
}

?>