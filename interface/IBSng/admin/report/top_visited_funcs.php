<?php
require_once("../../inc/init.php");
require_once(IBSINC."report.php");

function intShowTopVisitedURLS(&$smarty)
{
    if(isInRequest("show"))
        intSetReport($smarty);

    $smarty->display("admin/report/top_visited.tpl");
}

function intSetReport(&$smarty)
{
    $smarty->assign("show_report",TRUE);
    list($err, $report, $total) = intGetReport();
    if(!is_null($err))
        $smarty->set_page_error($err);

    $smarty->assign("total_rows", $total);
    $smarty->assign_by_ref("report",$report);
}

function intGetReport()
{
    $conds = collectConditions();

    $report_helper = new ReportHelper();
    $req = new GetTopVisitedReport($conds,
                                  $report_helper->getFrom(),
                                  $report_helper->getTo()
                                  );

    $resp = $req->sendAndRecv();
    if($resp->isSuccessful())
    {
        list($report, $total_count) = $resp->getResult();
        $err = null;
    }
    else
    {
        $err = $resp->getErrorMsg();
        $report = array();
    }
    return array($err, $report, $total_count);
}

function collectConditions()
{ 
    $collector = new ReportCollector();

    $collector->addToCondsFromRequest(TRUE,"date_from","date_from_unit");
    $collector->addToCondsFromRequest(TRUE,"date_to","date_to_unit");
    $collector->addToCondsFromRequest(TRUE,"user_ids");

    return $collector->getConds();
}
?>