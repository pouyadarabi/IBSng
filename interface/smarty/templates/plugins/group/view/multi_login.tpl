{viewTable title="Multi Login" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="multi_login"} {/if}
	    Multi Login
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
		{ifHasAttr object="group" var_name="multi_login"}
		    {$group_attrs.multi_login} instances 
		{/ifHasAttr} 
		{helpicon subject="multi login" category="user"}
    {/addEditTD}
{/viewTable}

