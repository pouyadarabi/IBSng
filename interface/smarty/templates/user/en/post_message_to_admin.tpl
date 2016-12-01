{* Post Message
    
    Success: this page is hown with success message at top
    Failure: this page is shown again with error message at top of the page

*}
{include file="user_header.tpl" title="Post Message To Admin" selected="user_messages"}
{include file="err_head.tpl"}

{headerMsg var_name="post_message_success"}
	Message Posted Successfully.
{/headerMsg}

<form method=POST action="post_message_to_admin.php">
    {addEditTable title="Post Message To Admin" action_icon="ok"}

	{addEditTD type="left" err="comment_err" comment=TRUE}
    	    Message
	{/addEditTD}
	{addEditTD type="right" comment=TRUE}
    	    <textarea name=message class=text>{ifisinrequest name="message"}</textarea>
	{/addEditTD}
	
    {/addEditTable}
</form>

{include file="user_footer.tpl"}
