<?php
require_once("init.php");

$valid_languages = array("en"=>"English","fa"=>"فارسی");

function isValidLang($lang)
{/*
    return true if language is valid, false otherwise
*/
    global $valid_languages;
    return isset($valid_languages[$_REQUEST["lang"]]);
}

function setSessionLang($lang)
{ /*
    set language for current session
*/
    if(isValidLang($lang))
        $_SESSION["lang"] = $lang;
    else
        toLog("Invalid language {$lang}");
}


function getLang()
{ /*
        return currently preferred language
*/
    if(isInRequest("lang") and isValidLang($_REQUEST["lang"]))
        return $_REQUEST["lang"];
    else if (sessionIsSet("lang"))
        return $_SESSION["lang"];
    else
        return DEFAULT_LANGUAGE;
}


?>