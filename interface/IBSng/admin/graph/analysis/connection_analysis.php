<?php

require_once("../../../inc/init.php");
require_once("../../report/connections_funcs.php");
require_once(IBSINC."report.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();

intShowConnectionAnalysis($smarty);

function intShowConnectionAnalysis(&$smarty)
{
    intAssignConnectionAnalysisVars($smarty);
    $smarty->display("admin/graph/connection_analysis.tpl");
}

function intAssignConnectionAnalysisVars(&$smarty)
{
    $smarty->assign("analysis_types",array("durations"=>"Durations",
                                      "group_usages"=>"Group Usages",
                                      "ras_usages"=>"Ras Usages",
                                      "admin_usages"=>"Admin Usages",
                                      "voip_dc_causes"=>"VoIP DC Causes",
                                      "successful_counts"=>"Success/Failure connections"));
    $smarty->assign("analysis_type_default",requestVal("analysis_type","durations"));
}
?>