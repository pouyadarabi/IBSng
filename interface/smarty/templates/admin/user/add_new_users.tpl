{* Add New User
    count: new group
    credit: 
    owner_name:
    group_name:
    credit_comment
    
    Success: client will be redirected to the new users information page
    Failure: this page is shown again with error message at top of the page

*}

{include file="admin_header.tpl" title="Add New Users" selected="Add New User"}
{include file="err_head.tpl"}
<script language="javascript" src="/IBSng/js/check_box_container.js"></script>

<form method=POST name=edit_user>
	<input type=hidden name=submit_form value=1>
	<input type=hidden name=add value=1>
	{addEditTable title="Add New Users" table_width="320"}
	{addEditTD type="left" err="count_err"}
	    Count
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=count value="{$count}" class=text>
	    {helpicon subject="count" category="user"}
	{/addEditTD}

	{addEditTD type="left" err="credit_err"}
	    Credit
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=credit value="{$credit}" class=text> {$MONEY_UNIT}
	    {helpicon subject="credit" category="user"}
	{/addEditTD}

<!--	{addEditTD type="left" err="credit_comment_err"}
	    Credit Change Comment
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=credit_comment value="{$credit_comment}" class=text>
	    {helpicon subject="credit_comment" category="user"}
	{/addEditTD} -->

	{addEditTD type="left" err="credit_comment_err"}
	    Owner
	{/addEditTD}

	{addEditTD type="right"}
		{if canDo("CHANGE_USER_OWNER")}
		    {admin_names_select name="owner_name" default_request="owner_name" default=$auth_name}
		{else}
		    {$auth_name}
		    <input type=hidden name="owner_name" value="{$auth_name}" class=text>
		{/if}
		{helpicon subject="owner" category="user"}
	{/addEditTD}
	    
	{addEditTD type="left" err="credit_comment_err"}
	    Group
	{/addEditTD}

	{addEditTD type="right"}
	    {group_names_select name="group_name" default="group_name"}
	    {helpicon subject="group" category="user"}
	
	{/addEditTD}
	
    {/addEditTable}

    {listTable no_header=TRUE no_foot=TRUE table_width=50%}
    {include file = "admin/report/skel_conditions.tpl"
					 name = "edit_attrs"
		 			 form_name = "edit_user"
					 title = "Attributes to Edit"
					 normal_username_checked="TRUE"
					 voip_username_checked="TRUE"
					 inc  = "admin/user/edit_select_attrs.tpl"}
    {/listTable}

</form>


{addRelatedLink}
    <a href="/IBSng/admin/user/search_user.php" class="RightSide_links">
	Search User
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/user/user_info.php" class="RightSide_links">
	User Information
    </a>
{/addRelatedLink}

{setAboutPage title="Add New User"}
Add New Users
{/setAboutPage}

{include file="admin_footer.tpl"}
