<?php


/**
 * 
 * connection_logs_report_creator.php
 * 
 * */

require_once (IBSINC . "../admin/report/connection_logs/connection_logs_report_creator.php");
require_once ("user_connection_logs_report_generator_controller.php");

class UserConnectionLogsReportCreator extends ConnectionLogsReportCreator
{
	function UserConnectionLogsReportCreator()
	{
		parent :: ConnectionLogsReportCreator();
	}

	function collectConditions()
	{
		$collector = new ReportCollector();
		$collector->addToCondsIfNotEq("service", "All");
		$collector->addToCondsIfNotEq("successful", "All");

		$collector->addToCondsFromRequest(TRUE, "login_time_from", "login_time_from_unit");
		$collector->addToCondsFromRequest(TRUE, "login_time_to", "login_time_to_unit");

		$collector->addToCondsFromRequest(TRUE, "credit_used", "credit_used_op");
		$collector->addToCondsFromRequest(TRUE, "view_options");
		$collector->addToCondsFromRequest(FALSE, "show_total_credit_used");
		$collector->addToCondsFromRequest(FALSE, "show_total_duration");

		return $collector->getConds();
	}
}
?>