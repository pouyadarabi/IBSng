<?php
require_once (IBSINC . "init.php");
require_once (IBSINC . "report.php");

require_once (IBSINC . "generator/report_generator/web_report_generator.php");

class UserAuditLogsWebReportGenerator extends WebReportGenerator {
    function UserAuditLogsWebReportGenerator() {
        parent :: WebReportGenerator();
    }

    function init() {
        parent :: init();
        $this->registerVar("smarty_file_name", "admin/report/user_audit_logs/user_audit_logs.tpl");
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

    function setOrderBys()
    {
	    $this->controller->smarty->assign("order_bys",array("change_time"=>"Change Time",
				                                      "object_id"=>"User ID",
				                                      "admin_id"=>"Admin ID"));
    	$this->controller->smarty->assign("order_by_default",requestVal("order_by","change_time"));        
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