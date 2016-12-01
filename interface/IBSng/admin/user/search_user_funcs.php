<?php
require_once(IBSINC."user_search.php");
require_once(IBSINC."report.php");
require_once(IBSINC."group_face.php");
require_once(IBSINC."charge_face.php");
require_once(IBSINC."admin_face.php");
require_once(IBSINC."perm.php");
require_once("search_user/search_user_report_creator.php");
require_once("search_user/search_user_report_generator_controller.php");


function intDoSearch()
{
    if(isInRequest("show_defaults"))
        setDefaultToShowAttrs();

    $controller = new SearchUserReportGeneratorController();
    $controller->display();
}


function setDefaultToShowAttrs()
{
    $_REQUEST["Internet_Username"]="show__attrs_normal_username";
    $_REQUEST["VoIP_Username"]="show__attrs_voip_username";
    $_REQUEST["Credit"]="show__basic_credit|price";
    $_REQUEST["Group"]="show__basic_group_name";
    $_REQUEST["Owner"]="show__basic_owner_name";
}

function collectConditions ()
{
   	$report_collector = new ReportCollector();

	$report_collector->addToCondsFromCheckBoxRequest("normal_charge_", "normal_charge");
	$report_collector->addToCondsFromCheckBoxRequest("voip_charge_", "voip_charge");
	$report_collector->addToCondsFromCheckBoxRequest("group_name_", "group_name");
	$report_collector->addToCondsFromRequest(TRUE, "multi_login", "multi_login_op");

	$report_collector->addToCondsFromRequest(TRUE, "normal_username", "normal_username_op");
	$report_collector->addToCondsFromRequest(TRUE, "no_normal_username");

	$report_collector->addToCondsFromRequest(TRUE, "voip_username", "voip_username_op");
	$report_collector->addToCondsFromRequest(TRUE, "no_voip_username");

	$report_collector->addToCondsFromRequest(TRUE, "caller_id", "caller_id_op");
	$report_collector->addToCondsFromCheckBoxRequest("owner_name_", "owner_name");
	$report_collector->addToCondsFromRequest(TRUE, "normal_username", "normal_username_op");

	$report_collector->addToCondsFromRequest(TRUE, "rel_exp_date", "rel_exp_date_unit", "rel_exp_date_op");
	$report_collector->addToCondsFromRequest(TRUE, "rel_exp_value", "rel_exp_value_unit", "rel_exp_value_op");
	$report_collector->addToCondsFromRequest(TRUE, "first_login", "first_login_unit", "first_login_op");

	$report_collector->addToCondsFromRequest(TRUE, "abs_exp_date", "abs_exp_date_unit", "abs_exp_date_op");

	$report_collector->addToCondsFromRequest(TRUE, "credit", "credit_op");

	$report_collector->addToCondsFromRequest(TRUE, "lock");
	$report_collector->addToCondsFromRequest(TRUE, "lock_reason", "lock_reason_op");
	$report_collector->addToCondsFromRequest(TRUE, "fast_mode");
		

	$report_collector->addToCondsFromRequest(TRUE, "save_bw_usage");

	$report_collector->addToCondsFromRequest(TRUE, "ippool");
	$report_collector->addToCondsFromRequest(TRUE, "assign_ip", "assign_ip_op");

	$report_collector->addToCondsFromRequest(TRUE, "persistent_lan_mac");
	$report_collector->addToCondsFromRequest(TRUE, "persistent_lan_ip");
	$report_collector->addToCondsFromRequest(TRUE, "persistent_lan_ras_ip");

	$report_collector->addToCondsFromRequest(TRUE, "comment", "comment_op");
	$report_collector->addToCondsFromRequest(TRUE, "name", "name_op");
	$report_collector->addToCondsFromRequest(TRUE, "phone", "phone_op");

	$report_collector->addToCondsFromRequest(TRUE, "email_address", "email_address_op");

	$report_collector->addToCondsFromRequest(TRUE, "limit_mac", "limit_mac_op");
	$report_collector->addToCondsFromRequest(TRUE, "limit_station_ip", "limit_station_ip_op");

	$report_collector->addToCondsFromRequest(TRUE, "view_options");

	if (isInRequest("user_id_op"))
		$report_collector->addToCondsFromRequest(TRUE, "user_id", "user_id_op");
	else
	{
		$report_collector->addToCondsFromRequest(TRUE, "user_id");
		$report_collector->addToConds("user_id_op", "=");
	}

	return $report_collector->getConds();
}

?>