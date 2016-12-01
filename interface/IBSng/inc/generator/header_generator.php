<?php

/**
 * used when want to attach file
 */
class HeaderGenerator
{
    /**
     * @param $type type of attachment
     * @param $filename name of your file
     * @author hossein
     * access public
     */
    function assignHeader($type, $fileName = "")
    {
        header("Content-Type: text/{$type}");
	if ($fileName != "")
	    header("Content-Disposition: attachment; filename={$fileName}");	
    }
}

?>