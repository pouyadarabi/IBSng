<?php
require_once("../../inc/init.php");
require_once(IBSINC."bw_face.php");
require_once(IBSINC."bw.php");

$smarty=new IBSSmarty();
if(isInRequest("delete_ip","ip_addr"))
    intDelIPAddress($smarty,$_REQUEST["ip_addr"]);
else
    intBwStaticIPInterface($smarty);


function intDelIPAddress(&$smarty,$ip_addr)
{
    $req=new DelBwStaticIP($ip_addr);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("del_ip_success",TRUE);
    else
        $resp->setErrorInSmarty($smarty);
    intBwStaticIPInterface($smarty);
}

function intBwStaticIPInterface(&$smarty)
{
    intSetAllBwStaticIPsInfo($smarty);
    face($smarty);
}


function face(&$smarty)
{
    $smarty->display("admin/bw/static_ip_list.tpl");
}


?>