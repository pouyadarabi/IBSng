{* Post Message
    user_id: id of user, or String ALL USERS
    
    Success: this page is hown with success message at top
    Failure: this page is shown again with error message at top of the page

*}
{include file="admin_header.tpl" title="Post Message To User" selected="Admin Messages"}
{include file="err_head.tpl"}

{headerMsg var_name="post_message_success"}
	Message Posted Successfully.
{/headerMsg}


<form method=POST action="post_message_to_user.php">
    {addEditTable title="Post Message To User(s)" action_icon="ok"}

        {addEditTD type="left" err="user_id_err"}
	    User ID(s)
	{/addEditTD}

	{addEditTD type="right"}
    	    {$user_id|truncate:30}
	    <input type=hidden name="user_id" value="{$user_id}">
    	    {helpicon subject='user id' category='message'}
        {/addEditTD}
	
	{addEditTD type="left" err="comment_err" comment=TRUE}
    	    Message
	{/addEditTD}
	{addEditTD type="right" comment=TRUE}
    	    <textarea name=message class=text>{ifisinrequest name="message"}</textarea>
	{/addEditTD}
	
    {/addEditTable}
</form>

{addRelatedLink}
    <a href="/IBSng/admin/message/view_messages.php" class="RightSide_links">
	View Messages
    </a>
{/addRelatedLink}

{if isset($smarty.request.user_id) and $smarty.request.user_id ne "ALL USERS"}
    {addRelatedLink}
	<a href="/IBSng/admin/user/user_info.php?user_id_multi={$smarty.request.user_id}" class="RightSide_links">
	    User <b>{$smarty.request.user_id|truncate:15}</b> Info
        </a>
    {/addRelatedLink}
{/if}


{setAboutPage title="Post Message To User"}

{/setAboutPage}

{include file="admin_footer.tpl"}
