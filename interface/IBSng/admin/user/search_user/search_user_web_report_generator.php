<?php
require_once (IBSINC . "init.php");
require_once (IBSINC . "report.php");
require_once (IBSINC . "group_face.php");

require_once (IBSINC . "generator/report_generator/report_creator.php");
require_once (IBSINC . "generator/report_generator/web_report_generator.php");

/**
 *
 * */

class SearchUserWebReportGenerator extends WebReportGenerator {
    function SearchUserWebReportGenerator() {
        parent :: WebReportGenerator();
    }

    function init() {
        parent :: init();
        $this->registerVar("smarty_file_name", "admin/user/search_user.tpl");
    }

    function dispose() {
        $this->setOrderBys();
        $this->showUserSearchSetVars();

        parent :: dispose();
    }

    /**
     * assign group_names to smarty
     * 
     * */
    function assignGroupNames() {
        $this->controller->smarty->assign_by_ref("group_names", getGroupNames($this->controller->smarty));
    }

    /**
     * assign admin_names to smarty
     * */
    function assignAdminNames() {
        $this->controller->smarty->assign_by_ref("admin_names", getAdminNames($this->controller->smarty));
    }

    /**
     * assigning Internet and VoIP charges to Smarty 
     * */
    function assignChargeNames() {
        intSetChargeNames($this->controller->smarty, "Internet", "internet_charges");
        intSetChargeNames($this->controller->smarty, "VoIP", "voip_charges");
    }

    /**
     * assign can_change to Smarty
     * */
    function assignCanChange() {
        $this->controller->smarty->assign("can_change", hasPerm("CHANGE USER ATTRIBUTES") or amIGod());
    }

    function showUserSearchSetVars() {
        $this->assignGroupNames();
        $this->assignAdminNames();
        $this->assignChargeNames();
        $this->assignCanChange();
        $this->controller->smarty->assign("user_search", TRUE);

        if (!$this->controller->smarty->is_assigned("show_results"))
            $this->controller->smarty->assign("show_results", FALSE);
    }

    function setOrderBys() {
        $this->controller->smarty->assign("order_by_options", array (
            "user_id" => "User ID",
            "normal_username" => "Normal Username",
            "voip_username" => "VoIP Username",
            "creation_date" => "Creation Date",
            "owner_id" => "Owner ID",
            "group_id" => "Group ID",
            "credit" => "Credit",
            "first_login" => "First Login"
        ));
        $this->controller->smarty->assign("order_by_default", requestVal("order_by", "login_time"));
    }
}
?>