{viewTable title="Monthly Traffic" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="monthly_traffic_paccounting"}{/if}
	    Monthly Reset Type
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="traffic_periodic_accounting_monthly"}
	    {$group_attrs.traffic_periodic_accounting_monthly|capitalize}
	{/ifHasAttr} 
	{helpicon subject="Monthly Traffic Periodic Accounting" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Monthly Traffic Limit
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="traffic_periodic_accounting_monthly_limit"}
	    {$group_attrs.traffic_periodic_accounting_monthly_limit|byte}
	{/ifHasAttr} 
	{helpicon subject="Monthly Traffic Periodic Accounting Limit" category="user"}
    {/addEditTD}
{/viewTable}
