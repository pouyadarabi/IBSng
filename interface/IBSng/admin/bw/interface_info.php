<?php
require_once("../../inc/init.php");
require_once(IBSINC."bw_face.php");
require_once(IBSINC."bw.php");
require_once("interface_info_face.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();
if(isInRequest("interface_name","delete_leaf_service","leaf_service_id","leaf_name","leaf_id"))
    intDelLeafService($smarty,$_REQUEST["interface_name"],$_REQUEST["leaf_name"],$_REQUEST["leaf_id"],$_REQUEST["leaf_service_id"]);

else if(isInRequest("interface_name","delete_node","node_id"))
    intDelNode($smarty,$_REQUEST["interface_name"],$_REQUEST["node_id"]);

else if(isInRequest("interface_name","delete_leaf","leaf_name","leaf_id"))
    intDelLeaf($smarty,$_REQUEST["interface_name"],$_REQUEST["leaf_name"],$_REQUEST["leaf_id"]);

else if(isInRequest("interface_name","delete_interface"))
    intDelInterface($smarty,$_REQUEST["interface_name"]);

else if(isInRequest("interface_name"))
    intShowInterfaceInfo($smarty,$_REQUEST["interface_name"]);
else
    redirectToInterfaceList();

function intShowInterfaceInfo(&$smarty,$interface_name)
{
    $tree=createTree($smarty,$interface_name);
    $smarty->assign_by_ref("tree",$tree);
    intSetInterfaceInfo($smarty,$interface_name);
    $smarty->display("admin/bw/interface_info.tpl");    

}

function createTree(&$smarty,$interface_name)
{
    $req=new GetTree($interface_name);
    $resp=$req->sendAndRecv();
    if(!$resp->isSuccessful())
    {
        $resp->setErrorInSmarty($smarty);
        return "";
    }
    $root_node=$resp->getResult();
    return createSubTree($smarty,$root_node,"nothing");
}

function intDelLeafService(&$smarty,$interface_name,$leaf_name,$leaf_id,$leaf_service_id)
{
    $req=new DelLeafService($leaf_name,$leaf_service_id);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("delete_leaf_service_success",TRUE);
    else
        $resp->setErrorInSmarty($smarty);
        
    intShowLayer($smarty,"leaf",$leaf_id);
    intShowInterfaceInfo($smarty,$interface_name);
}
    
function intDelNode(&$smarty,$interface_name,$node_id)
{
    $req=new DelNode($node_id);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("delete_node_success",TRUE);
    else
    {
        $resp->setErrorInSmarty($smarty);
        intShowLayer($smarty,"node",$node_id);
    }
        
    intShowInterfaceInfo($smarty,$interface_name);
}

function intDelLeaf(&$smarty,$interface_name,$leaf_name,$leaf_id)
{
    $req=new DelLeaf($leaf_name);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("delete_leaf_success",TRUE);
    else
    {
        $resp->setErrorInSmarty($smarty);
        intShowLayer($smarty,"leaf",$leaf_id);
    }
        
    intShowInterfaceInfo($smarty,$interface_name);
}

function intDelInterface(&$smarty,$interface_name)
{
    $req=new DelInterface($interface_name);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToInterfaceList();
    else
        $resp->setErrorInSmarty($smarty);

    intShowInterfaceInfo($smarty,$interface_name);
}

function intShowLayer(&$smarty,$type,$id)
{
    $smarty->assign("show_layer_link","{$id}_{$type}_link");
}


?>