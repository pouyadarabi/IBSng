<?php

/**
 * 
 * admin_deposit_change_logs_report_creator.php
 * 
 * */

require_once ("web_analyzer_logs_report_generator_controller.php");
require_once (IBSINC."generator/report_generator/report_creator.php");

class WebAnalyzerLogsReportCreator extends ReportCreator
{
	function WebAnalyzerLogsReportCreator()
	{
		parent :: ReportCreator();
	}

	function create ()
	{
		if (isInRequest("xml"))
			$this->printXML();
		else
			ReportCreator::create();
	}

	function printXML()
	{
    	    $response_results = $this->getResonseResults();

	    $this->controller->extractVarsFromResults($response_results);
    	    list($totals, $report) = $response_results;

	    if(!$this->getRegisteredValue("error_occured"))
    	    {
        	$report_xml = convAllDicsToXML($report, "REQUEST");
        	$totals_xml = convDicToXML($totals);
        	print xmlAnswer("WEB_ANALYZER_LOG", TRUE, "<REPORT>{$report_xml}</REPORT><TOTALS>{$totals_xml}</TOTALS>", "");
    	    }
    	    else
        	print xmlAnswer("WEB_ANALYZER_LOG", FALSE, "", $this->getRegisteredValue("error_mesg"));
	}	

	/**
	 * collecting conditions
	 */
	function collectConditions()
	{
	    $collector=new ReportCollector();

    	$collector->addToCondsFromRequest(TRUE,"ip_addr");
    	$collector->addToCondsFromRequest(TRUE,"url","url_op");

    	$collector->addToCondsFromRequest(TRUE,"log_id","log_id_op");

    	$collector->addToCondsFromRequest(TRUE,"elapsed","elapsed_op");
    	$collector->addToCondsFromRequest(TRUE,"bytes","bytes_op");

	    $collector->addToCondsFromRequest(TRUE,"date_from","date_from_unit");
    	$collector->addToCondsFromRequest(TRUE,"date_to","date_to_unit");

    	$collector->addToCondsFromRequest(TRUE,"user_ids");

    	return $collector->getConds();    
	}

	function getRequest ($conds, $from, $to, $order_by, $desc)
	{
	    return new GetWebAnalyzerReport($conds, $from, $to, $order_by, $desc);
	}

	function getFieldValue($row_report, $attribute_name)
	{
	    /*
		slash Used in Miss/Hit attribute to seperate them by slash
	    */
	    $special_chars = array ("slash" => "/");
	    $attribute_name = str_replace("show__", "", $attribute_name);
	    $ret = "";

	    if (isset($row_report[$attribute_name]))
	    	$ret = $row_report[$attribute_name];

	    else if(isset ($special_chars[$attribute_name]))
	    	$ret = $special_chars[$attribute_name];

	    return $ret;
	}

	 function & getReports(& $request_results)
	 {
	     return $request_results[1];
	 }

	function getUsefulInformation($report) {
		return array ( "log_id"  => $report["log_id"],
				"_count"  => $report["_count"],
				"elapsed" => $report["elapsed"],
				"ip_addr" => $report["ip_addr"]);
	}
}
?>