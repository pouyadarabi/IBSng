{include file="user_header.tpl" title="مشاهده پیغامها " selected="view_messages"} 
{include file="err_head.tpl"} 
{include file="util/calendar.tpl"}

<p>
    <a href="/IBSng/user/post_message_to_admin.php" class="link_in_body" style="font-size: 10pt; font-weight: bold">
	ارسال پیغام به مدیر سیستم
    </a>
</p>

{headerMsg var_name="delete_message_success"}
	حذف پیغام با موفقیت انجام شد.
{/headerMsg}

<form method=POST action="view_messages.php#show_results" name="view_messages">
<input type=hidden name=show value=1>
<input type=hidden name=page value=1>

{addEditTable double=TRUE title="شرایط نمایش"}

    {addEditTD type="left1" double=TRUE}
	از تاریخ
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{absDateSelect name="post_date_from" default_request="post_date_from"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	تا تاریخ
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{absDateSelect name="post_date_to" default_request="post_date_to"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	مرتب بر اساس
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{html_options name="order_by" options=$order_bys selected=$order_by_default} 
	Desc <input name=desc type=checkbox {checkBoxValue name="desc" default_checked=TRUE always_in_form="show"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	تعداد نتایج در هر صفحه
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{reportRPP no_high=TRUE}
    {/addEditTD}

{/addEditTable}
</form>

{if isInRequest("show")}

<a name="show_results"></a>
{listTable title="لیست پیغامها" cols_num=4}
    {listTableHeaderIcon action="details"}
    {listTableHeaderIcon action="delete" close_tr=TRUE }

    {listTR type="header"}
	{listTD}
	    ردیف
	{/listTD}
	
	{listTD}
	    تاریخ
	{/listTD}
    
	{listTD}
	    به
	{/listTD}

	{listTD}
	    پیغام
	{/listTD}

    {/listTR}

  {foreach from=$messages item=row}
    {listTR type="body"}
	{listTD}
	    {counter}
	{/listTD}

	{listTD}
	    {$row.post_date_formatted}
	{/listTD}

	{listTD}
	    {if $row.user_id == "ALL USERS"}
		همه کاربران
	    {else}
	        {$auth_name}
	    {/if}
	{/listTD}

	{listTD}
	    <div id="message_text_truncated_{$row.message_id}" style="display: ;">
		{$row.message_text|truncate:80}
	    </div>

	    <div id="message_text_{$row.message_id}" style="display: none">
		{$row.message_text|nl2br|wordwrap:80:"<br />":true}
	    </div>
	{/listTD}

	{listTD icon=TRUE }
    	    <a onClick="return showMessage({$row.message_id});" href="#">
		{listTableBodyIcon cycle_color=TRUE action="details"}
	    </a>
	{/listTD}

	{listTD icon=TRUE }
    	    <a href="{requestToUrl ignore="delete"}&delete={$row.message_id}" {jsconfirm}>
		{listTableBodyIcon action="delete"}
	    </a>
	{/listTD}

    {/listTR}
  {/foreach}
    
{/listTable}    

{listTable title=مجموع cols_num=2}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		تعداد کل ردیف ها:
    	    {/listTD}
	    {listTD}
	        {$total_rows} 
	    {/listTD}

	{/listTR}
{/listTable}

{reportPages total_results=$total_rows}

{/if}

{include file="user_footer.tpl"}
