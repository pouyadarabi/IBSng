{viewTable title="Daily Traffic" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="daily_traffic_paccounting"}{/if}
	    Number of days in period
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="traffic_periodic_accounting_daily"}
	    {$group_attrs.traffic_periodic_accounting_daily}
	{/ifHasAttr} 
	{helpicon subject="Daily Traffic Periodic Accounting" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Daily Traffic Limit
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="traffic_periodic_accounting_daily_limit"}
	    {$group_attrs.traffic_periodic_accounting_daily_limit|byte}
	{/ifHasAttr} 
	{helpicon subject="Daily Traffic Periodic Accounting Limit" category="user"}
    {/addEditTD}
{/viewTable}
