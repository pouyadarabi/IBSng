<?php
require_once (IBSINC . "init.php");
require_once (IBSINC . "report.php");

require_once (IBSINC . "generator/report_generator/web_report_generator.php");

class WebAnalyzerLogsWebReportGenerator extends WebReportGenerator {
    function WebAnalyzerLogsWebReportGenerator() {
        parent :: WebReportGenerator();
    }

    function init() {
        parent :: init();
        $this->registerVar("smarty_file_name", "admin/report/web_analyzer_logs/web_analyzer_logs.tpl");
    }

    function dispose() {
        $this->setOrderBys();
        $this->assignTotals();

        parent :: dispose();
    }

	function assignTotals() 
	{
	    $this->controller->smarty->assign("total_rows", $this->controller->total_rows); 
	    $this->controller->smarty->assign("total_count", $this->controller->total_count);
	    $this->controller->smarty->assign("total_elapsed", $this->controller->total_elapsed);
	    $this->controller->smarty->assign("total_bytes", $this->controller->total_bytes);
	    $this->controller->smarty->assign("total_miss", $this->controller->total_miss);
	    $this->controller->smarty->assign("total_hit", $this->controller->total_hit);
	}

    function setOrderBys() {
        $this->controller->smarty->assign("order_bys", array("log_id"=>"Log ID",
                                      "_date"=>"Date",
                                      "user_id"=>"User ID"));
        $this->controller->smarty->assign("order_by_default",requestVal("order_by","log_id"));
    }
    function createReportBodyTable()
    {
        $ret  = $this->getListTd("counter");
        $ret .= parent::createReportBodyTable();

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