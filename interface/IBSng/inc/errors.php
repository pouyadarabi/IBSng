<?php

$ERRORS=array("INVALID_ERROR"=>"Invalid/Unknown error",
              "ACCESS_DENIED"=>"Access Denied",
              "INVALID_INPUT"=>"Invalid Input",
              "INCOMPLETE_REQUEST"=>"INCOMPLETE REQUEST"
            );




class Error
{ /* This Class is for errors reported from core or interface.
     Normally errors should consist of lines of ( keys and  messages), formated in a string like "key|msg"
     key shows what is error about and msg is the error message for this situation

  */
    function Error($err_str)
    {
        $this->raw_err_str=$err_str;
        $this->err_msgs=array();
        $this->err_keys=array();
        $this->__splitErrorLines();
    
    }

    function __splitErrorLines()
    {
        $err_lines=split("\n",$this->raw_err_str);
        foreach($err_lines as $line)
            $this->__splitError($line);
    }

    function __splitError($err_str)
    {
        $err_sp=split("\|",$err_str,2);
        if(sizeof($err_sp)==2)
        {
            $this->err_msgs[]=$err_sp[1];
            $this->err_keys[]=$err_sp[0];
        }    
        else
        {
            $this->err_msgs[]=$err_str;
            $this->err_keys[]="";
        }
    }

    function getErrorKeys()
    {/*
        Return an array of error keys
     */

        return $this->err_keys;
    }

    function getErrorMsgs()
    {/*
        Return array of error msgs
        useful for set_page_error method of smarty
     */
        return $this->err_msgs;
    }

    function getErrorMsg()
    {/* 
        Return an string of all error messages concatanated
     */
        $msgs="";
        foreach ($this->err_msgs as $msg)
            $msgs.=$msg;
        return $msgs;
    }

}

function error($error_key)
{/* return complete error message of $error_key */
    global $ERRORS;
    if (isset($ERRORS[$error_key]))
        return new Error($error_key."|".$ERRORS[$error_key]);
    else
        return new Error($ERRORS["INVALID_ERROR"]);
}



?>