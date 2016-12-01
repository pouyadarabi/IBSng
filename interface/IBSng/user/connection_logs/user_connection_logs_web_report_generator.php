<?php
require_once (IBSINC . "init.php");
require_once (IBSINC . "report.php");

require_once (IBSINC . "generator/report_generator/web_report_generator.php");

/**
 *
 * */

class UserConnectionLogsWebReportGenerator extends WebReportGenerator
{
	function UserConnectionLogsWebReportGenerator()
	{
		parent :: WebReportGenerator();
	}

	function init()
	{
		parent :: init();
		$this->registerVar("smarty_file_name", "user/" . getLang() . "/connection_log.tpl");
	}

	function intAssignVars()
	{
		$this->controller->smarty->assign("services_default", requestVal("service", "All"));
		$this->controller->smarty->assign("successful_default", requestVal("successful", "All"));
		$this->controller->smarty->assign("size", count($this->controller->getReportSelectors()));

		$this->controller->smarty->assign("services", array (
			"internet",
			"voip",
			"All"
		));
		$this->controller->smarty->assign("successful_options", array (
			"Yes",
			"No",
			"All"
		));

		if (isset ($this->results)) {
			$this->total_rows = $this->results["total_rows"];
			$this->total_credit = $this->results["total_credit"];
			$this->total_duration = $this->results["total_duration"];
		}
		$this->controller->smarty->assign("total_rows", $this->controller->total_rows);
		$this->controller->smarty->assign("total_credit", $this->controller->total_credit);
		$this->controller->smarty->assign("total_duration", $this->controller->total_duration);
	}

	function dispose() {
		$this->setOrderBys();
		$this->intAssignVars();

		parent :: dispose();
	}

	function setOrderBys() {
		$this->controller->smarty->assign("order_bys", array (
			"credit_used" => "Credit Used",
			"login_time" => "Login Time",
			"logout_time" => "Logout Time",
			"successful" => "Succesful",
			"service" => "Service"
		));
		$this->controller->smarty->assign("order_by_default", requestVal("order_by", "login_time"));
	}

	function createReportBodyTable() {
		$ret  = parent :: createReportBodyTable();
		$ret .= $this->getMathIncrementEquation("page_total_duration", "duration_seconds");
		$ret .= $this->getMathIncrementEquation("page_total_credit", "credit_used");

		return $ret;
	}
}
?>