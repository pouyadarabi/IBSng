<?php


function formatBoolean($b)
{
	return $b == "t" ? "Yes" : "No";
}

function createLinkConnectionLogsUserID($user_id)
{
    $ret  = "<a class=\"link_in_body\" href=\"/IBSng/admin/user/user_info.php?user_id={$user_id}\">";
    $ret .= "{$user_id}";
    $ret .= "</a>";

    return $ret;
}

function formatServiceType($service)
{
	$services = array(
		    "internet" => "Internet",
		    "voip" => "VoIP");

	return isset ($services[$service]) ? $services[$service] : $service;
}

function lockFormat ($lock_reason)
{
	return $lock_reason == "-" ? "No" : "Yes"; 
}

/**
 * return A HREF link for given $url.
 * @param $url name of url
 * 
 * */
function formatWebAnalyzerLogsURL($url, $length = 80, $cut=false)
{
    $wrapped_URL = wordwrap($url, $length, "<BR/>", $cut);
    return "<a href={$url} style=visited:blue target=_blank>{$wrapped_URL}</a>";
}

function linkUserIDToUserInfo($user_id, $link_body="")
{
    if(!$link_body)
	$link_body = $user_id;
    
    $a_href = '<a href="/IBSng/admin/user/user_info.php?user_id_multi='.$user_id.'" class="link_in_body">';
    
    return $a_href.$user_id."</a>";
}

function linkAdminNameToAdminInfo($admin_name)
{
    $a_href = '<a href="/IBSng/admin/admins/admin_info.php?admin_username='.$admin_name.'" class="link_in_body">';
    return $a_href.$admin_name."</a>";
}

function linkGroupNameToGroupInfo ($group_name)
{
    $a_href = '<a href="IBSng/admin/group/group_info.php?group_name='.$group_name.'" class="link_in_body">';
    return $a_href.$group_name."</a>";
}
?>