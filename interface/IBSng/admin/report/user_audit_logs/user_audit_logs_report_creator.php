<?php

/**
 * 
 * admin_deposit_change_logs_report_creator.php
 * 
 * */

require_once ("user_audit_logs_report_generator_controller.php");
require_once (IBSINC."generator/report_generator/report_creator.php");

require_once (IBSINC."../admin/report/connections_funcs.php");

class UserAuditLogsReportCreator extends ReportCreator
{
	function UserAuditLogsReportCreator()
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
	    $collector->addToCondsFromRequest(TRUE,"attr_names");
	
	    $collector->addToCondsIfNotEq(TRUE,"group_name");
	    $collector->addToCondsIfNotEq("admin","All");
	        
	    $collector->addToCondsFromRequest(TRUE,"change_time_from","change_time_from_unit");
	    $collector->addToCondsFromRequest(TRUE,"change_time_to","change_time_to_unit");

	    return $collector->getConds();    
	}

	function getRequest ($conds, $from, $to, $order_by, $desc)
	{
		return new GetUserAuditLogs($conds, $from, $to, $order_by, $desc);
	}

	function getFieldValue($row_report, $attribute_name)
	{
	    $attribute_name = str_replace("show__", "", $attribute_name);
	    $ret = "";
	    $is_user = $row_report["is_user"] == "t";
	    
	    if ($attribute_name == "user_group_type")
	    	$ret = $is_user ? "User" : "Group";

	    else if ($attribute_name == "name")
	    {
	    	$ret = $row_report["is_user"] == "t" ?
	    					$row_report["username"] :
	    					$row_report["group_name"];

	    	if ($this->controller->getViewOuputSelectedName() == "WEB")
	    		if ($is_user)
	    		{
	    			require_once($this->controller->smarty->_get_plugin_filepath('modifier', 'formatUserRepr'));
	    			$user_repr = smarty_modifier_formatUserRepr($ret);
	    			$ret = linkUserIDToUserInfo($row_report['object_id'], $user_repr);
	    		}
	    		else
	    			$ret = linkGroupNameToGroupInfo($ret);
	    }
	    else
	    	$ret = $row_report[$attribute_name]; 

	    return $ret;
	}
}
?>