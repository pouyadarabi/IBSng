<?php

/**
 * 
 * admin_deposit_change_logs_report_creator.php
 * 
 * */

require_once ("credit_changes_report_generator_controller.php");
require_once (IBSINC."generator/report_generator/report_creator.php");

class CreditChangeReportCreator extends ReportCreator
{
	function CreditChangeReportCreator()
	{
		parent :: ReportCreator();
	}

	/**
	 * collecting conditions
	 */
	function collectConditions()
	{
	    $collector=new ReportCollector();

	    $collector->addToCondsFromRequest(TRUE,"user_ids");
	    $collector->addToCondsIfNotEq("action","All");
	    $collector->addToCondsIfNotEq("admin","All");
	        
	    $collector->addToCondsFromRequest(TRUE,"change_time_from","change_time_from_unit");
	    $collector->addToCondsFromRequest(TRUE,"change_time_to","change_time_to_unit");
	
	    $collector->addToCondsFromRequest(TRUE,"per_user_credit","per_user_credit_op");
	
	    $collector->addToCondsFromRequest(TRUE,"admin_credit","admin_credit_op");
	
	    $collector->addToCondsFromRequest(FALSE,"show_total_per_user_credit");
	    $collector->addToCondsFromRequest(FALSE,"show_total_admin_credit");
	
	    $collector->addToCondsFromRequest(TRUE,"remote_addr");
	
	    return $collector->getConds();  
	}

	function getRequest (& $conds, $from, $to, $order_by, $desc)
	{
		return new GetCreditChanges($conds, $from, $to, $order_by, $desc);
	}

	function getFieldValue(& $row_report, $attribute_name)
	{
		$attribute_name = str_replace("show__", "", $attribute_name);

		if ($attribute_name == "user_ids")
			return join($row_report[$attribute_name], ", ");

		return $row_report[$attribute_name];
	}

	function getUsefulInformation(& $report)
	{
		return array ( "per_user_credit" => $report["per_user_credit"],
					   "admin_credit" => $report["admin_credit"],
					   "credit_change_id" => $report["credit_change_id"],
					   "comment" => $report["comment"],
					   "remote_addr" => $report["remote_addr"],
					   "user_ids" => $report["user_ids"]);
	}
}
?>