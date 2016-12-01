<?php
require_once (IBSINC."init.php");
require_once (IBSINC."report.php");

require_once (IBSINC."generator/report_generator/web_report_generator.php");

/**
 *
 * */

class ConnectionLogsWebReportGenerator extends WebReportGenerator
{
	function ConnectionLogsWebReportGenerator()
	{
		parent :: WebReportGenerator();
	}

	function init()
	{
		parent :: init();
		$this->registerVar("smarty_file_name", "admin/report/connections.tpl");
	}

	function dispose()
	{
		$this->setTotalFields();
		$this->setOrderBys();
		$this->setOutputSize();
 		parent :: dispose();
	}

	function setTotalFields()
	{
		$this->controller->smarty->assign("total_rows", $this->controller->total_rows);
		$this->controller->smarty->assign("total_credit", $this->controller->total_credit);
		$this->controller->smarty->assign("total_duration", $this->controller->total_duration);
		$this->controller->smarty->assign("total_in_bytes", $this->controller->total_in_bytes);
		$this->controller->smarty->assign("total_out_bytes", $this->controller->total_out_bytes);
	}

	function setOrderBys()
	{
		$this->controller->smarty->assign("order_bys", array ("user_id" => "User ID", "credit_used" => "Credit Used", "login_time" => "Login Time", "logout_time" => "Logout Time", "successful" => "Succesful", "service" => "Service", "ras_id" => "Ras ID"));
		$this->controller->smarty->assign("order_by_default", requestVal("order_by", "login_time"));
	}

	function setOutputSize()
	{
		$this->controller->smarty->assign("size", count($this->controller->getReportSelectors()));
	}

    function createReportBodyTable()
    {
        $ret = $this->getListTd("counter");
        $ret .= parent::createReportBodyTable();

        $ret .= $this->getMathIncrementEquation("page_total_duration", "duration_seconds");
        $ret .= $this->getMathIncrementEquation("page_total_credit", "credit_used");

        return $ret;
    }

    function createReportHeaderTable()
    {
        $ret = $this->getFieldForHeaderTpl("Row");
        $ret .= parent::createReportHeaderTable();
        return $ret;
    }
}

?>