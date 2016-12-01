<?php
require_once("../../inc/init.php");
require_once(IBSINC."bw_face.php");
require_once(IBSINC."bw.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("add","ip_addr","tx_leaf_name","rx_leaf_name"))
    intAddBwStaticIP($_REQUEST["ip_addr"],$_REQUEST["tx_leaf_name"],$_REQUEST["rx_leaf_name"]);
else if (isInRequest("add"))
    addInterface();

else if (isInRequest("edit","static_ip_id","old_ip_addr","ip_addr","tx_leaf_name","rx_leaf_name"))
    intUpdateBwStaticIP($_REQUEST["static_ip_id"],$_REQUEST["old_ip_addr"],$_REQUEST["ip_addr"],$_REQUEST["tx_leaf_name"],$_REQUEST["rx_leaf_name"]);

else if (isInRequest("edit","ip_addr"))
    editInterface($_REQUEST["ip_addr"]);
else
    redirectToBwStaticIPList();

function intUpdateBwStaticIP($static_ip_id,$old_ip_addr,$ip_addr,$tx_leaf_name,$rx_leaf_name)
{
    $req=new UpdateBwStaticIP($static_ip_id,$ip_addr,$tx_leaf_name,$rx_leaf_name);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToBwStaticIPList();
    else
        editInterface($old_ip_addr,$resp->getError());
}

function editInterface($ip_addr,$err=null)
{
    $smarty=new IBSSmarty();
    $req=new GetBwStaticIPInfo($ip_addr);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $info=$resp->getResult();
        $tx_leaf_name=$info["tx_leaf_name"];
        $rx_leaf_name=$info["rx_leaf_name"];
        $smarty->assign_array($info);
    }   
    else
    {
        $resp->setErrorInSmarty($smarty);
        $tx_leaf_name="";
        $rx_leaf_name="";
    }
    intEditAssignValues($smarty,$tx_leaf_name,$rx_leaf_name);
    face($smarty,$err);
}

function intAddBwStaticIP($ip_addr,$tx_leaf_name,$rx_leaf_name)
{
    $req=new AddBwStaticIP($ip_addr,$tx_leaf_name,$rx_leaf_name);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToBwStaticIPList();
    else
        addInterface($resp->getError());
}

function addInterface($err=NULL)
{
    $smarty=new IBSSmarty();
    intAddAssignValues($smarty);
    face($smarty,$err);
}

function face(&$smarty,$err)
{
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/bw/add_static_ip.tpl");
}

function intAddAssignValues(&$smarty)
{
    intAssignBwLeafNames($smarty,FALSE);
    $smarty->assign("tx_leaf_selected",requestVal("tx_leaf_name"));
    $smarty->assign("rx_leaf_selected",requestVal("rx_leaf_name"));

    $smarty->assign("action","add");
    $smarty->assign("action_title","Add");
    $smarty->assign("action_icon","add");
}

function intEditAssignValues(&$smarty,$tx_leaf_name,$rx_leaf_name)
{
    intAssignBwLeafNames($smarty,FALSE);
    $smarty->assign("tx_leaf_selected",requestVal("tx_leaf_name",$tx_leaf_name));
    $smarty->assign("rx_leaf_selected",requestVal("rx_leaf_name",$rx_leaf_name));

    $smarty->assign("action","edit");
    $smarty->assign("action_title","Edit");
    $smarty->assign("action_icon","ok");
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("ip_err"=>array("INVALID_STATIC_IP","INVALID_IP_ADDRESS","STATIC_IP_EXISTS"),
                                  "leaf_name_err"=>array("INVALID_LEAF_NAME")
                                  ),$err_keys);
}

?>