<?php
require_once("../inc/init.php");


if(isInRequest("date_type") and in_array($_REQUEST["date_type"],array("gregorian","jalali","relative")))
    setSessionDateType($_REQUEST["date_type"]);

print ucwords(getDateType());


?>