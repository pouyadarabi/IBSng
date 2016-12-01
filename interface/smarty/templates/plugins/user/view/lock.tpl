{viewTable title="Lock" nofoot="TRUE" table_width="100%"}
    {addEditTD type="left" comment=TRUE}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="lock"} {/if}
	    User is Locked
	{/strip}
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
		{ifHasAttr object="user" var_name="lock" alternate="No"}
		    Yes, Reason: {$user_attrs.lock|nl2br} 
		{/ifHasAttr} 
		{helpicon subject="lock" category="user"}
    {/addEditTD}
{/viewTable}

