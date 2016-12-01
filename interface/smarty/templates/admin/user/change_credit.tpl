{include file="admin_header.tpl" title="Change Credit" selected="User Information"}
{include file="err_head.tpl"}

{if isset($change_successfull) and $change_successfull}
    {include file="admin/user/user_pages_redirect_user_info.tpl" msg="Credit Changed Successfully"}
{else}
    {include file="admin/user/user_pages_user_id_header.tpl"}    
    <form method=POST action="change_credit.php">
    <input type=hidden name=user_id value="{$user_id}">
    {addEditTable title="Change Credit"}
	{addEditTD type="left" err="credit_err"}
	    Credit Change Amount
	{/addEditTD}
	{addEditTD type="right"}
	    <input name="credit" value="{ifisinrequest name="credit"}" class=text>
	{/addEditTD}
	
	{addEditTD type="left"}
	    Credit Change Comment
	{/addEditTD}
	{addEditTD type="right"}
	    <input name="credit_comment" value="{ifisinrequest name="credit_comment"}" class=text>
	{/addEditTD}
    {/addEditTable}
    </form>
{/if}

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
You can increase or decrease user credit in this page
{/setAboutPage}

{include file="admin_footer.tpl"}
