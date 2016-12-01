{include file="admin_header.tpl" title="Add User Save Details" selected="Add User Saves"} 
{include file="err_head.tpl"}


{viewTable title="Details" double=TRUE}
    {addEditTD type="left1" double=TRUE}
	ID
    {/addEditTD}
    {addEditTD type="right1" double=TRUE}
        {$add_user_save_id} 
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Date
    {/addEditTD}
    {addEditTD type="right2" double=TRUE}
	{$add_date_formatted}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Admin
    {/addEditTD}
    {addEditTD type="right1" double=TRUE}
        {$admin_name} 
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Type
    {/addEditTD}
    {addEditTD type="right2" double=TRUE}
	{$type_str}
    {/addEditTD}

    {addEditTD type="left" double=TRUE comment=TRUE}
	Comment
    {/addEditTD}
    {addEditTD type="right" double=TRUE comment=TRUE}
        {$comment} 
    {/addEditTD}

{/viewTable}

{listTable title="Saved User Add Details" cols_num=6}
    {listTR type="header"}
	{listTD}
	    Row No.
	{/listTD}	
    
	{listTD}
	    User ID
	{/listTD}

	{listTD}
	    Username 
	{/listTD}

	{listTD}
	    Password
	{/listTD}

    {/listTR}

  {foreach from=`$details[0]` item=user_id key=idx}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		{counter}
	    {/listTD}
	    {listTD}
		<a href="/IBSng/admin/user/user_info.php?user_id={$user_id}" class="link_in_body">
		    {$user_id}
		</a>
	    {/listTD}

	    {listTD}
		{$details[1][$idx]}
	    {/listTD}

	    {listTD}
		{$details[2][$idx]}
	    {/listTD}
	{/listTR}
    {/foreach}
{/listTable}

<form action="add_user_save_details.php">
<input type=hidden name="add_user_save_id" value="{$add_user_save_id}">
{addEditTable title="Download As CSV"}
    {addEditTD type="left"}
	Separator
    {/addEditTD}
    {addEditTD type="right"}
	{separatorSelect name="csv" default_request="csv"}
    {/addEditTD}
{/addEditTable}
</form>

{addRelatedLink}
    <a href="/IBSng/admin/user/add_user_save_details.php?delete=1&add_user_save_id={$add_user_save_id}" class="RightSide_links" {jsconfirm}>
	Delete This Add User Save
    </a>
{/addRelatedLink}

{addRelatedLink}
    <form method=POST action="/IBSng/admin/user/user_info.php" name="all_users_info">
	<input type=hidden name=user_id_multi value="{arrayJoin glue="," array=`$details[0]`}">
	<a href="#" onClick="document.all_users_info.submit()" class="RightSide_links">
	    All Users Information
	</a>
    </form>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/user/search_add_user_saves.php" class="RightSide_links">
	Search Add User Saves
    </a>
{/addRelatedLink}

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


{setAboutPage title="Add User Save Details"}
    
{/setAboutPage}


{include file="admin_footer.tpl"}    