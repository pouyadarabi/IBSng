<?php

require_once (IBSINC."generator/report_generator/report_generator_controller.php");
require_once ("user_connection_logs_web_report_generator.php");
require_once ("user_connection_logs_report_creator.php");
require_once (IBSINC."../admin/report/connection_logs/connection_logs_report_generator_controller.php");

class UserConnectionLogsReportGeneratorController extends ConnectionLogsReportGeneratorController
{
	function UserConnectionLogsReportGeneratorController()
	{
		parent :: ConnectionLogsReportGeneratorController();

		$this->total_rows = 0;
		$this->total_credit = 0;
		$this->total_duration = 0;
	}

	function extractVarsFromResults (& $results)
	{
		$this->total_rows = $results["total_rows"];
		$this->total_credit = $results["total_credit"];
		$this->total_duration = $results["total_duration"];
	}

	function getCreator ()
	{
	    return new UserConnectionLogsReportCreator ();
	}


	function init()
	{
		parent :: init();
		$this->registerGenerator("WEB", "createUserWebGenerator");
	}

	/**
	 * get report selectors
	 * @return array selectors
	 * */
	function getReportSelectors() {
		return array_merge(array (
			"User ID" => "show__user_id|createLinkConnectionLogsUserID"
		), parent :: getReportSelectors());
	}

}

/**
 * get geneartor for web
 * */
function createUserWebGenerator()
{
	return new UserConnectionLogsWebReportGenerator();
}
