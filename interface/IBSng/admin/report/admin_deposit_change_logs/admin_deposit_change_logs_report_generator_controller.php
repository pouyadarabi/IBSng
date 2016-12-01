<?php

require_once (IBSINC."generator/report_generator/report_generator_controller.php");
require_once ("admin_deposit_change_logs_web_report_generator.php");
require_once ("admin_deposit_change_logs_report_creator.php");

class AdminDepositChangeLogsReportGeneratorController extends ReportGeneratorController
{
	function AdminDepositChangeLogsReportGeneratorController()
	{
		parent :: ReportGeneratorController();
		$this->total_of_rows = 0;
		$this->total_deposit_change = 0;
	}
	
	function getCreator ()
	{
		return new AdminDepositChangeLogsReportCreator ();
	}

	function init()
	{
		parent :: init();
		$this->registerGenerator("WEB", "createAdminDepositChangeLogsWebGenerator");
		$this->output_filename = "admin_deposit_change_logs_reports";
		$this->view_default_selected_name = "WEB";
	}

	function extractVarsFromResults (& $results)
	{
		$this->total_of_rows = $results["total_rows"]; 
		$this->total_deposit_change = $results["total_deposit_change"];
	}
}

/**
 * get geneartor for web
 * */
function createAdminDepositChangeLogsWebGenerator()
{
	return new AdminDepositChangeLogsWebReportGenerator();
}
