<?php
require_once("init.php");

function getSeparatorChar($separator)
{
        if (in_array($separator,array(",",";","\t")))
            return $separator;
        else if ($separator=="TAB")
            return "\t";
        else
            return ",";
}


class CSVGenerator
{
    function CSVGenerator($separator=",",$buffer=False)
    {/*
        $seperator can be ",", ";","\t","TAB", or else it will be set as ","
        if $buffer is true, all lines are buffered instead of print
    */
        $this->separator=getSeparatorChar($separator);
        $this->do_buffer=$buffer;
        if($buffer)
            $this->buffer=array();
    }


    function doLine()
    {/*
        convert arguments to csv format
        if do_buffer is true , it will add the line to buffer
        else it will print the line
    */
        $arg_list=func_get_args();
        $this->doArray($arg_list);
    }

    function doArray($arr)
    {
        $line=join($this->separator,$arr)."\r\n";
        if($this->do_buffer)
            $this->buffer[]=$line;
        else
            print $line;
    }
    
    function sendHeader($filename)
    {

        header("Content-Type: Text/Text");
        header("Content-Disposition: attachment; filename=".$filename);
    }
    
}


class CSVParser
{
    function CSVParser($separator=",")
    {
        $this->contents="";
        $this->separator=getSeparatorChar($separator);
    }
    
    function readUploadedFile($field_name)
    {
        if(isset($_FILES[$field_name]["error"]) and $_FILES[$field_name]["error"])
            return "Error in uploading file, error code: {$_FILES[$field_name]["error"]}";
        else
            $this->readFile($_FILES[$field_name]["tmp_name"]);
        return TRUE;
    }
    
    function readFile($filename)
    {
        $handle = fopen ($filename, "r");
        $this->contents = fread ($handle, filesize ($filename));
        fclose ($handle);
    }
    
    function getArray()
    {//return parsed array of csv file
        $parsed=array();
        foreach(explode("\n",trim($this->contents)) as $line)
            $parsed[]=explode($this->separator,trim($line));
        return $parsed;
    }
    
}
?>