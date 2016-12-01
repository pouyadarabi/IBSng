{include file="admin_header.tpl" title="View Admin Messages" selected="Admin Messages"} 
{include file="err_head.tpl"} 
{include file="util/calendar.tpl"}

{headerMsg var_name="delete_message_success"}
	Message(s) Deleted Successfully.
{/headerMsg}

<form method=POST action="view_messages.php#show_results" name="view_messages">
<input type=hidden name=show value=1>
<input type=hidden name=page value=1>

{addEditTable double=TRUE title="Admin Messages Conditions"}

    {addEditTD type="left1" double=TRUE}
	Post Date From
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{absDateSelect name="post_date_from" default_request="post_date_from"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Post Date To
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{absDateSelect name="post_date_to" default_request="post_date_to"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	User IDs
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=text class=text name=user_ids value="{ifisinrequest name="user_ids"}"> {multistr input_name="user_ids" form_name="view_messages"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Messages of
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	<input name=table type=radio value=admin {radioButtonValue name=table value=admin default_checked=TRUE}> Admins
	<input name=table type=radio value=user {radioButtonValue name=table value=user}> Users
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Sort By
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{html_options name="order_by" options=$order_bys selected=$order_by_default} 
	Desc <input name=desc type=checkbox {checkBoxValue name="desc" default_checked=TRUE always_in_form="show"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Result Per Page
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{reportRPP}
    {/addEditTD}

{/addEditTable}

{if isInRequest("show")}
<a name="show_results"></a>

{listTable title=Totals cols_num=2}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		Total Number Of Results:
    	    {/listTD}
	    {listTD}
	        {$total_rows} 
	    {/listTD}

	{/listTR}
{/listTable}

<script language="javascript" src="/IBSng/js/check_box_container.js"></script>
<script language="javascript">
    var message_ids=new CheckBoxContainer();
</script>
<input type=hidden name="bulk_delete_messages" value=1>
{listTable title="Messages" cols_num=6}
    {listTableHeaderIcon action="reply"}
    {listTableHeaderIcon action="view"}
    {listTableHeaderIcon action="delete" close_tr=TRUE }

    {listTR type="header"}
	{listTD}
	    <input type=checkbox name="check_all_messages"> 
	    <script language="javascript">
		message_ids.setCheckAll("view_messages","check_all_messages");
	    </script>
	{/listTD}
	
	{listTD}
	    Row
	{/listTD}
	
	{listTD}
	    Date
	{/listTD}

	{listTD}
	    User ID
	{/listTD}

	{listTD}
	    Username
	{/listTD}

	{listTD}
	    Message
	{/listTD}

    {/listTR}

  {foreach from=$messages item=row}
    {listTR type="body"}
	{listTD extra="onClick='event.cancelBubble=true;'"}
	    <input type=checkbox name="delete_message_id_{$row.message_id}" value="{$row.message_id}"> 
	    <script language="javascript">
		message_ids.addByName("view_messages","delete_message_id_{$row.message_id}");
	    </script>
	{/listTD}	
	
	{listTD}
	    {counter}
	{/listTD}

	{listTD}
	    {$row.post_date_formatted}
	{/listTD}

	{listTD}
	    <a class="link_in_body" href="/IBSng/admin/user/user_info.php?user_id={$row.user_id}">
	        {$row.user_id}
	    </a>

	{/listTD}

	{listTD}
	    {$row.username_text|formatUserRepr}
	{/listTD}

	{listTD}
	    <div id="message_text_truncated_{$row.message_id}" style="display: ;">
		{$row.message_text|strip_tags|truncate:80}
	    </div>

	    <div id="message_text_{$row.message_id}" style="display: none">
		{$row.message_text|nl2br|wordwrap:80:"<br />":true}
	    </div>
	{/listTD}

	{listTD icon=TRUE }
    	    <a href="/IBSng/admin/message/post_message_to_user.php?user_id={$row.user_id}">
		{listTableBodyIcon cycle_color=TRUE action="reply"}
	    </a>
	{/listTD}

	{listTD icon=TRUE }
    	    <a onClick="return showMessage({$row.message_id});" href="#">
		{listTableBodyIcon action="view"}
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
{if isInRequest("page")}
    <input type="hidden" name="delete_page" value="{$smarty.request.page}">
{/if}
<input align=center type=image src="/IBSng/images/icon/delete.gif" name=bulk_delete_messages value="Delete" {jsconfirm}>
</form>
<br />

{reportPages total_results=$total_rows ignore_in_url="delete,bulk_delete_messages,delete_page"}

{/if}

{if requestVal("user_ids") ne ""}
    {addRelatedLink}
	<a href="/IBSng/admin/user/user_info.php?user_id_multi={$smarty.request.user_ids}" class="RightSide_links">
	    User <b>{$smarty.request.user_ids|truncate:15}</b> Info
        </a>
    {/addRelatedLink}

{/if}

{addRelatedLink}
    <a href="/IBSng/admin/message/post_message_to_user.php" class="RightSide_links">
	Post Message To All Users
    </a>
{/addRelatedLink}

{setAboutPage title="View Admin Messages"}
    
{/setAboutPage}


{include file="admin_footer.tpl"}