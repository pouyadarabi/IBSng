<?php
require_once("../../../inc/init.php");
require_once(IBSINC."voip_tariff_face.php");
require_once(IBSINC."voip_tariff.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("add","tariff_name","comment"))
    intAddTariff($_REQUEST["tariff_name"],$_REQUEST["comment"]);
else if (isInRequest("edit","tariff_id","tariff_name","old_tariff_name","comment"))
    intUpdateTariff($_REQUEST["tariff_id"],$_REQUEST["tariff_name"],$_REQUEST["old_tariff_name"],$_REQUEST["comment"]);
else if (isInRequest("edit","tariff_name"))
    editInterface($_REQUEST["tariff_name"]);
else
    addInterface();

function intUpdateTariff($tariff_id,$tariff_name,$old_tariff_name,$comment)
{
    $req=new UpdateTariff($tariff_id,$tariff_name,$comment);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToTariffInfo($tariff_name);
    else
        editInterface($old_tariff_name,$resp->getError());
}

function editInterface($tariff_name,$err=null)
{
    $smarty=new IBSSmarty();
    intSetTariffInfo($smarty,$tariff_name,FALSE);
    
    $smarty->assign("action","edit");
    $smarty->assign("action_title","Edit");
    $smarty->assign("action_icon","ok");
    face($smarty,$err);
}

function intAddTariff($tariff_name,$comment)
{
    $req=new AddNewTariff($tariff_name,$comment);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToTariffInfo($tariff_name);
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
    $smarty->display("admin/charge/voip_tariff/add_edit_tariff.tpl");
}
function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("tariff_name_err"=>array("BAD_TARIFF_NAME",
                                                           "TARIFF_NAME_ALREADY_EXISTS")
                                                           ),$err_keys);
}

?>