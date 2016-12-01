<?php
require_once("init.php");
function largeUrlSave($request_key,$value,$max_size=1024)
{/*
    this function is used, to keep large url parameters in user sesssion, and don't pass them in url that causes some
    problems. this is done by checking if $value is more that $max_size in length, if so save $value in session
    and return an id instead of the real paramters. then on target php, we should have an largeUrlRestore call
    with same $request_key as arguement. it will transparently put necessary session data into request, so other page
    codes doesn't need to alter
*/
    if (strlen($value)>$max_size)
    {
        $id=saveInSession($request_key,$value);
        return "{$request_key}__large_id={$id}";
    }
    else
        return "{$request_key}={$value}";
}


function largeUrlRestore($request_key)
{/*
    this's second part of large url handling, that should be put in target php to restore $_REQUEST
*/
    if(!isInRequest($request_key) and isInRequest("{$request_key}__large_id"))
        $_REQUEST[$request_key]=$_SESSION["{$request_key}__values"][(int)$_REQUEST["{$request_key}__large_id"]];
}

//**********************
function saveInSession($request_key,$value)
{
    if(!isset($_SESSION["{$request_key}__id"]))
    {
        $_SESSION["{$request_key}__id"]=0;
        $_SESSION["{$request_key}__values"]=array();
    }
    $id=++$_SESSION["{$request_key}__id"];
    $_SESSION["{$request_key}__values"][$id]=$value;
    return $id;
}


?>