<?php
require_once("../../inc/init.php");
require_once(IBSINC."bw_face.php");
require_once(IBSINC."bw.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("add","interface_name","comment"))
    intAddInterface($_REQUEST["interface_name"],$_REQUEST["comment"]);
else if (isInRequest("edit","interface_id","interface_name","old_interface_name","comment"))
    intUpdateInterface($_REQUEST["interface_id"],$_REQUEST["interface_name"],$_REQUEST["old_interface_name"],$_REQUEST["comment"]);
else if (isInRequest("edit","interface_name"))
    editInterface($_REQUEST["interface_name"]);
else
    addInterface();

function intUpdateInterface($interface_id,$interface_name,$old_interface_name,$comment)
{
    $req=new UpdateInterface($interface_id,$interface_name,$comment);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToInterfaceInfo($interface_name);
    else
        editInterface($old_interface_name,$resp->getError());
}

function editInterface($interface_name,$err=null)
{
    $smarty=new IBSSmarty();
    intSetInterfaceInfo($smarty,$interface_name);
    
    $smarty->assign("action","edit");
    $smarty->assign("action_title","Edit");
    $smarty->assign("action_icon","ok");
    face($smarty,$err);
}

function intAddInterface($interface_name,$comment)
{
    $req=new AddInterface($interface_name,$comment);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToInterfaceInfo($interface_name);
    else
        addInterface($resp->getError());
}

function addInterface($err=NULL)
{
    $smarty=new IBSSmarty();
    $smarty->assign("action","add");
    $smarty->assign("action_title","Add");
    $smarty->assign("action_icon","add");
    face($smarty,$err);
}

function face(&$smarty,$err)
{
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/bw/add_interface.tpl");    
}
function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("interface_name_err"=>array("INVALID_INTERFACE_NAME",
                                                           "INTERFACE_NAME_ALREADY_EXISTS")
                                                           ),$err_keys);
}

?>