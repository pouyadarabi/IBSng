{* Add/Edit Interface
    interface_name: new interface name
    comment: comment!
    
    Success: client will be redirected to the new interface information page
    Failure: this page is shown again with error message at top of the page

*}
{include file="admin_header.tpl" title="`$action_title` Interface" selected="Bandwidth"}
{include file="err_head.tpl"}

<form method=POST action="add_interface.php">
<input type=hidden name={$action} value=1>
    {addEditTable title="`$action_title` Interface" action_icon="`$action_icon`"}

    {if $action == "edit"}
	<input type=hidden name=old_interface_name value="{$interface_name}">
	<input type=hidden name=interface_id value={$interface_id}>
	    {addEditTD type="left" err="interface_id_err"}
		Interface ID 
	    {/addEditTD}

	    {addEditTD type="right"}
		{$interface_id}
	    {/addEditTD}
    {/if}

	{addEditTD type="left" err="interface_name_err"}
	    Interface 
	{/addEditTD}

	{addEditTD type="right"}
	    <input type=text name=interface_name value="{ifisinrequest name="interface_name" default_var="interface_name"}" class="text">
	    {helpicon subject='interface name' category='bandwidth'}
	{/addEditTD}
	
	{addEditTD type="left" err="comment_err" comment=TRUE}
	    Comment
	{/addEditTD}
	{addEditTD type="right" comment=TRUE}
	    <textarea name=comment class=text>{ifisinrequest name="comment" default_var="comment"}</textarea>
	{/addEditTD}
	
    {/addEditTable}
</form>
{addRelatedLink}
    <a href="/IBSng/admin/bw/interface_list.php" class="RightSide_links">
	Interface list
    </a>
{/addRelatedLink}

{if $action == "add"}
    {setAboutPage title="Add Interface"}

    {/setAboutPage}
{else}
    {setAboutPage title="Edit Interface"}

    {/setAboutPage}
{/if}

{include file="admin_footer.tpl"}
