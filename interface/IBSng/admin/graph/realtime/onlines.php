<?php
require_once("../../../inc/init.php");
require_once(IBSINC."graph.php");
require_once(IBSINC."snapshot.php");


needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("internet"))
    intInternetOnlinesGraph();
else if (isInRequest("voip"))
    intVoIPOnlinesGraph();
else
    intAllOnlinesGraph();

function intAllOnlinesGraph()
{
    intOnlinesGraph("all_onlines","All Onlines");
}

function intInternetOnlinesGraph()
{
    intOnlinesGraph("internet_onlines","Internet Onlines");
}

function intVoIPOnlinesGraph()
{
    intOnlinesGraph("voip_onlines","VoIP Onlines");
}

function intOnlinesGraph($snapshot_name,$title)
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

    $ibs_graph = new IBSGraph($dates, $values, $scale);
    $ibs_graph->setTitles($title, "# Onlines","","# Onlines");
    $graph = $ibs_graph->createGraph();
    $graph->stroke();
}
    
