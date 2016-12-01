{if isset($user_attrs.time_periodic_accounting_daily)}

{viewTable title="Daily Time Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	Number of days in period
    {/addEditTD}
    {addEditTD type="right"}
	{$user_attrs.time_periodic_accounting_daily}
	{helpicon subject="Daily Time Periodic Accounting" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Time Limit
    {/addEditTD}
    {addEditTD type="right"}
	{$user_attrs.time_periodic_accounting_daily_limit|duration}
	{helpicon subject="Daily Time Periodic Accounting Limit" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	    This Period Usage
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="user" var_name="time_periodic_accounting_daily_usage"}
	    {$user_attrs.time_periodic_accounting_daily_usage|duration}
    	    {helpicon subject="Daily Time Periodic Accounting Usage" category="user"}
	{/ifHasAttr} 
    {/addEditTD}

    {addEditTD type="left"}
	    Next Reset
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="user" var_name="time_periodic_accounting_daily_reset"}
	    {$user_attrs.time_periodic_accounting_daily_reset}
    	    {helpicon subject="Daily Time Periodic Accounting Reset" category="user"}
	{/ifHasAttr} 
    {/addEditTD}
    
{/viewTable}

{/if}

{if isset($user_attrs.time_periodic_accounting_monthly)}

{viewTable title="Monthly Time Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	    Monthly Reset Type
    {/addEditTD}
    {addEditTD type="right"}
	{$user_attrs.time_periodic_accounting_monthly|capitalize}
	{helpicon subject="Monthly Time Periodic Accounting" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Monthly Time Limit
    {/addEditTD}
    {addEditTD type="right"}
	{$user_attrs.time_periodic_accounting_monthly_limit|duration}
	{helpicon subject="Monthly Time Periodic Accounting Limit" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	    This Period Usage
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="user" var_name="time_periodic_accounting_monthly_usage"}
	    {$user_attrs.time_periodic_accounting_monthly_usage|duration}
    	    {helpicon subject="Monthly Time Periodic Accounting Usage" category="user"}
	{/ifHasAttr} 
    {/addEditTD}

    {addEditTD type="left"}
	    Next Reset
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="user" var_name="time_periodic_accounting_monthly_reset"}
	    {$user_attrs.time_periodic_accounting_monthly_reset}
    	    {helpicon subject="Monthly Time Periodic Accounting Reset" category="user"}
	{/ifHasAttr} 
    {/addEditTD}
    
{/viewTable}

{/if}

<!-- Traffic -->

{if isset($user_attrs.traffic_periodic_accounting_daily)}

{viewTable title="Daily Traffic Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	Number of days in period
    {/addEditTD}
    {addEditTD type="right"}
	{$user_attrs.traffic_periodic_accounting_daily}
	{helpicon subject="Daily Traffic Periodic Accounting" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Traffic Limit
    {/addEditTD}
    {addEditTD type="right"}
	{$user_attrs.traffic_periodic_accounting_daily_limit|byte}
	{helpicon subject="Daily Traffic Periodic Accounting Limit" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	    This Period Usage
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="user" var_name="traffic_periodic_accounting_daily_usage"}
	    {$user_attrs.traffic_periodic_accounting_daily_usage|byte}
    	    {helpicon subject="Daily Traffic Periodic Accounting Usage" category="user"}
	{/ifHasAttr} 
    {/addEditTD}

    {addEditTD type="left"}
	    Next Reset
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="user" var_name="traffic_periodic_accounting_daily_reset"}
	    {$user_attrs.traffic_periodic_accounting_daily_reset}
    	    {helpicon subject="Daily Traffic Periodic Accounting Reset" category="user"}
	{/ifHasAttr} 
    {/addEditTD}
    
{/viewTable}

{/if}

{if isset($user_attrs.traffic_periodic_accounting_monthly)}

{viewTable title="Monthly Traffic Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	    Monthly Reset Type
    {/addEditTD}
    {addEditTD type="right"}
	{$user_attrs.traffic_periodic_accounting_monthly|capitalize}
	{helpicon subject="Monthly Traffic Periodic Accounting" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Monthly Traffic Limit
    {/addEditTD}
    {addEditTD type="right"}
	{$user_attrs.traffic_periodic_accounting_monthly_limit|byte}
	{helpicon subject="Monthly Traffic Periodic Accounting Limit" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	    This Period Usage
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="user" var_name="traffic_periodic_accounting_monthly_usage"}
	    {$user_attrs.traffic_periodic_accounting_monthly_usage|byte}
    	    {helpicon subject="Monthly Traffic Periodic Accounting Usage" category="user"}
	{/ifHasAttr} 
    {/addEditTD}

    {addEditTD type="left"}
	    Next Reset
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="user" var_name="traffic_periodic_accounting_monthly_reset"}
	    {$user_attrs.traffic_periodic_accounting_monthly_reset}
    	    {helpicon subject="Monthly Traffic Periodic Accounting Reset" category="user"}
	{/ifHasAttr} 
    {/addEditTD}
    
{/viewTable}

{/if}