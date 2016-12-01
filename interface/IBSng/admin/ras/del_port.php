<?php
require_once("../../inc/init.php");
require_once(IBSINC."ras_face.php");
require_once(IBSINC."ras.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("ras_ip","port_name"))
    intDelPort($_REQUEST["ras_ip"],$_REQUEST["port_name"]);
else
{
    $err=error("INVALID_INPUT");
    redirectToRasList($err->getErrorMsg());
}

function intDelPort($ras_ip,$port_name)
{
    $del_port_req=new DelRasPort($ras_ip,$port_name);
    list($success,$err)=$del_port_req->send();
    if($success)
        redirectToRasInfo($ras_ip);
    else
        errorInterface($ras_ip,$err);
}

function errorInterface($ras_ip,$err)
{
    $smarty=new IBSSmarty();
    $smarty->assign("ras_ip",$ras_ip);
    $smarty->set_page_error($err->getErrorMsgs());
    $smarty->display("admin/ras/del_port.tpl");
}

?>