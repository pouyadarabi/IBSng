<?php

require_once (IBSINC."generator/report_generator/report_generator_controller.php");
require_once ("credit_changes_web_report_generator.php");
require_once ("credit_changes_report_creator.php");

class CreditChangeReportGeneratorController extends ReportGeneratorController
{
	function CreditChangeReportGeneratorController()
	{
		parent :: ReportGeneratorController();

		$this->total_rows = 0;
		$this->total_admin_credit = 0;
		$this->total_per_user_credit = 0;
	}
	
	function getCreator ()
	{
		return new CreditChangeReportCreator ();
	}

	function init()
	{
		parent :: init();
		$this->registerGenerator("WEB", "createCreditChangeWebGenerator");
		$this->output_filename = "credit_change_reports";
		$this->view_default_selected_name = "WEB";
	}

	function extractVarsFromResults (& $results)
	{
		$this->total_rows = $results["total_rows"];
		$this->total_admin_credit = $results["total_admin_credit"];
		$this->total_per_user_credit = $results["total_per_user_credit"];
	}
}

/**
 * get geneartor for web
 * */
function createCreditChangeWebGenerator()
{
	return new CreditChangeWebReportGenerator();
}
