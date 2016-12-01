<?php
define("BYTE_FLOAT_PRECISION",2);

function smarty_modifier_byte($string, $unit_type="small_byte")
{       /*
            convert byte value to kb or mg or gb and put unit beside it
            $unit_type(string, optional): can be one of small_byte, bit, bit/s, small_byte/s
        */
    $bytes = (float)$string;
    
    if($unit_type == "bit")
    	$units=array("Bit","KBit","Mbit","Gbit");
    
    else if($unit_type == "bit/s")
    	$units=array(" Bit/s"," KBit/s"," MBit/s"," GBit/s");

    else if($unit_type == "small_byte/s")
    	$units=array("B/s","K/s","M/s","G/s");

    else
    	$units=array("B","K","M","G");
    
    $i = 0;
    while($bytes>=1024 and $i < sizeof($units))
    {
        $bytes /= 1024;
        $i ++;
    }

    return getFormattedBytes($bytes).$units[$i];
}

/*
 * return byte with BYTE_FLOAT_PRECISION as float precision
 */
function getFormattedBytes($bytes)
{ 
    $temp = round($bytes * pow(10,BYTE_FLOAT_PRECISION));
    
    $int_part = floor($temp / pow(10,BYTE_FLOAT_PRECISION));
    $float_part = $temp % pow(10,BYTE_FLOAT_PRECISION);

    if($float_part>0)
        return "{$int_part}.".leftPadZero($float_part,BYTE_FLOAT_PRECISION);
    else
        return $int_part;
}

//function leftPadZero($a,$b){return $a;}
//print smarty_modifier_byte(1.999)

?>
