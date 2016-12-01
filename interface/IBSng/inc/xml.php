<?php

function convDicToXML($dic)
{/* Convert a dictionry to xml*/
    $xml="";
    foreach($dic as $key=>$value)
    {
        if(is_array($value))
            $value=convDicToXML($value);
        else
            $value=cdataWrap($value);
        $xml.="<{$key}>{$value}</{$key}>";
    }
    return $xml;
}


function convAllDicsToXML($arr, $row_node_name)
{/* convert a list of dictionaries to XML. Wrapping each dictionary with $row_node_name
*/
    $xml="";
    foreach($arr as $dic)
        $xml.="<{$row_node_name}>".convDicToXML($dic)."</{$row_node_name}>";
    return $xml;
}

function xmlAnswer($ancest_node_name,$success,$xml_response,$reason="")
{
    header("Content-Type: text/xml");

    $dtd="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
    $head="<{$ancest_node_name}><result>";
    if($success)
        $head.="SUCCESS";
    else
        $head.="FAILURE";

    $head.="</result>";
    
    if(!$success)
        $head.="<reason>{$reason}</reason>";
    
    return $dtd.$head.$xml_response."</{$ancest_node_name}>";
}

////////////////////////////////
function cdataEscape($str)
{// escape data to be put in XML cdata type. return escaped string
    return preg_replace("/\]\]>|CDATA\[/i","",$str);
}

function cdataWrap($value)
{//wrap value into cdata escaped xml
    $value=cdataEscape($value);
    return "<![CDATA[{$value}]]>";
}
?>