<?php
require_once("../../inc/init.php");
require_once(IBSINC."bw_face.php");
require_once(IBSINC."bw.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();
if(isInRequest("add","interface_name","leaf_name","parent_id","total_rate_kbits","total_ceil_kbits","default_rate_kbits","default_ceil_kbits"))
    intAddLeaf($smarty,
               $_REQUEST["interface_name"],
               $_REQUEST["leaf_name"],
               $_REQUEST["parent_id"],
               $_REQUEST["total_rate_kbits"],
               $_REQUEST["total_ceil_kbits"],
               $_REQUEST["default_rate_kbits"],
               $_REQUEST["default_ceil_kbits"]);
else if (isInRequest("add","interface_name","parent_id"))
    addInterface($smarty,$_REQUEST["interface_name"],$_REQUEST["parent_id"]);
else if(isInRequest("edit","interface_name","leaf_id","leaf_name","old_leaf_name","total_rate_kbits","total_ceil_kbits","default_rate_kbits","default_ceil_kbits"))
    intUpdateLeaf($smarty,
               $_REQUEST["interface_name"],
               $_REQUEST["leaf_id"],
               $_REQUEST["leaf_name"],
               $_REQUEST["old_leaf_name"],
               $_REQUEST["total_rate_kbits"],
               $_REQUEST["total_ceil_kbits"],
               $_REQUEST["default_rate_kbits"],
               $_REQUEST["default_ceil_kbits"]);
else if (isInRequest("edit","interface_name","leaf_name"))
    editInterface($smarty,$_REQUEST["interface_name"],$_REQUEST["leaf_name"]);

else
    redirectToInterfaceList();


function intUpdateLeaf(&$smarty,$interface_name,$leaf_id,$leaf_name,$old_leaf_name,$total_rate_kbits,$total_ceil_kbits,$default_rate_kbits,$default_ceil_kbits)
{
    $req=new UpdateLeaf($leaf_id,$leaf_name,$default_rate_kbits,$default_ceil_kbits,$total_rate_kbits,$total_ceil_kbits);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToInterfaceInfo($interface_name);
    else
        editInterface($smarty,$interface_name,$old_leaf_name,$resp->getError());
}

function editInterface(&$smarty,$interface_name,$leaf_name,$err=null)
{
    $req=new GetLeafInfo($leaf_name);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign_array($resp->getResult());
    else
        $resp->setErrorInSmarty($smarty);
    intEditAssignValues($smarty,$interface_name);
    face($smarty,$err);
}

function intAddLeaf(&$smarty,$interface_name,$leaf_name,$parent_id,$total_rate_kbits,$total_ceil_kbits,$default_rate_kbits,$default_ceil_kbits)
{
    $req=new AddLeaf($leaf_name,$parent_id,$default_rate_kbits,$default_ceil_kbits,$total_rate_kbits,$total_ceil_kbits);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToInterfaceInfo($interface_name);
    else
        addInterface($smarty,$interface_name,$parent_id,$resp->getError());
}

function addInterface(&$smarty,$interface_name,$parent_id,$err=NULL)
{
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
    $smarty->display("admin/bw/add_leaf.tpl");
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
    $smarty->set_field_errs(array("default_limit_kbits_err"=>array("INVALID_LIMIT_KBITS"),
                                  "total_limit_kbits_err"=>array("INVALID_TOTAL_LIMIT_KBITS"),
                                  "leaf_name_err"=>array("INVALID_LEAF_NAME","LEAF_NAME_ALREADY_EXISTS")
                            ),$err_keys);
}

?>