<?php

/**
 * 
 * connection_logs_report_creator.php
 * 
 * */

require_once (IBSINC . "generator/report_generator/report_creator.php");
require_once ("connection_logs_report_generator_controller.php");

class ConnectionLogsReportCreator extends ReportCreator {
	function ConnectionLogsReportCreator() {
		parent :: ReportCreator();
	}

	function init() {
		parent :: init();
		$this->register("formula_prefixes", array (
			"show__details_",
			"show__"
		));
	}

	function getRequest ($conds, $from, $to, $order_by, $desc)
	{
	    return new GetConnections ($conds, $from, $to, $order_by, $desc);
	}

	function collectConditions()
	{
		return collectConditions();
	}
		
	/**
	 * get value of $attribute_name in $row_report
	 * @param mixed $row_report
	 * @param string $field_name_index
	 * */
	function getFieldValue($row_report, $attribute_name) {
		$ret = "-";
		if (ereg("^show__details_.*", $attribute_name)) {
			if ($attribute_name == "show__details_any_username")
				$attribute_names = array (
					"username",
					"voip_username"
				);
			else
				$attribute_names = array (
					str_replace("show__details_",
					"",
					$attribute_name
				));

			foreach ($row_report["details"] as $details_index => $details_attr_name) {
				if (in_array($details_attr_name[0], $attribute_names)) {
					$ret = $details_attr_name[1];
					break;
				}
			}
		} else {
			if (ereg("^show__.*", $attribute_name)) {
				$attribute_name = str_replace("show__", "", $attribute_name);
				if (isset ($row_report[$attribute_name]))
					$ret = $row_report[$attribute_name];
			}
		}
		return $ret;
	}

	/**
	 * get useful information
	 * */
	function getUsefulInformation($report) {
		return array (
			"connection_log_id" => $report["connection_log_id"],
			"details" => $report["details"]
		);
	}

}
?>