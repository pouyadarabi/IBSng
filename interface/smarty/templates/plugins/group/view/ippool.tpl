{viewTable title="IPpool" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="ippool"}{/if}
	    IPpool
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
		{ifHasAttr object="group" var_name="ippool"}
		    {$group_attrs.ippool}  
		{/ifHasAttr} 
		{helpicon subject="ippool" category="user"}
    {/addEditTD}

{/viewTable}
