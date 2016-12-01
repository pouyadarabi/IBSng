<?php

require_once("../../inc/init.php");
require_once(IBSINC."report.php");
require_once(IBSINC."xml.php");


needAuthType(ADMIN_AUTH_TYPE);

$req=new GetOnlineUsers($_REQUEST["internet_order_by"],
                        $_REQUEST["internet_desc"]=="true",
                        $_REQUEST["voip_order_by"],
                        $_REQUEST["voip_desc"]=="true", 
                        intGetConditions());
                        
$resp=$req->sendAndRecv();
if($resp->isSuccessful())
{
    list($internet_onlines,$voip_onlines)=$resp->getResult();
    

    $internet_xml="<internet_onlines>".convAllDicsToXML($internet_onlines,"row")."</internet_onlines>";

//    $internet_xml="<internet_onlines>";
//    for($i=0;$i<100;$i++)
//      $internet_xml.=convAllDicsToXML($internet_onlines,"row");
//    $internet_xml.="</internet_onlines>";

    $voip_xml="<voip_onlines>".convAllDicsToXML($voip_onlines,"row")."</voip_onlines>";
    print xmlAnswer("onlines",TRUE, $internet_xml.$voip_xml );
}
else
    print xmlAnswer("onlines",FALSE,"",$resp->getErrorMsg());


function intGetConditions()
{
    $collector=new ReportCollector();
    $collector->addToCondsFromCheckBoxRequest("ras_","ras_ips");
    $collector->addToCondsFromCheckBoxRequest("username_","username_starts_with");
    return $collector->getConds();
}

?>