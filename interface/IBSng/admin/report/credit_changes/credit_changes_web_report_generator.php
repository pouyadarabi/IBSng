<?php
require_once (IBSINC . "init.php");
require_once (IBSINC . "report.php");

require_once (IBSINC . "generator/report_generator/web_report_generator.php");

class CreditChangeWebReportGenerator extends WebReportGenerator {
    function CreditChangeWebReportGenerator() {
        parent :: WebReportGenerator();
    }

    function init() {
        parent :: init();
        $this->registerVar("smarty_file_name", "admin/report/credit_change/credit_change.tpl");
    }

    function dispose() {
        $this->setOrderBys ();
        $this->setActions ();
        $this->assignTotals ();

        parent :: dispose();
    }

	function assignTotals() 
	{
		$this->controller->smarty->assign("total_rows", $this->controller->total_rows);
		$this->controller->smarty->assign("total_admin_credit", $this->controller->total_admin_credit);
		$this->controller->smarty->assign("total_per_user_credit", $this->controller->total_per_user_credit); 
	}

    function setOrderBys() {
		$this->controller->smarty->assign("order_bys",array("change_time"=>"Change Time",
						                                      "per_user_credit"=>"User Credit",
						                                      "admin_credit"=>"Admin Credit"));

		$this->controller->smarty->assign("order_by_default",requestVal("order_by","change_time"));
    }

	function setActions ()
	{
		$this->controller->smarty->assign("actions", array( "ADD_USER"=>"Add User",
										  "CHANGE_CREDIT"=>"Change Credit",
										  "DEL_USER"=>"Delete User",
										  "All"=>"All"));

		$this->controller->smarty->assign("actions_default",requestVal("action","All"));	    
	}

    function createReportBodyTable()
    {
        $ret  = $this->getListTd("counter");

        $ret .= $this->getMathIncrementEquationFromRow("page_total_per_user_credit", "other.per_user_credit");
        $ret .= $this->getMathIncrementEquationFromRow("page_total_admin_credit", "other.admin_credit");

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