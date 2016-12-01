<?php
require_once("../../../inc/init.php");
require_once(IBSINC."report.php");
require_once(IBSINC."graph.php");
require_once("../../report/connections_funcs.php");


needAuthType(ADMIN_AUTH_TYPE);
if(isInRequest("analysis_type") and in_array($_REQUEST["analysis_type"],array("durations","group_usages","admin_usages","ras_usages","voip_dc_causes","successful_counts")))
{
    require_once($_REQUEST["analysis_type"].".php");
    intGraph();
}

function intGraph()
{
    $data = queryData(collectConditions());
    intShowGraph($data);
}

function connectionQueryData($conds,$req_class_name)
{
    eval("\$req=new {$req_class_name}(\$conds);");
    $resp = $req->sendAndRecv();
    if($resp->isSuccessful())
        return $resp->getResult();
    else
    {
        toLog($resp->getErrorMsg());
        exit();
    }
    
}

function connectionDurationShowGraph(&$durations,$title)
{//duration should be array in format [[legend,duration_seconds],..]
    $datas=array();
    $legends=array();
    $labels=array();
    
    foreach($durations as $duration)
    {
        $datas[]=$duration[1];
        $legends[]="{$duration[0]} (".formatDuration($duration[1]).")"; 
        $labels[]="%.1f%% ({$duration[0]})";
    }
    $ibs_graph = new IBSPieGraph($title,$legends,$labels,$datas);
    $graph = $ibs_graph->createGraph();
    $graph->stroke();
}
