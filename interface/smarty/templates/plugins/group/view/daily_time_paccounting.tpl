{viewTable title="Daily Time" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="daily_time_paccounting"}{/if}
	    Number of days in period
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="time_periodic_accounting_daily"}
	    {$group_attrs.time_periodic_accounting_daily}
	{/ifHasAttr} 
	{helpicon subject="Daily Time Periodic Accounting" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Time Limit
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="time_periodic_accounting_daily_limit"}
	    {$group_attrs.time_periodic_accounting_daily_limit|duration}
	{/ifHasAttr} 
	{helpicon subject="Daily Time Periodic Accounting Limit" category="user"}
    {/addEditTD}
{/viewTable}
