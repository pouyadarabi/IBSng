{userInfoTable title="Daily Time" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="daily_time_paccounting"} {/if}
	    Number of days in period
	{/strip}
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="time_periodic_accounting_daily"}
		    {$user_attrs.time_periodic_accounting_daily}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="time_periodic_accounting_daily"}
		    {$group_attrs.time_periodic_accounting_daily}
		{/ifHasAttr} 
		{helpicon subject="Daily Time Periodic Accounting" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Time Limit
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="time_periodic_accounting_daily_limit"}
		    {$user_attrs.time_periodic_accounting_daily_limit|duration}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="time_periodic_accounting_daily_limit"}
		    {$group_attrs.time_periodic_accounting_daily_limit|duration}
		{/ifHasAttr} 
		{helpicon subject="Daily Time Periodic Accounting Limit" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="daily_time_paccounting_usage"} {/if}
	    This Period Usage
	{/strip}
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="time_periodic_accounting_daily_usage"}
		    {$user_attrs.time_periodic_accounting_daily_usage|duration}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		Not Applicable
		{helpicon subject="Daily Time Periodic Accounting Usage" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Next Reset
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="time_periodic_accounting_daily_reset"}
		    {$user_attrs.time_periodic_accounting_daily_reset}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		Not Applicable
		{helpicon subject="Daily Time Periodic Accounting Reset" category="user"}
    {/userInfoTD}


{/userInfoTable}

