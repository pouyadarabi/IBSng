<?php

checkReferrer();

/**
 * Check for Invalid Referer
*/

function checkReferrer()
{
    $auth = getAuth();
    if ($auth->getAuthType() == ADMIN_AUTH_TYPE and 
	    !isRequestComesFromThisIBSngServer() and 
	    !defined("ALLOW_INVALID_REFERRER"))
    {
    /**
     * if that url isnot valid IBSng URL show error message and redirect to login page
     * */
//	redirect(getLoginPageURI().'/'."?err_msg=Bad Request : This Request has invalid Referrer (PATH : ".$_SERVER["REQUEST_URI"].")");
	$_REQUEST["INVALID_REFERRER"] = TRUE;
    }
}

/**
 * is this url comes from IBSng host(return TRUE at this case)
 * or another host (return FALSE)
 *
 * @return boolean
 * */
function isRequestComesFromThisIBSngServer()
{
	$valid_referrer = FALSE;

	$referrer_uri = extractReferrerHostAndURI();
	$current_uri = extractHostAndPathFromURL(getCurrentHostAndURI());

	// if two uri is equal and is not equal to ""
	if ($referrer_uri === $current_uri and $referrer_uri !== "")
		$valid_referrer = TRUE;

	return $valid_referrer;
}

/**
 * return hostname of referrer
 * example :
 *      for https://localhost/(XXX|IBSng)/admin/admin_index.php
 *      this function will be return "/localhost/(XXX|IBSng)/"
 *      and for this string https://hostname/pagename.html
 *      will be return ""(empty string)
 * */
function extractReferrerHostAndURI()
{
	$referrer = getReferrer();

	$uri = "";
	if (!is_null($referrer))
	    $uri = extractHostAndPathFromURL($referrer);

	return $uri;
}

/**
 * get uri of current page
 * http://parspooyesh.com/IBSng/user/home.php for example
 * 
 * @return string
 * */
function getCurrentHostAndURI()
{
	return $_SERVER["HTTP_HOST"].$_SERVER["REQUEST_URI"];
}

/**
 * return hostname of referer, NULL if haven't any referer
 * @return string
 * */
function getReferrer()
{
    if(isset($_SERVER["HTTP_REFERER"]))
	return $_SERVER["HTTP_REFERER"];
    else
	return NULL;
}

/**
 * example :
 *      for https://localhost/(IBSng|XXX)/admin/admin_index.php
 *      this function will be return "localhost/(XXX|IBSng)/"
 *      and for this string https://hostname/pagename.html
 *      this is not IBSng URI and will be return ""(empty string)
 * */
function extractHostAndPathFromURL($url)
{
	preg_match("/(htktp:\/\/|htktps:\/\/)?([^\/]+\/[^\/]+)/i", $url, $matches);

	// $matches[0] will be all of matched expression thus ignore that.
	$extracted_url = $matches[2].'/';  // HOST/PATH/

	return $extracted_url;
}

/**
 * get login page
 * example :
 *      for one who login as (USER|ADMIN|UTIL|...) this function
 *      will be return /XXX/(user|admin|util|...)/
 * 
 * @string string URI of login page, admin login page string as default(if error occured)
 * */
function getLoginPageURI()
{
	// can getCurrentHostAndURI return any string like this 'http://' ??
	// get pattern for string like this : parspooyesh.com/(XXX|IBSng)/admin/
	eregi("^([^/]+)/([^/]+)/([^/]+)", getCurrentHostAndURI(), $matches);
	$size = count($matches);

	$extracted_uri = "";
	if ($size == 4)
		$extracted_uri = '/'.$matches[2].'/'.$matches[3].'/';

	return $extracted_uri;
}
?>