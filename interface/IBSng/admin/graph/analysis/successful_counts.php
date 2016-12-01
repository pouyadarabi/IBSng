<?php
function queryData($conds)
{
    return connectionQueryData($conds,"GetSuccessfulCounts");
}

function intShowGraph(&$datas)
{
    $legends=array("Successful","Failure");
    $labels=array("%.1f%% (Successful)","%.1f%% (Failure)");
    
    $ibs_graph = new IBSPieGraph("Successful/Failure Analysis",$legends,$labels,$datas);
    $graph = $ibs_graph->createGraph();
    $graph->stroke();
}
    

