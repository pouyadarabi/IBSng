<?php
require_once("../../inc/init.php");
require_once(IBSINC."user.php");

if(isInRequest("type","username","image","current_username"))
    checkUser($_REQUEST["type"],$_REQUEST["username"],$_REQUEST["current_username"],$_REQUEST["image"]=="t");
else
{
    print "Invalid Input!";
    exit();
}

function checkUser($type,$username,$current_username,$ret_image)
{
    if($type=="normal")
        checkNormalUser($username,$current_username,$ret_image);
    else if ($type=="voip")
        checkVoIPUser($username,$current_username,$ret_image);
}

function checkNormalUser($username,$current_username,$ret_image)
{
    $req=new CheckNormalUsernameForAdd($username,$current_username);
    $resp=$req->sendAndRecv();
    if($ret_image)
        returnImage($resp);
    else
        returnText($resp);
}

function checkVoIPUser($username,$current_username,$ret_image)
{
    $req=new CheckVoIPUsernameForAdd($username,$current_username);
    $resp=$req->sendAndRecv();
    if($ret_image)
        returnImage($resp);
    else
        returnText($resp);
}

function returnText($resp)
{
    $smarty=new IBSSmarty();
    if($resp->isSuccessful())
        $smarty->assign("alerts",$resp->getResult());
    else
    {
        $resp->setErrorInSmarty($smarty);
        $smarty->assign("alerts",array());
    }
    $smarty->display("admin/user/check_user_for_add.tpl");
}

function returnImage($resp)
{
    if (!$resp->isSuccessful() or sizeof($resp->getResult())>0)
        returnNotOKImage();
    else
        returnOKImage();
}


function returnNotOKImage()
{
    showImageContents("invalid_icon.gif");
}

function returnOKImage()
{
    showImageContents("valid_icon.gif");
}

function showImageContents($img_file)
{/*Warning: Don't use very large image file! */
    header("Content-Type: image/gif\r\n");
    $img_file=IMAGES_ROOT."icon/".$img_file;
    $fd=fopen ($img_file,"r");
    if($fd===FALSE)
        return;
    print fread ($fd, filesize ($img_file));
    fclose ($fd);
//    redirect(IMAGES_ROOT."icon/".$img_file);
}
?>