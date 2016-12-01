{* Admin Lock
    
*}
{include file="admin_header.tpl" title="Admin List" selected="Admin List"}
{include file="err_head.tpl"}

<form method="POST" action="admin_info.php">
<input type=hidden name="admin_username" value="{$admin_username}">
<input type=hidden name="lock" value="1">

{addEditTable title="Lock Admin"}
    {addEditTD type="left"}
        Admin
    {/addEditTD}
    {addEditTD type="right"}
	{$admin_username}
    {/addEditTD}
    {addEditTD type="left" comment=TRUE}
        Reason
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	<textarea name="reason" class=text>{ifisinrequest name="reason"}</textarea>
    {/addEditTD}
{/addEditTable}
</form>

{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_info.php?admin_username{$admin_username}" class="RightSide_links">
	Admin <b>{$admin_username}</b> Info
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
{setAboutPage title="Admin List"}
A list of all admins are shown here.
{/setAboutPage}

{include file="admin_footer.tpl"}