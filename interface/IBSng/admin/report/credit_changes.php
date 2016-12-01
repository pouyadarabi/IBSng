<?php

require_once("../../inc/init.php");
require_once(IBSINC."report.php");
require_once ("credit_changes/credit_changes_report_generator_controller.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
session_write_close();

$controller = new CreditChangeReportGeneratorController();
$controller->display();
?>