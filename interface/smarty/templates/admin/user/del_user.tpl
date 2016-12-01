{include file="admin_header.tpl" title="Delete User" selected="User Information"}
{include file="err_head.tpl"}
{headerMsg var_name="delete_successful"}
    User(s) Deleted Successfully
{/headerMsg}
{include file="admin/user/user_pages_user_id_header.tpl"}    
<form method=POST action="del_user.php">
    <input type=hidden name=user_id value="{$user_id}">
    <input type=hidden name="delete" value=1>
    {addEditTable title="Delete User" action_icon="delete"}
	
	{addEditTD type="left"}
	    Comment
	{/addEditTD}
	{addEditTD type="right"}
	    <input name="delete_comment" value="{ifisinrequest name="delete_comment"}" class=text>
	{/addEditTD}

	{addEditTD type="left"}
	    Delete User(s) Connection Logs
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=checkbox name="delete_connection_logs" {checkBoxValue name="delete_connection_logs"}>
	{/addEditTD}

	{addEditTD type="left"}
	    Delete User(s) Audit Logs
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=checkbox name="delete_audit_logs" {checkBoxValue name="delete_audit_logs"}>
	{/addEditTD}

    {/addEditTable}
</form>

{addRelatedLink}
    <a href="/IBSng/admin/user/user_info.php?user_id_multi={$user_id|escape:"url"}" class="RightSide_links">
	User <b>{$user_id|truncate:15}</b> Info
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/user/search_user.php" class="RightSide_links">
	Seach User 
    </a>
{/addRelatedLink}

{setAboutPage title="User Info"}
You can delete user(s) here!
{/setAboutPage}

{include file="admin_footer.tpl"}
