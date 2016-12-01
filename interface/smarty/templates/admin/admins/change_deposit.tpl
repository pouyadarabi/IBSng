{include file="admin_header.tpl" title="Change Deposit" selected="Admin List"}
{include file="err_head.tpl"}

{if isset($change_successfull) and $change_successfull}

    {headerMsg}
	Deposit Changed Successfully
    {/headerMsg}

    {redirectToPage url="/IBSng/admin/admins/admin_info.php?admin_username=$admin_username" page_name="Admin Information"}

{else}

    <form method=POST action="change_deposit.php">
    <input type=hidden name=admin_username value="{$admin_username}">

    {addEditTable title="Change Deposit"}

	{addEditTD type="left" err="admin_username_err"}
	    Admin username
	{/addEditTD}
	{addEditTD type="right"}
	    {$admin_username}
	{/addEditTD}

	{addEditTD type="left" err="deposit_err"}
	    Deposit Change Amount
	{/addEditTD}
	{addEditTD type="right"}
	    <input name="deposit" value="{ifisinrequest name="deposit"}" class=text>
	{/addEditTD}

	{addEditTD type="left" err="deposit_comment_err"}
	    Deposit Change Comment
	{/addEditTD}
	{addEditTD type="right"}
	    <input name="deposit_comment" value="{ifisinrequest name="deposit_comment"}" class=text>
	{/addEditTD}
    {/addEditTable}
    </form>
{/if}

{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_info.php?admin_username={$admin_username}" class="RightSide_links">
	Admin <b>{$admin_username|capitalize}</b> info
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

{setAboutPage title="Change Deposit"}
You can increase or decrease admin deposit in this page
{/setAboutPage}

{include file="admin_footer.tpl"}
