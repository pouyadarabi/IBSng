<?php
function queryData($conds)
{
    return connectionQueryData($conds,"GetVoIPDisconnectCausesCount");
}

function intShowGraph(&$cause_codes)
{
    $datas=array();
    $legends=array();
    $labels=array();
    
    foreach($cause_codes as $cause_code)
    {
        $legends[]=$cause_code[0]; //cause code number
        $labels[]="%.1f%% ({$cause_code[0]})";
        $datas[]=$cause_code[1];
    }
    $ibs_graph = new IBSPieGraph("VoIP Cause Code Analysis",$legends,$labels,$datas);
    $graph = $ibs_graph->createGraph();
    $graph->stroke();
}
    

