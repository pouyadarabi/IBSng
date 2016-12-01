<?php

require_once("../../inc/init.php");
require_once(IBSINC."report.php");
require_once(IBSINC."xml.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("last_log_time"))
    intPrintLogBuffer($_REQUEST["last_log_time"]);
else
{
    $smarty=new IBSSmarty();
    intShowRealTimeLogConsole($smarty);
}

function intShowRealTimeLogConsole(&$smarty)
{
    $smarty->assign("hide_menu",TRUE);
    $smarty->display("admin/report/realtime_log_console.tpl");
}

function intPrintLogBuffer($last_log_time)
{
    $req=new GetConsoleBuffer();
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $buffer=$resp->getResult();
    else
    {
        print xmlAnswer("LOG_CONSOLE", FALSE, "", $resp->getErrorMsg());
        return;
    }
    
    $last_log_time = (float)$last_log_time;
    $content_xml = "";
    
    foreach($buffer as $log_arr)
    {
        if($log_arr[0] > $last_log_time)
        {
            $content_xml .= "<LOG><e>{$log_arr[0]}</e><u>{$log_arr[2]}</u><df>{$log_arr[1]}</df><a>{$log_arr[3]}</a><avpairs>";

            foreach($log_arr[4] as $key=>$avpair)
                $content_xml .= "<av{$key}><n>{$avpair[0]}</n><v>{$avpair[1]}</v></av{$key}>";

            $content_xml .= "</avpairs></LOG>";
        }
    }

    print xmlAnswer("LOG_CONSOLE", TRUE, "<REPORT>{$content_xml}</REPORT>", "");
}

?>