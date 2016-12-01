<?php
require_once("../../inc/init.php");
require_once(IBSINC."ras_face.php");
require_once(IBSINC."ras.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();

//print_r($_REQUEST);

if(isInRequest("ras_ip","port_name","port_type","phone","comment"))
    intUpdatePort($smarty,$_REQUEST["ras_ip"],$_REQUEST["port_name"],$_REQUEST["port_type"],$_REQUEST["phone"],$_REQUEST["comment"]);
else if(isInRequest("ras_ip","port_name"))
    intEditPort($smarty,$_REQUEST["ras_ip"],$_REQUEST["port_name"]);
else
{
    $err=error("INVALID_INPUT");
    redirectToRasList($err->getErrorMsg());
}

function intUpdatePort(&$smarty,$ras_ip,$port_name,$port_type,$phone,$comment)
{
    $add_port_req=new UpdateRasPort($ras_ip,$port_name,$port_type,$phone,$comment);
    list($success,$err)=$add_port_req->send();
    if($success)
        redirectToRasInfo($ras_ip);
    else
    {
        $smarty->set_page_error($err->getErrorMsgs());
        intSetErrors($smarty,$err->getErrorKeys());     
        face($smarty,$ras_ip,$port_name);
    }
}

function intEditPort(&$smarty,$ras_ip,$port_name)
{
    $port_info_req=new GetRasPortInfo($ras_ip,$port_name);
    list($success,$port_info)=$port_info_req->send();
    if($success)
        face($smarty,$ras_ip,$port_name,$port_info);
    else
    {
        $smarty->set_page_error($port_info->getErrorMsgs());
        face($smarty,$ras_ip,$port_name,$port_info);    
    }
}

function face(&$smarty,$ras_ip,$port_name,$port_info=null)
{
    intAssignValues($smarty,$ras_ip,$port_name,$port_info);
    intSetPortTypes($smarty);
    $smarty->display("admin/ras/edit_port.tpl");    
}


function intAssignValues(&$smarty,$ras_ip,$port_name,$port_info)
{
    if(is_null($port_info))
        $port_info=array();

    $smarty->assign_array(array("ras_ip"=>$ras_ip,
                               "port_name"=>$port_name,
                               "port_type"=>requestValWithDefaultArr("port_type",$port_info),
                               "phone"=>requestValWithDefaultArr("phone",$port_info),
                               "comment"=>requestValWithDefaultArr("comment",$port_info)
                              ));
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("port_name_err"=>array("INVALID_PORT_NAME",
                                                      "RAS_DONT_HAVE_PORT"),
                                     "port_type_err"=>array("INVALID_PORT_TYPE")
                                    ),$err_keys);

}

?>