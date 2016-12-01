<?php


/**
 * 
 * admin_deposit_change_logs_report_creator.php
 * 
 * */

require_once ("admin_deposit_change_logs_report_generator_controller.php");
require_once (IBSINC."generator/report_generator/report_creator.php");

class AdminDepositChangeLogsReportCreator extends ReportCreator
{
	function AdminDepositChangeLogsReportCreator()
	{
		parent :: ReportCreator();
	}

	function init()
	{
		parent :: init();

		$this->register("formula_prefixes", array ("show__"));
	}

	/**
	 * collecting conditions
	 */
	function collectConditions()
	{
		$report_collector = new ReportCollector();

		$report_collector->addToCondsIfNotEq("from_admin", "All");
		$report_collector->addToCondsIfNotEq("to_admin", "All");

		$report_collector->addToCondsFromRequest(TRUE, "change_time_from", "change_time_from_unit");
		$report_collector->addToCondsFromRequest(TRUE, "change_time_to", "change_time_to_unit");

		$report_collector->addToCondsFromRequest(TRUE, "order_by");
		$report_collector->addToCondsFromRequest(TRUE, "rpp");
		$report_collector->addToCondsFromRequest(TRUE, "view_options");
		$report_collector->addToCondsFromRequest(TRUE, "desc");

		$report_collector->addToCondsFromRequest(TRUE, "show_total_deposit_change");
		
		return $report_collector->getConds();
	}

	function getRequest ($conds, $from, $to, $order_by, $desc)
	{
	    return new GetAdminDepositChangeLogs($conds, $from, $to, $order_by, $desc);
	}

	function getFieldValue(& $row_report, $attribute_name)
	{
	    $attribute_name = str_replace("show__", "", $attribute_name);
	    return $row_report[$attribute_name];
	}

	function getUsefulInformation(& $report) {
		return array ("deposit_change" => $report["deposit_change"]);
	}
}
?>