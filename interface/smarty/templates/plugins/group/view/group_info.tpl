{viewTable title="Group Informations" nofoot="TRUE"}
    {addEditTD type="left"}
	    {strip}
		{if $can_change} {editCheckBox edit_tpl_name="group_info"} {/if}
		Group ID
	    {/strip}
    {/addEditTD}
    {addEditTD type="right"}
		{$group_id}
    {/addEditTD}

    {addEditTD type="left"}
		Group Name
    {/addEditTD}
    {addEditTD type="right"}
		{$group_name}
    {/addEditTD}

    {addEditTD type="left"}
		Owner Name
    {/addEditTD}
    {addEditTD type="right"}
		{$owner_name}
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
		Comment
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
		{$comment}
    {/addEditTD}
{/viewTable}
