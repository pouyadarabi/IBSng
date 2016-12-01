<?php
require_once("../../inc/init.php");
require_once(IBSINC."bw_face.php");
require_once(IBSINC."bw.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();
if(isInRequest("add","leaf_name","protocol","filter_type","filter_value","interface_name","rate_kbits","ceil_kbits"))
    intAddLeafService($smarty,
                      $_REQUEST["interface_name"],
                      $_REQUEST["leaf_name"],
                      $_REQUEST["protocol"],
                      $_REQUEST["filter_type"],
                      $_REQUEST["filter_value"],
                      $_REQUEST["rate_kbits"],
                      $_REQUEST["ceil_kbits"]);
else if (isInRequest("add","leaf_name","interface_name"))
    addLeafServiceInterface($smarty,$_REQUEST["interface_name"],$_REQUEST["leaf_name"]);
else if(isInRequest("edit","leaf_service_id","leaf_name","protocol","filter_type","filter_value","interface_name","rate_kbits","ceil_kbits"))
    intUpdateLeafService($smarty,
                      $_REQUEST["leaf_service_id"],
                      $_REQUEST["interface_name"],
                      $_REQUEST["leaf_name"],
                      $_REQUEST["protocol"],
                      $_REQUEST["filter_type"],
                      $_REQUEST["filter_value"],
                      $_REQUEST["rate_kbits"],
                      $_REQUEST["ceil_kbits"]);
else if (isInRequest("edit","leaf_name","interface_name","leaf_service_id"))
    editLeafServiceInterface($smarty,$_REQUEST["leaf_service_id"],$_REQUEST["interface_name"],$_REQUEST["leaf_name"]);
else
    redirectToInterfaceList("Invalid Input");


function intUpdateLeafService(&$smarty,$leaf_service_id,$interface_name,$leaf_name,$protocol,$filter_type,$filter_value,$rate_kbits,$ceil_kbits)
{
    $req=new UpdateLeafService($leaf_name,$leaf_service_id,$protocol,"{$filter_type} {$filter_value}",$rate_kbits,$ceil_kbits);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToInterfaceInfo($interface_name);
    else
        editLeafServiceInterface($smarty,$leaf_service_id,$interface_name,$leaf_name,$resp->getError());
}

function editLeafServiceInterface(&$smarty,$leaf_service_id,$interface_name,$leaf_name,$err=null)
{
    intSetServiceInfo($smarty,$leaf_name,$leaf_service_id);
    intEditAssignValues($smarty,$interface_name);
    face($smarty,$err);
}

function intSetServiceInfo(&$smarty,$leaf_name,$leaf_service_id)
{
    $req=new GetLeafInfo($leaf_name);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $leaf_info=$resp->getResult();
        foreach($leaf_info["services"] as $service)
        {
            if ($service["leaf_service_id"]==$leaf_service_id)
            {
                intAssignServiceInfo($smarty,$service);
                return;
            }
        }
        $smarty->set_page_error("Leaf Service with id {$leaf_service_id} not found");
    }
    else
        $resp->setErrorInSmarty($smarty);
}
function intAssignServiceInfo(&$smarty,&$service_info)
{
    $smarty->assign_array($service_info);
    list($filter_type,$filter_value)=explode(" ",$service_info["filter"]);
    $smarty->assign("filter_type_selected",requestVal("filter_type",$filter_type));
    $smarty->assign("protocol_selected",requestVal("protocol",$service_info["protocol"]));
    $smarty->assign("filter_value",$filter_value);
}

function intAddLeafService(&$smarty,$interface_name,$leaf_name,$protocol,$filter_type,$filter_value,$rate_kbits,$ceil_kbits)
{
    $req=new AddLeafService($leaf_name,$protocol,$filter_type . " " . $filter_value,$rate_kbits,$ceil_kbits);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToInterfaceInfo($interface_name);
    else
        addLeafServiceInterface($smarty,$interface_name,$leaf_name,$resp->getError());
}


function addLeafServiceInterface(&$smarty,$interface_name,$leaf_name,$err=null)
{
    intAddAssignValues($smarty,$interface_name,$leaf_name);
    face($smarty,$err);
}


function face(&$smarty,$err)
{
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/bw/add_leaf_service.tpl");
}

function intAddAssignValues(&$smarty,$interface_name,$leaf_name)
{
    intAssignSelectValues($smarty);
    $smarty->assign("interface_name",$interface_name);
    $smarty->assign("leaf_name",$leaf_name);
    $smarty->assign("action","add");
    $smarty->assign("action_title","Add");
    $smarty->assign("action_icon","add");
    $smarty->assign("protocol_selected",requestVal("protocol",""));
    $smarty->assign("filter_type_selected",requestVal("filter_types",""));
}

function intEditAssignValues(&$smarty,$interface_name)
{
    intAssignSelectValues($smarty);
    $smarty->assign("interface_name",$interface_name);
    $smarty->assign("action","edit");
    $smarty->assign("action_title","Edit");
    $smarty->assign("action_icon","ok");
}

function intAssignSelectValues(&$smarty)
{
    $smarty->assign("protocols",array("tcp","udp"));
    $smarty->assign("filter_types",array("sport"=>"Source Port(s)","dport"=>"Destination Port(s)"));
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("limit_kbits_err"=>array("INVALID_LIMIT_KBITS"),
                                  "leaf_name_err"=>array("INVALID_LEAF_NAME"),
                                  "filter_err"=>array("LEAF_HAS_THIS_FILTER","INVALID_FILTER"),
                                  "protocol_err"=>array("LEAF_HAS_THIS_FILTER","INVALID_PROTOCOL")
                            ),$err_keys);
}

?>