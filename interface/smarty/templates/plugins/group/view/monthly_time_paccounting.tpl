{viewTable title="Monthly Time" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="monthly_time_paccounting"}{/if}
	    Monthly Reset Type
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="time_periodic_accounting_monthly"}
	    {$group_attrs.time_periodic_accounting_monthly|capitalize}
	{/ifHasAttr} 
	{helpicon subject="Monthly Time Periodic Accounting" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Monthly Time Limit
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="time_periodic_accounting_monthly_limit"}
	    {$group_attrs.time_periodic_accounting_monthly_limit|duration}
	{/ifHasAttr} 
	{helpicon subject="Monthly Time Periodic Accounting Limit" category="user"}
    {/addEditTD}
{/viewTable}
