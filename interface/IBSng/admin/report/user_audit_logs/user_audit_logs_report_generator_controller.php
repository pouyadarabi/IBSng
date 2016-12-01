<?php

require_once (IBSINC."generator/report_generator/report_generator_controller.php");
require_once ("user_audit_logs_web_report_generator.php");
require_once ("user_audit_logs_report_creator.php");

class UserAuditLogsReportGeneratorController extends ReportGeneratorController
{
	function UserAuditLogsReportGeneratorController()
	{
		parent :: ReportGeneratorController();

		$this->total_rows = 0;
	}
	
	function getCreator ()
	{
		return new UserAuditLogsReportCreator ();
	}

	function init()
	{
		parent :: init();

		$this->registerGenerator("WEB", "createUserAuditLogsWebGenerator");
		$this->output_filename = "user_audit_logs_reports";
		$this->view_default_selected_name = "WEB";
	}

	function extractVarsFromResults (& $results)
	{
		$this->total_rows = $results["total_rows"];
	}
}

/**
 * get geneartor for web
 * */
function createUserAuditLogsWebGenerator()
{
	return new UserAuditLogsWebReportGenerator();
}
