<?php
require_once("../../inc/init.php");
require_once(IBSINC."bw_face.php");
require_once(IBSINC."bw.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("add","interface_name","parent_id","rate_kbits","ceil_kbits"))
    intAddNode($_REQUEST["interface_name"],$_REQUEST["parent_id"],$_REQUEST["rate_kbits"],$_REQUEST["ceil_kbits"]);
else if (isInRequest("add","interface_name","parent_id"))
    addInterface($_REQUEST["interface_name"],$_REQUEST["parent_id"]);

else if (isInRequest("edit","node_id","interface_name","rate_kbits","ceil_kbits"))
    intUpdateNode($_REQUEST["interface_name"],$_REQUEST["node_id"],$_REQUEST["rate_kbits"],$_REQUEST["ceil_kbits"]);

else if (isInRequest("edit","node_id","interface_name"))
    editInterface($_REQUEST["interface_name"],$_REQUEST["node_id"]);
else
    redirectToInterfaceList();

function intUpdateNode($interface_name,$node_id,$rate_kbits,$ceil_kbits)
{
    $req=new UpdateNode($node_id,$rate_kbits,$ceil_kbits);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToInterfaceInfo($interface_name);
    else
        editInterface($interface_name,$node_id,$resp->getError());
}

function editInterface($interface_name,$node_id,$err=null)
{
    $smarty=new IBSSmarty();
    intEditAssignValues($smarty,$interface_name);
    $req=new GetNodeInfo($node_id);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign_array($resp->getResult());
    else
        $resp->setErrorInSmarty($smarty);
    face($smarty,$err);
}

function intAddNode($interface_name,$parent_id,$rate_kbits,$ceil_kbits)
{
    $req=new AddNode($interface_name,$parent_id,$rate_kbits,$ceil_kbits);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToInterfaceInfo($interface_name);
    else
        addInterface($interface_name,$parent_id,$resp->getError());
}

function addInterface($interface_name,$parent_id,$err=NULL)
{
    $smarty=new IBSSmarty();
    intAddAssignValues($smarty,$interface_name,$parent_id);
    face($smarty,$err);
}

function face(&$smarty,$err)
{
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/bw/add_node.tpl");
}

function intAddAssignValues(&$smarty,$interface_name,$parent_id)
{
    $smarty->assign("interface_name",$interface_name);
    $smarty->assign("parent_id",$parent_id);
    $smarty->assign("action","add");
    $smarty->assign("action_title","Add");
    $smarty->assign("action_icon","add");
}

function intEditAssignValues(&$smarty,$interface_name)
{
    $smarty->assign("interface_name",$interface_name);
    $smarty->assign("action","edit");
    $smarty->assign("action_title","Edit");
    $smarty->assign("action_icon","ok");
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("limit_kbits_err"=>array("INVALID_LIMIT_KBITS")),$err_keys);
}

?>