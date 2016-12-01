<?php

function session_init()
{
    if(!ini_get('session.auto_start'))
    {
        session_name("IBS_SESSID");
        session_start();
    }
}

function sessionRegister($sess_var_name,$value)
{
    $_SESSION[$sess_var_name]=$value;
}


function sessionGetVar($var_name)
{
    return $_SESSION[$var_name];
}

function sessionIsSet($var_name)
{
    return isset($_SESSION[$var_name]);
}

?>