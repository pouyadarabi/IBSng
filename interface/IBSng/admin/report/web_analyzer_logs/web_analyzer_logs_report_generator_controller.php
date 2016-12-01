<?php

require_once (IBSINC."generator/report_generator/report_generator_controller.php");
require_once ("web_analyzer_logs_web_report_generator.php");
require_once ("web_analyzer_logs_report_creator.php");

class WebAnalyzerLogsReportGeneratorController extends ReportGeneratorController
{
	function WebAnalyzerLogsReportGeneratorController()
	{
		parent :: ReportGeneratorController();

		$this->total_miss = 0;
	    $this->total_rows = 0;
	    $this->total_count = 0;
	    $this->total_elapsed = 0;
	    $this->total_failure = 0;
	    $this->total_bytes = 0;
	    $this->total_hit = 0;
	    $this->total_success = 0; 
	}
	
	function getCreator ()
	{
		return new WebAnalyzerLogsReportCreator ();
	}

	function init()
	{
		parent :: init();
		$this->registerGenerator("WEB", "createWebAnalyzerLogsWebGenerator");
		$this->output_filename = "web_analyzer_logs_reports";
		$this->view_default_selected_name = "WEB";
	}

	function extractVarsFromResults (& $results)
	{
	     $this->total_miss = $results[0]["total_miss"];
	     $this->total_rows = $results[0]["total_rows"];
	     $this->total_count = $results[0]["total_count"];
	     $this->total_elapsed = $results[0]["total_elapsed"];
	     $this->total_failure = $results[0]["total_failure"];
	     $this->total_bytes = $results[0]["total_bytes"];
	     $this->total_hit = $results[0]["total_hit"];
	     $this->total_success = $results[0]["total_success"];
	}
	
	function getReportSelectors()
	{
	    $selectors = ReportGeneratorController::getReportSelectors();

		// split key of $selectors that contains " / " into more than one keys
		// and add new keys to $selectors with associated values.
		if ($this->getViewOuputSelectedName() != "WEB")
	    	foreach ($selectors as $selector => $smarty_output)
	    		if (strchr($selector, " / ")) {
	    	    	unset($selectors[$selector]);
	    	    	$keys = split(" / ", $selector);
	    	    	$values = split(",show__slash,", $smarty_output);

	    	    	for ($i = 0; $i < count($keys); $i ++)
	    	    		$selectors[$keys[$i]] = $values[$i];
	    		}

	    return $selectors;
	}
}

/**
 * get geneartor for web
 * */
function createWebAnalyzerLogsWebGenerator()
{
	return new WebAnalyzerLogsWebReportGenerator();
}
