<?php
require_once("../../../inc/init.php");
require_once(IBSINC."graph.php");
require_once(IBSINC."snapshot.php");


needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("username","user_id","ras_ip","unique_id_val"))
    intUserBwGraph($_REQUEST["username"],$_REQUEST["user_id"],$_REQUEST["ras_ip"],$_REQUEST["unique_id_val"]);
else
    intAllBWGraph();


function intUserBwGraph($username,$user_id,$ras_ip,$unique_id_val)
{
    $req = new GetBWSnapShotForUser($user_id,$ras_ip,$unique_id_val);
    $resp = $req->sendAndRecv();
    if($resp->isSuccessful())
    {   
        list($dates,$values) = $resp->getResult();
        intShowGraph($dates,$values,"Bw Usage for {$username}");
    }
    else
        toLog($resp->getErrorMsg());
}

function intAllBWGraph()
{
    intBWGraph("internet_bw","All Users BW");
}

function intBWGraph($snapshot_name,$title)
{
    $req = new GetRealTimeSnapShot($snapshot_name);
    $resp = $req->sendAndRecv();
    if($resp->isSuccessful())
    {   
        list($dates,$values) = $resp->getResult();
        intShowGraph($dates,$values,$title);
    }
    else
        toLog($resp->getErrorMsg());
}

function intShowGraph(&$dates,&$values,$title)
{
    $scale=isInRequest("scale")?$_REQUEST["scale"]:"minute";
    list($dates,$values) = cropValuesForScale($scale,$dates,$values);

    $ibs_graph = new IBSBWGraph($dates, $values, $scale);
    $ibs_graph->setTitles($title, "In Rate","Out Rate","","In/Out Rate (kbytes/s)");
    $graph = $ibs_graph->createGraph();
    $graph->stroke();
}
    
