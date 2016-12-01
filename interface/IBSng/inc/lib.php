<?php
require_once("attr_lib.php");

function getClientIPAddress()
{/* return client ip address */
    return $_SERVER["REMOTE_ADDR"];
}

function redirect($url)
{/* redirect user to $url
    NOTE: this must be done before sending headers
 */
    header("Status: 302 moved");
    header("Location: {$url}");
    exit();
}

function isInRequest()
{/* This function has variable length arguments
    It checks if all of arguments is available in REQUEST, if so, return TRUE
    else return FALSE
*/
    $arg_list=func_get_args();
    foreach($arg_list as $arg)
        if(!isset($_REQUEST[$arg]))
            return FALSE;
    return TRUE;
    
}

function requestVal($key,$default="")
{/* return value of $key in request, if it's not available in request return $default 
 */
    if (isInRequest($key))
        return $_REQUEST[$key];
    else
        return $default;

}

function requestValWithDefaultArr($key,$default_arr,$default="")
{/*
    return value of $key in request, if it's not available in request, it will check $default_arr and return
    if it has key $key, if not, return $default
*/
    if (isInRequest($key))
        return $_REQUEST[$key];
    else if (isset($default_arr[$key]))
        return $default_arr[$key];
    else
        return $default;
    
}

function str_trim($str,$max_size)
{ /*trim $str to $max_size trying to end trimmed string with a complete word 
    Also put ... after str, if it were trimmed    
  */
  if ($max_size>=strlen($str))
    return $str;

  preg_match("/^(.{".$max_size."}[^\s\t\n]{0,100}).*/s",$str,$matches);

  return $matches[1]." ...";
}

function checkPasswordMatch($password1,$password2)
{
    if($password1!=$password2)
        return array(FALSE,new Error("PASSWORDS_NOT_MATCH|Passwords don't match"));
    else
        return array(TRUE,"");
}

function checkBoxValue($name,$default="",$if_not_exists="")
{
/*
    return value for a check box, return string is "" (empty string) or "selected" that can be 
    put into input box
    $name(string): name of check box in request
    $default(string): default value, if check box is not in request, default value is returned
    $if_not_exists(string): if this parameter isn't an empty string, it will checked against the request
        and return "checked" if it isn't in request. This is useful when you want a check box , to be checked
        by default when page is first showed, and relay on $name and $default afterwards

*/
    if(array_key_exists($name,$_REQUEST))
        return "checked";
    if($if_not_exists!=="")
        if(array_key_exists($if_not_exists,$_REQUEST))
            return "checked";
        else 
            return "";
    return $default;
}

function radioBoxValue($name,$value,$default_checked=FALSE)
{
    if(isInRequest($name))
    {
        if($_REQUEST[$name] == $value)
            return "checked";
        else
            return "";
    }
    else
    {
        if($default_checked)
            return "checked";
        else
            return "";
    }
}

function escapeIP($ip)
{/*
    escape ip address so it can be used in form names
*/
    return preg_replace("/[.]/","!",$ip);
}

function unEscapeIP($ip)
{/*
    unEscape ip that is used in form names
*/
    return preg_replace("/\!/",".",$ip);
}


function getTRColor($swap=FALSE,$var_name="tr_last_color")
{/*
    get TR color, Used in smarty plugins
    TR colors are either "light" or "dark"

    $swap tells if color needs to be swapped and we need a new color, normally this
    is done for new TR

    $var_name tells what should be the color state variable name
*/
    if(!isset($GLOBALS[$var_name]))
        $GLOBALS[$var_name]="light";
    else if($swap)
    {
        if($GLOBALS[$var_name]=="light")
            $GLOBALS[$var_name]="dark";
        else
            $GLOBALS[$var_name]="light";
    }
    return $GLOBALS[$var_name];
}

function convertRequestToUrl($ignore_list=array(),$post_style=FALSE)
{/*
    convert request key/values to url parameters.
    keys that are in $ignore_list array are ignored
    post_style(boolean): create form hidden inputs instead of get arguments
*/
    $names=array();
    $vals=array();
    foreach($_REQUEST as $key=>$value)
    {
        if(in_array($key,$ignore_list))
            continue;

        if(is_array($value))
            foreach($value as $x)
            {
                $names[]="{$key}[]";
                $values[]=$x;
            }
        else
        {
            $names[]=$key;
            $vals[]=$value;
        }
    }
    if($post_style)
    {
        $ret = "";
        foreach($names as $index=>$name)
            $ret .= "<input type=hidden name=\"{$name}\" value=\"{$vals[$index]}\">";
        return $ret;
    }
    else
    {
        $ret = array();
        foreach($names as $index=>$name)
            $ret[] = urlencode("{$name}")."=".urlencode("{$vals[$index]}");
        return join("&",$ret);
    }
}

function price($string, $precision=2)
{/*
            put , between each 3 digits, take care of $precision digits of floating point
*/
        $price=(float)$string;
        $sign=$price<0?-1:1;
        $price*=$sign;
        if($precision)
        {
            $int_price=floor($price);
            $float_part=round(($price-$int_price)*pow(10,$precision));
        }
        else
        {
            $int_price=round($price);
            $float_part=0;
        }
        
        $int_part="{$int_price}";
        $str="";
        while(strlen($int_part)>3)
        {
            $part=substr($int_part,strlen($int_part)-3,3);
            $int_part=substr($int_part,0,strlen($int_part)-3);
            $str=",{$part}{$str}";
        }
        $str="{$int_part}{$str}";
        if($float_part>0)
            $str.=".{$float_part}";
        if($sign==-1)
            $str="-{$str}";
        return $str;
}

function removeCR($str)
{/* remove Carriage Return("\r") from str and return it
    \r is converted to \n by python xmlrpc */
    return str_replace("\r","",$str);
}


function leftPadZero($str,$len)
{ /* zero left pad $str to $len */
    $str="{$str}";
    while (strlen($str)<$len)
        $str="0".$str;
    return $str;
}

function durationToSeconds($duration)
{/* Convert a string from duration format (x:x:x or x:x or x) to number of seconds) */
    $sp = explode(":",$duration);
    
    $seconds = 0;
    $factor = 3600;
    foreach($sp as $x)
    {
        $seconds += (int)$x * $factor;
        $factor /= 60;
        if($factor < 1)
            break;
    }
    return $seconds;
}

function formatDuration($seconds)
{
    if(!is_numeric($seconds))
        return $seconds;
    $seconds=(int)$seconds;
    $hours=(int)($seconds/3600);
    if($hours<10)
        $hours="0{$hours}";
    $rest=$seconds%3600;
    $mins=(int)($rest/60);
    if($mins<10)
        $mins="0{$mins}";
    $secs=$rest%60;
    if($secs<10)
        $secs="0{$secs}";

    return "{$hours}:{$mins}:{$secs}";
}

/////////////////////////////// Date Type Handling
function getDateType()
{/*return date_type, based on request,session or system wide default*/
    if(isInRequest("date_type"))
        return $_REQUEST["date_type"];
    if (sessionIsSet("date_type"))
        return $_SESSION["date_type"];
    else
        return DATE_TYPE;
}

function setSessionDateType($date_type)
{
    $_SESSION["date_type"]=$date_type;
}


?>