<?php

function queryData($conds)
{
    $req = new GetDurations($conds);
    $resp = $req->sendAndRecv();
    if($resp->isSuccessful())
        return $resp->getResult();
    else
    {
        toLog($resp->getErrorMsg());
        exit();
    }
    
}

function intShowGraph(&$durations)
{
    $datas=array();
    $legends=array("Less than 1 minute","Between 1 and 5 minutes","Between 5 and 60 minutes","Between 1 and 2 hours","Between 2 and 4 hours","More than 4 hours");
    $labels=array("%.1f%% (<1min)","%.1f%% (1-5min)","%.1f%% (5-60min)","%.1f%% (1-2hours)","%.1f%% (2-4hours)","%.1f%% (>4hours)");
    
    foreach($durations as $duration)
        $datas[]=$duration[1];
    
    $ibs_graph = new IBSPieGraph("Connection Duration Analysis",$legends,$labels,$datas);
    $graph = $ibs_graph->createGraph();
    $graph->stroke();
}
    

