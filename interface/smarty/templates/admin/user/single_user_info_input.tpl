{include file="admin_header.tpl" title="User Information" selected="User Information"}
{include file="err_head.tpl"}
<form method=GET action="/IBSng/admin/user/user_info.php" name="user_info">
    {addEditTable title="User ID"}
	{addEditTD type="left"}
	    User ID
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=user_id_multi class=text value="{ifisinrequest name="user_id_multi"}">
	    {multistr form_name="user_info" input_name="user_id_multi"}
	{/addEditTD}
		
    {/addEditTable}
</form>

<form method=GET action="/IBSng/admin/user/user_info.php" name="user_info_normal">
    {addEditTable title="Internet Username"}
	{addEditTD type="left"}
	    Internet Username
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=normal_username_multi class=text value="{ifisinrequest name="normal_username_multi"}">
	    {multistr form_name="user_info_normal" input_name="normal_username_multi"}
	{/addEditTD}
		
    {/addEditTable}
</form>

<form method=GET action="/IBSng/admin/user/user_info.php" name="user_info_voip">
    {addEditTable title="VoIP Username"}
	{addEditTD type="left"}
	    VoIP Username
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=voip_username_multi class=text value="{ifisinrequest name="voip_username_multi"}">
	    {multistr form_name="user_info_voip" input_name="voip_username_multi"}
	{/addEditTD}
		
    {/addEditTable}
</form>

{addRelatedLink}
    <a href="/IBSng/admin/user/search_user.php" class="RightSide_links">
	Search User 
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/user/add_new_users.php" class="RightSide_links">
	Add New User
    </a>
{/addRelatedLink}

{setAboutPage title="User Info"}
You can enter user id or normal username of one user to see his information
{/setAboutPage}


{include file="admin_footer.tpl"}