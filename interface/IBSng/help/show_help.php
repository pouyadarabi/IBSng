<?php
require_once("../inc/init.php");

if(!isInRequest("subject","category"))
    showHelpError("Invalid inputs");
else
    showHelp($_REQUEST["subject"],$_REQUEST["category"]);


function showHelp($subject,$category)
{
    $smarty=new IBSSmarty();
    $smarty->default_template_handler_func = 'template_handler_func';
    $smarty->assign("tpl_file",getTplFile($subject,$category));
    $smarty->assign("subject",$subject);
    $smarty->assign("category",$category);
    $smarty->display("help/skeleton.tpl");
}

function getTplFile($subject,$category)
{
    $subject=quotemeta(helpFixFileName($subject));
    $category=quotemeta(helpFixFileName($category));
    return "help/{$category}/{$subject}.tpl";
}

function helpFixFileName($file_name)
{
    $file_name=str_replace(" ","_",$file_name);
    $file_name=str_replace(".","_",$file_name);
    return $file_name;
}

function template_handler_func($resource_type, $resource_name, &$template_source, &$template_timestamp, &$smarty_obj)
{
    showHelpError("Help File Not Found!");
    return true; //unreachable
}

function showHelpError($msg="")
{
    print getHelpErrorContents($msg);
//    exit();
}

function getHelpErrorContents($msg)
{
    $smarty=new IBSSmarty();
    $smarty->assign("msg",$msg);
    return $smarty->fetch("help/error.tpl");
}

?>