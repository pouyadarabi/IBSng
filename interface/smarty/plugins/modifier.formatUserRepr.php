<?php

function smarty_modifier_formatUserRepr($string)
{       /*
            Format Username Representation
            ex. I: ali will be converted to ali <sub>i</sub>
            
            Only string starting with I: and V: will be formatted. All other strings will be returned unchanged
        */
	$prefix = substr($string, 0, 2);
	switch($prefix)
	{
		case "I:":
		case "V:":
			$string = substr($string, 3);
			$identifier = ($prefix=="I:")?"Int":"VoIP";
			
			return "<SUP style='font-weight:bold;font-size:5pt;text-decoration:none'>{$identifier}</SUP>&nbsp;{$string}";
			break;
		default:
			return $string;
			break;
	}
}



?>
