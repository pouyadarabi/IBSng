<?php
require_once (IBSINC . "init.php");
require_once (IBSINC . "report.php");
require_once (IBSINC . "group_face.php");

require_once (IBSINC . "generator/report_generator/report_creator.php");
require_once (IBSINC . "generator/report_generator/web_report_generator.php");

class AdminDepositChangeLogsWebReportGenerator extends WebReportGenerator {
    function AdminDepositChangeLogsWebReportGenerator() {
        parent :: WebReportGenerator();
    }

    function init() {
        parent :: init();
        $this->registerVar("smarty_file_name", "admin/report/admin_deposit_change_logs/admin_deposit_change_logs.tpl");
    }

    function dispose() {
        $this->setOrderBys();
        $this->assignTotals();

        parent :: dispose();
    }

	function assignTotals() 
	{
	    $this->controller->smarty->assign("total_of_rows", $this->controller->total_of_rows);
	    $this->controller->smarty->assign("total_deposit_change", $this->controller->total_deposit_change);
	}

    function setOrderBys() {
        $this->controller->smarty->assign("order_bys", array (
            "admin_id" => "From Admin",
            "to_admin_id" => "To Admin",
            "change_time" => "Change Time",
            "deposit_change" => "Deposit Change",
        ));
        $this->controller->smarty->assign("order_by_default", requestVal("order_by", "change_time"));
    }
    function createReportBodyTable()
    {
        $ret  = $this->getListTd("counter");
        $ret .= parent::createReportBodyTable();
        $ret .= $this->getMathIncrementEquationFromRow("page_total_deposit_change", "other.deposit_change");

        return $ret;
    }

    function createReportHeaderTable()
    {
        $ret  = $this->getFieldForHeaderTpl("Row");
        $ret .= parent::createReportHeaderTable();
        return $ret;
    }

}
?>