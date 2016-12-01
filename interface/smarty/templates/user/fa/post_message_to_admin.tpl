{* Post Message
    
    Success: this page is hown with success message at top
    Failure: this page is shown again with error message at top of the page

*}
{include file="user_header.tpl" title="ارسال پیغام به مدیرسیستم" selected="user_messages"}
{include file="err_head.tpl"}

{headerMsg var_name="post_message_success"}
	پیغام با موفقیت ارسال شد.
{/headerMsg}

<form method=POST action="post_message_to_admin.php">
    {addEditTable title="ارسال پیغام به مدیر" action_icon="ok"}

	{addEditTD type="left" err="comment_err" comment=TRUE}
    	    پیغام
	{/addEditTD}
	{addEditTD type="right" comment=TRUE}
    	    <textarea name=message class=text>{ifisinrequest name="message"}</textarea>
	{/addEditTD}
	
    {/addEditTable}
</form>

{include file="user_footer.tpl"}

