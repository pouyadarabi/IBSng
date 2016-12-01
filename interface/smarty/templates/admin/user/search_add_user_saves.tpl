{include file="admin_header.tpl" title="Add User Saves" selected="Add User Saves"} 
{include file="err_head.tpl"}
{include file="util/calendar.tpl"}

<form method=POST action="search_add_user_saves.php" name="search_add_user_saves">
<input type=hidden name=show value=1>
<input type=hidden name=page value=1>

{addEditTable double=TRUE title="Search Add User Saves Conditions"}
    {addEditTD type="left1" double=TRUE}
	Add User Save ID
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=text class=text name=add_user_save_id value="{ifisinrequest name="add_user_save_id"}"> {multistr input_name="add_user_save_id" form_name="search_add_user_saves"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Type
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{html_options name="type" values=$type_options output=$type_options selected=$type_default}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Date from
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{absDateSelect name="date_from" default_request="date_from"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Date To
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{absDateSelect name="date_to" default_request="date_to"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Contains User ID
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=text class=text name=user_id value="{ifisinrequest name="user_id"}"> {multistr input_name="user_id" form_name="search_add_user_saves"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Contains Username
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{op class="likestr" name="username_op" selected="username_op"}
	<input type=text class=text name=username value="{ifisinrequest name="username"}"> {multistr input_name="username" form_name="search_add_user_saves"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Issuer Admin	
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	{admin_names_select name="admin" default="All" default_request="admin" add_all=TRUE}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Comment
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	{op class="likestr" name="comment_op" selected="comment_op"}
	<input type=text class=text name=comment value="{ifisinrequest name="comment"}">
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
</form>
{if isInRequest("show")}
<a name="show_results"></a>
{listTable title=Totals cols_num=2}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		Total Number Of Rows:
    	    {/listTD}
	    {listTD}
	        {$total_rows} 
	    {/listTD}

	{/listTR}
{/listTable}


{listTable title="Saved User Adds" cols_num=7}
    {listTableHeaderIcon action="view" close_tr=TRUE}
    {listTR type="header"}
	{listTD}
	    Row
	{/listTD}

	{listTD}
	    Date
	{/listTD}

	{listTD}
	    Issuer Admin
	{/listTD}

	{listTD}
	    Type
	{/listTD}

	{listTD}
	    Comment
	{/listTD}

	{listTD}
	    Count
	{/listTD}

	{listTD}
	    Usernames
	{/listTD}
    {/listTR}

  {foreach from=$results item=row}
	{listTR type="body"}
	    {listTD}
		{counter}
	    {/listTD}

	    {listTD}
		{$row.add_date_formatted}
	    {/listTD}

	    {listTD}
		{$row.admin_name}
	    {/listTD}

	    {listTD}
		{$row.type_str}
	    {/listTD}

	    {listTD}
		{$row.comment|truncate:60}
	    {/listTD}

	    {listTD}
		{$row.users_count}
	    {/listTD}

	    {listTD}
		{arrayJoin array=`$row.details[1]` glue="," truncate=60}
	    {/listTD}
	    {listTD icon=TRUE}
		<a href="add_user_save_details.php?add_user_save_id={$row.add_user_save_id}">
		    {listTableBodyIcon cycle_color=TRUE action="view"}
		</a>
	    {/listTD}
	{/listTR}
    {/foreach}
{/listTable}
{reportPages total_results=$total_rows}

{/if}


{addRelatedLink}
    <a href="/IBSng/admin/user/add_new_users.php" class="RightSide_links">
	Add New Users
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/credit_changes.php" class="RightSide_links">
	Credit Changes
    </a>
{/addRelatedLink}


{setAboutPage title="Add User Saves"}
    
{/setAboutPage}


{include file="admin_footer.tpl"}    