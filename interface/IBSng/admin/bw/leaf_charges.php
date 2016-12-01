<?php

require_once("../../inc/init.php");
require_once(IBSINC."bw.php");
require_once(IBSINC."bw_face.php");
require_once(IBSINC."user_search.php");


needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();

if(isInRequest("leaf_name","interface_name","redirect_to_user_search"))
    intShowLeafUsers($smarty, $_REQUEST["leaf_name"], $_REQUEST["interface_name"]);

else if (isInRequest("leaf_name","interface_name"))
    intShowLeafCharges($smarty, $_REQUEST["leaf_name"], $_REQUEST["interface_name"]);

else
    redirectToInterfaceList();

function intShowLeafCharges(&$smarty, $leaf_name, $interface_name)
{
    $charge_names = getLeafCharges($smarty, $leaf_name);
    if($charge_names == FALSE)
        $charge_names = array(); //error already set
        
    face($smarty, $leaf_name, $charge_names, $interface_name);
}


function intShowLeafUsers(&$smarty, $leaf_name, $interface_name)
{
    $charge_names = getLeafCharges($smarty, $leaf_name);
    if($charge_names === FALSE)
        face($smarty, $leaf_name, array(), $interface_name);

    else if (!sizeof($charge_names))
    {
        $smarty->set_page_error("Leaf is not used in any Charge");
        face($smarty, $leaf_name, array(), $interface_name);
    }
    else
    {
        $url_conds = array();
        foreach($charge_names as $charge_name)
            $url_conds[] = "normal_charge_{$charge_name}={$charge_name}";
        
        redirectToUserSearch("tab1_selected=Charge&".join("&", $url_conds));
    }
}



function face(&$smarty, $leaf_name, $charge_names, $interface_name)
{
    $smarty->assign_by_ref("charge_names", $charge_names);
    $smarty->assign("leaf_name", $leaf_name);
    $smarty->assign("interface_name", $interface_name);
    $smarty->display("admin/bw/leaf_charges.tpl");
}

function getLeafCharges(&$smarty, $leaf_name)
{
    $req=new GetLeafCharges($leaf_name);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        return $resp->getResult();
    else
    {
        $resp->setErrorInSmarty($smarty);
        return FALSE;
    }
}

?>