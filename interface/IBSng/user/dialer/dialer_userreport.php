<?php
require_once("../../inc/init.php");
require_once(IBSINC."dialer.php");
require_once(IBSINC."report.php");

needDialerAuth();
intShowUserReport();

function intShowUserReport()
{
    $count=isInRequest("count")?$_REQUEST["count"]:5;
    $req=new GetConnections(array(),0,5,"login_time",TRUE);
    $resp=$req->sendAndRecv();
    if(!$resp->isSuccessful())
    {
        $err=$resp->getError();
        print answerDialer(FALSE,"",$err->getErrorMsg());
    }
    else
    {
        $answer=intConvReportToXML($resp->getResult());
        print answerDialer(TRUE,$answer);
    }
    
}

function intConvReportToXML($logs)
{
    $answer="";
    $i=1;
    foreach($logs["report"] as $log)
    {
        $answer.="<connection><row>{$i}</row>";

        foreach($log as $attr_name=>$attr_value)
        {
            switch($attr_name)
            {
                case "duration_seconds":
                    $attr_name="duration";
                    $attr_value=formatDuration($attr_value);
                    break;
            }
            
            if($attr_name!="details")
                $answer.="<attribute><name>{$attr_name}</name><value>{$attr_value}</value></attribute>";
        }
        $answer.="</connection>";
        $i++;
    }
    return $answer;
}

?>