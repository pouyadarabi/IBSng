<?php

function intBWGraph($username)
{
    $data = getData(collectConds());
    list($dates, $values) = convDatas($data);
    intShowGraph($dates, $values, $username);
}

function convDatas($data)
{
    $dates = array();
    $values = array();
    $i=0;
    foreach($data as $tuple)
    {
        if($i>0 and $data[$i][0] - $data[$i-1][0] > 600)
        {
            $dates[]=$data[$i-1][0]+300;
            $values[]=array(0,0);

            $dates[]=$data[$i][0]-300;
            $values[]=array(0,0);
        
        }
        $dates[]=$tuple[0];
        $values[] = array($tuple[1], $tuple[2]);
        $i++;
    }

    return array($dates, $values);
}

function getData($conds)
{
    $req = new GetBWSnapShot($conds);
    $resp = $req->sendAndRecv();
    if($resp->isSuccessful())
    {   
        return $resp->getResult();
    }
    else
    {
        toLog($resp->getErrorMsg());
        exit();
    }
    
}

function collectConds()
{
    $collector=new ReportCollector();

    $collector->addToCondsFromRequest(TRUE,"date_from","date_from_unit");
    $collector->addToCondsFromRequest(TRUE,"date_to","date_to_unit");
    $collector->addToCondsFromRequest(TRUE,"user_id");

    return $collector->getConds();
}

function intShowGraph(&$dates,&$values, $username)
{
    
    $ibs_graph = new IBSBWGraph($dates, $values);
    $ibs_graph->setTitles("BW Graph For {$username}", "In Rate","Out Rate","","In/Out Rate (kbytes/s)");
    $graph = $ibs_graph->createGraph();
    $graph->stroke();

}
?>