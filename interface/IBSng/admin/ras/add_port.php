<?php
require_once("../../inc/init.php");
require_once(IBSINC."ras_face.php");
require_once(IBSINC."ras.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("ras_ip","port_name","port_type","phone","comment"))
    intAddPort($_REQUEST["ras_ip"],$_REQUEST["port_name"],$_REQUEST["port_type"],$_REQUEST["phone"],$_REQUEST["comment"]);
else if(isInRequest("ras_ip"))
    face($_REQUEST["ras_ip"]);
else
{
    $err=error("INVALID_INPUT");
    redirectToRasList($err->getErrorMsg());
}

function intAddPort($ras_ip,$port_name,$port_type,$phone,$comment)
{
    $add_port_req=new AddRasPort($ras_ip,$port_name,$port_type,$phone,$comment);
    list($success,$err)=$add_port_req->send();
    if($success)
        redirectToRasInfo($ras_ip);
    else
        face($ras_ip,$err);

}

function face($ras_ip,$err=NULL)
{
    $smarty=new IBSSmarty();
    intAssignValues($smarty,$ras_ip);
    intSetPortTypes($smarty);
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/ras/add_port.tpl");    
}


function intAssignValues(&$smarty,$ras_ip)
{
    $smarty->assign_array(array("ras_ip"=>$ras_ip,
                               "port_name"=>requestVal("port_name"),
                               "port_type"=>requestVal("port_type"),
                               "phone"=>requestVal("phone"),
                               "comment"=>requestVal("comment")
                              ));
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("port_name_err"=>array("INVALID_PORT_NAME",
                                                      "RAS_ALREADY_HAS_PORT"),
                                     "port_type_err"=>array("INVALID_PORT_TYPE")
                                    ),$err_keys);

}


?>