<?php
error_reporting(E_ALL);//should be E_NONE
ini_set("display_errors",1);
ini_set("track_errors",1);
$old_error_handler = set_error_handler("errorHandler");

function errorHandler ($errno, $errstr, $errfile, $errline) {
    if($errno!=2048) //deprecated warnings
        toLog("errno: {$errno} str: {$errstr} on file: {$errfile} line :{$errline}");
}

function toLog($msg)
{
    if(!array_key_exists("log_handler",$GLOBALS))
    {
        $fh=fopen("/var/log/IBSng/ibs_interface.log","a+");
        if(!$fh)
            return;
        $GLOBALS["log_handler"]=$fh;
    }
    else
    {
        $fh=$GLOBALS["log_handler"];
    }
    $timeArr=localtime(time(),1);
    $timeStr="{$timeArr["tm_year"]}/{$timeArr["tm_mon"]}/{$timeArr["tm_mday"]} {$timeArr["tm_hour"]}:{$timeArr["tm_min"]}";
    $phperr=isset($php_errormsg)?$php_errormsg:"";
    fwrite($fh,"{$timeStr} {$msg} {$phperr}\n");
    return;

}

?>
