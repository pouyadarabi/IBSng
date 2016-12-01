{viewTable title="Save BW Usage" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="save_bw_usage"}{/if}
	    Save BW Usage
	{/strip}
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
	{ifHasAttr object="group" var_name="save_bw_usage" alternate="No"}
	    Yes
	{/ifHasAttr} 
	{helpicon subject="Save BW Usage" category="user"}
    {/addEditTD}

{/viewTable}
