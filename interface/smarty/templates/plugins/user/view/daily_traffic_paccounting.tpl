{userInfoTable title="Daily Traffic" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="daily_traffic_paccounting"} {/if}
	    Number of days in period
	{/strip}
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="traffic_periodic_accounting_daily"}
		    {$user_attrs.traffic_periodic_accounting_daily}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="traffic_periodic_accounting_daily"}
		    {$group_attrs.traffic_periodic_accounting_daily}
		{/ifHasAttr} 
		{helpicon subject="Daily Traffic Periodic Accounting" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Traffic Limit
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="traffic_periodic_accounting_daily_limit"}
		    {$user_attrs.traffic_periodic_accounting_daily_limit|byte}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="traffic_periodic_accounting_daily_limit"}
		    {$group_attrs.traffic_periodic_accounting_daily_limit|byte}
		{/ifHasAttr} 
		{helpicon subject="Daily Traffic Periodic Accounting Limit" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="daily_traffic_paccounting_usage"} {/if}
	    This Period Usage
	{/strip}
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="traffic_periodic_accounting_daily_usage"}
		    {$user_attrs.traffic_periodic_accounting_daily_usage|byte}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		Not Applicable
		{helpicon subject="Daily Traffic Periodic Accounting Usage" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Next Reset
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="traffic_periodic_accounting_daily_reset"}
		    {$user_attrs.traffic_periodic_accounting_daily_reset}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		Not Applicable
		{helpicon subject="Daily Traffic Periodic Accounting Reset" category="user"}
    {/userInfoTD}


{/userInfoTable}

