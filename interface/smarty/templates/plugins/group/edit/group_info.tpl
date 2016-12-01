<input type="hidden" name="group_id" value="{$group_id}">
{attrUpdateMethod update_method="groupInfo"}
{viewTable title="Group Information" nofoot="TRUE"}
    {addEditTD type="left"}
	Group ID
    {/addEditTD}

    {addEditTD type="right"}
	{$group_id}
    {/addEditTD}

    {addEditTD type="left"}
	Group Name
    {/addEditTD}

    {addEditTD type="right"}
	<input class=text type=text name="group_name" value="{ifisinrequest name="group_name" default_var="group_name"}">
    {/addEditTD}

    {addEditTD type="left"}
	Owner Name
    {/addEditTD}

    {addEditTD type="right"}
	{if canDo("SEE ADMIN INFO")}
	    {admin_names_select name=owner_name default_request="owner_name" default=`$owner_name` }
	{else}
	    <input type=hidden name="owner_name" value="{$owner_name}">
	    {$owner_name}
	{/if}
	
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Comment
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	<textarea name=comment class=text>{strip}{ifisinrequest name="comment" default_var="comment"}{/strip}</textarea>
    {/addEditTD}
{/viewTable}
<br>
