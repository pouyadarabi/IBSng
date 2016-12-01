{* 
    Add New Group
    group_name: new group
    comment: 
    
    Success: client will be redirected to the new group information page
    Failure: this page is shown again with error message at top of the page

*}
{include file="admin_header.tpl" title="Add New Group" selected="Add New Group"}
{include file="err_head.tpl"}

<form method=POST>
    {addEditTable title="Add New Group"}
	{addEditTD type="left" err="name_err"}
	    Group Name
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text class=text name=group_name value="{$group_name}">
	    {helpicon subject='group name' category='group'}    
	{/addEditTD}
	
	{addEditTD type="left" err="comment_err" comment=TRUE}
	    Comment
	{/addEditTD}
	{addEditTD type="right" comment=TRUE}
	    <textarea name=comment class=text>{$comment|strip}</textarea>
	{/addEditTD}
	
    {/addEditTable}
</form>
{addRelatedLink}
    <a href="/IBSng/admin/group/group_list.php" class="RightSide_links">
	 Group List
    </a>
{/addRelatedLink}
{include file="admin_footer.tpl"}
