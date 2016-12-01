<?php

/**
 * used when want to attach file
 */
class HeaderGenerator
{
    function assignHeader($type, $fileName = "")
    {
        header("Content-Type: text/{$type}");
	if ($fileName != "")
	    header("Content-Disposition: attachment; filename={$fileName}");	
    }
}