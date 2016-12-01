<?php
require_once (IBSINC . "init.php");
require_once (IBSINC . "report.php");

require_once (IBSINC . "generator/report_generator/web_report_generator.php");

class ConnectionUsageWebReportGenerator extends WebReportGenerator {
    function ConnectionUsageWebReportGenerator() {
        parent :: WebReportGenerator();
    }

    function init() {
        parent :: init();
        $this->registerVar("smarty_file_name", "admin/report/connection_usage.tpl");
    }

    function dispose() {
        $this->setOrderBys();
        $this->assignTotals();

        parent :: dispose();
    }

	function assignTotals() 
	{
    	$this->controller->smarty->assign("total_rows", $this->controller->total_rows); 
	}

    function setOrderBys() {
        
        $this->controller->smarty->assign("report_types",array("credit_usages"=>"Credit Usages",
										 "time_usages"=>"Time Usages",
										 "inout_usages"=>"InOut Usages"
										));
		$this->controller->smarty->assign("report_type_default", requestVal("report_type"));	
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