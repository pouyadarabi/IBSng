{* 
    Change an Admin password
    username: username of admin to change permission
	      if user don't have permission to change other admin passwords
*}
{include file="admin_header.tpl" title="Change Admin Password" selected="Admin List"}
{include file="err_head.tpl"}
{headerMsg var_name="success"}
    Password for {$changed_username} Changed Successfully
{/headerMsg}

{headerMsg var_name="changed_self_password"}
    You must <a href="/IBSng/admin"> Relogin </a> Now!
{/headerMsg}

<form method=POST>
{if $can_change_others eq TRUE}
    {addEditTable title="Admin Change Password" table_width="300"}
	{addEditTD type="left" err="username_err"}
	    Username
	{/addEditTD}

	{addEditTD type="right"}
	    <select name=username>
		{html_options values=$usernames selected=$default_username output=$usernames}
	    </select>
	{/addEditTD}

	{addEditTD type="left" err="password_err"}
	    Password
	{/addEditTD}

	{addEditTD type="right"}
    	    <input class=text type=password name=password1>
	{/addEditTD}

	{addEditTD type="left" err="password_err"}
	    Confirm Password
	{/addEditTD}

	{addEditTD type="right"}
    	    <input class=text type=password name=password2>
	{/addEditTD}

    {/addEditTable}
{else}
    {addEditTable title="Admin Change Password" table_width="300"}
	{addEditTD type="left" err="username_err"}
	    Username
	{/addEditTD}

	{addEditTD type="right"}
	    {$self_username}
	{/addEditTD}

	{addEditTD type="left" err="password_err"}
	    Password
	{/addEditTD}

	{addEditTD type="right"}
    	    <input class=text type=password name=password1>
	{/addEditTD}

	{addEditTD type="left" err="password_err"}
	    Confirm Password
	{/addEditTD}

	{addEditTD type="right"}
    	    <input class=text type=password name=password2>
	{/addEditTD}

    {/addEditTable}
{/if}
</form>

{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_info.php?admin_username={$self_username}" class="RightSide_links">
	Admin {$self_username} info
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_list.php" class="RightSide_links">
	Admin List
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/admins/add_new_admin.php" class="RightSide_links">
	Add New Admin
    </a>
{/addRelatedLink}
{setAboutPage title="Admin Change Password"}

{/setAboutPage}
{include file="admin_footer.tpl"}