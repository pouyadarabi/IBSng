<?php

/**
 * 
 * admin_deposit_change_logs_report_creator.php
 * 
 * */

require_once ("connection_usages_report_generator_controller.php");
require_once (IBSINC."generator/report_generator/report_creator.php");

require_once (IBSINC."../admin/report/connections_funcs.php");

class ConnectionUsageReportCreator extends ReportCreator
{
	function ConnectionUsageReportCreator()
	{
		parent :: ReportCreator();
		$this->register("formula_prefixes", array (
										"show__all_",
										"show__inout_usages_",
										"show__credit_usages_",
										"show__time_usages_"));
		$this->requests = array (
						"inout_usages" =>  "GetInOutUsages",
						"credit_usages" => "GetCreditUsages",
						"time_usages" => "GetDurationUsages"
							);

		$this->row_indexes = array ("show__all_user_id" => 0, "show__all_user_name" => 1,
								"show__inout_usages_in_bytes" => 2,	"show__inout_usages_out_bytes" => 2,
								"show__credit_usages_credit_usage" => 2,
								"show__time_usages_time_usage" => 2);
		
	}

	/**
	 * collecting conditions
	 */
	function collectConditions()
	{
	    return collectConditions();
	}

	function getRequest ($conds, $from, $to, $order_by, $desc)
	{
		$report_type = $_REQUEST["report_type"];
		$klass = "";

		if (isset ($this->requests [$report_type]))
		{
		    $klass = $this->requests [$report_type];
		    eval ("\$klass = new {$klass}(\$conds, \$from, \$to);");
		}
		else
		    $this->controller->smarty->set_page_error("Invalid Report Type");

		return $klass;
	}

	function getFieldValue($row_report, $attribute_name)
	{
	    return $row_report[$this->row_indexes[$attribute_name]];
	}

	function canShowReports() {
		return isInRequest("show_reports", "report_type");
	}
}
?>