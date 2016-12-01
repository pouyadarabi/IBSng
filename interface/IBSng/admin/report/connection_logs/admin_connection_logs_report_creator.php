<?php


/**
 * 
 * connection_logs_report_creator.php
 * 
 * */

require_once (IBSINC . "generator/report_generator/report_creator.php");
require_once ("admin_connection_logs_report_generator_controller.php");
require_once ("connection_logs_report_creator.php");

class AdminConnectionLogsReportCreator extends ConnectionLogsReportCreator {
	function AdminConnectionLogsReportCreator() {
		parent :: ConnectionLogsReportCreator();
	}

	function collectConditions() {
		return collectConditions();
	}
}
?>