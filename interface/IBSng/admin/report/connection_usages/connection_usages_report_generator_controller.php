<?php

require_once (IBSINC."generator/report_generator/report_generator_controller.php");
require_once ("connection_usages_web_report_generator.php");
require_once ("connection_usages_report_creator.php");

class ConnectionUsageReportGeneratorController extends ReportGeneratorController
{
	function ConnectionUsageReportGeneratorController()
	{
		parent :: ReportGeneratorController();

		$this->total_rows = 0;
	}
	
	function getCreator ()
	{
		return new ConnectionUsageReportCreator ();
	}

	function init()
	{
		parent :: init();

		$this->registerGenerator("WEB", "createConnectionUsageWebGenerator");
		$this->output_filename = "connection_usage_reports";
		$this->view_default_selected_name = "WEB";
	}

	function extractVarsFromResults (& $results)
	{
		$this->total_rows = $results["total_rows"];
	}
	
	function getReportSelectors()
	{
		$ret = ReportGeneratorController::getReportSelectors ("show__all");

		if (isset ($_REQUEST["report_type"]))
			$ret = array_merge($ret, ReportGeneratorController::getReportSelectors (
											"show__".$_REQUEST["report_type"]));

		return $ret;
	}
}

/**
 * get geneartor for web
 * */
function createConnectionUsageWebGenerator()
{
	return new ConnectionUsageWebReportGenerator();
}
