<?php
/**
 * collecting conditions
 */
function collectConditions()
{
	$collector = new ReportCollector();
	$collector->addToCondsFromRequest(TRUE, "user_ids");

	addBooleanCheckBoxCond($collector, "service_internet", "service_voip", array ("service", "internet"), array ("service", "voip"));
	addBooleanCheckBoxCond($collector, "successful_yes", "successful_no", array ("successful", "yes"), array ("successful", "no"));

	$collector->addToCondsIfNotEq("owner", "All");

	$collector->addToCondsFromRequest(TRUE, "username");
	$collector->addToCondsFromRequest(TRUE, "voip_username");

	$collector->addToCondsFromRequest(TRUE, "mac");
	$collector->addToCondsFromRequest(TRUE, "view_options");
	$collector->addToCondsFromRequest(TRUE, "caller_id");

	$collector->addToCondsFromRequest(TRUE, "remote_ip");
	$collector->addToCondsFromRequest(TRUE, "station_ip");

	$collector->addToCondsFromRequest(TRUE, "login_time_from", "login_time_from_unit");
	$collector->addToCondsFromRequest(TRUE, "login_time_to", "login_time_to_unit");

	$collector->addToCondsFromRequest(TRUE, "logout_time_from", "logout_time_from_unit");
	$collector->addToCondsFromRequest(TRUE, "logout_time_to", "logout_time_to_unit");

	$collector->addToCondsFromRequest(TRUE, "credit_used", "credit_used_op");

	$collector->addToCondsFromRequest(FALSE, "show_total_credit_used");
	$collector->addToCondsFromRequest(FALSE, "show_total_duration");
	$collector->addToCondsFromRequest(FALSE, "show_total_inouts");

	$collector->addToCondsFromCheckBoxRequest("ras_", "ras_ip");

	return $collector->getConds();
}

function addBooleanCheckBoxCond(& $collector, $key1, $key2, $val_arr1, $val_arr2)
{
	/*
	    add condition to collector if either $key1 or $key2 is available in request and NOT both of them
	    if $key1 is available content of $val_arr1 will be added to conditions
	    if $key2 is available content of $val_arr2 will be added to conditions
	*/
	if (isInRequest($key1, $key2))
		return;

	if (isInRequest($key1))
		$collector->addToConds($val_arr1[0], $val_arr1[1]);
	else
		if (isInRequest($key2))
			$collector->addToConds($val_arr2[0], $val_arr2[1]);
}
?>
