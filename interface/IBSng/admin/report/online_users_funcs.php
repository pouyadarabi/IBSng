<?php

require_once("../../inc/init.php");
require_once(IBSINC."report.php");

function intGetOnlineUsers(&$smarty)
{
    $report_helper=new ReportHelper();
    $internet_order_by = $report_helper->getOrderBy();
    $internet_desc = $report_helper->getDesc();

    $report_helper->order_by_key="voip_order_by";
    $report_helper->desc_key="voip_desc";
    $report_helper->updateToRequest();

    $voip_order_by = $report_helper->getOrderBy();
    $voip_desc = $report_helper->getDesc();

    $req=new GetOnlineUsers($internet_order_by,$internet_desc,$voip_order_by,$voip_desc, array());
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        list($internet_onlines,$voip_onlines)=$resp->getResult();
    else
    {
        $resp->setErrorInSmarty($smarty);
        $internet_onlines=array();
        $voip_onlines=array();
    }
    return array($internet_onlines, $voip_onlines);
}

?>