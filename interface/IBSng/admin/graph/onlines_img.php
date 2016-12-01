<?php
require_once("../../inc/init.php");
require_once(IBSINC."graph.php");
require_once(IBSINC."snapshot.php");
require_once(IBSINC."report_lib.php");


needAuthType(ADMIN_AUTH_TYPE);
intOnlineGraph();


function intOnlineGraph()
{
    $data = getData(collectConds(), getUserType());
    list($dates, $values) = convDatas($data);
    intShowGraph($dates,$values);
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
            $values[]=0;

            $dates[]=$data[$i][0]-300;
            $values[]=0;
        }
        $dates[]=$tuple[0];
        $values[]=$tuple[1];
        $i++;
    }

    return array($dates,$values);
}

function getData($conds,$type)
{
    $req = new GetOnlinesSnapShot($conds,$type);
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

function getUserType()
{
    return $_REQUEST["type"];
}

function collectConds()
{
    $collector=new ReportCollector();

    $collector->addToCondsFromRequest(TRUE,"date_from","date_from_unit");
    $collector->addToCondsFromRequest(TRUE,"date_to","date_to_unit");
    $collector->addToCondsFromCheckBoxRequest("ras_","ras_ips");

    return $collector->getConds();
}

function intShowGraph(&$dates,&$values)
{
    $ibs_graph = new IBSGraph($dates, $values);
    $ibs_graph->setTitles(ucwords(getUserType())." Online Users", "# Onlines","","# Onlines");
    $graph = $ibs_graph->createGraph(TRUE, FALSE);
    $graph->stroke();
}
    

