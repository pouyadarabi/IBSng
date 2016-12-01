{userInfoTable title="Monthly Traffic" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="monthly_traffic_paccounting"} {/if}
	    Monthly Reset Type
	{/strip}
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="traffic_periodic_accounting_monthly"}
		    {$user_attrs.traffic_periodic_accounting_monthly|capitalize}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="traffic_periodic_accounting_monthly"}
		    {$group_attrs.traffic_periodic_accounting_monthly|capitalize}
		{/ifHasAttr} 
		{helpicon subject="Monthly Traffic Periodic Accounting" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Monthly Traffic Limit
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="traffic_periodic_accounting_monthly_limit"}
		    {$user_attrs.traffic_periodic_accounting_monthly_limit|byte}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="traffic_periodic_accounting_monthly_limit"}
		    {$group_attrs.traffic_periodic_accounting_monthly_limit|byte}
		{/ifHasAttr} 
		{helpicon subject="Monthly Traffic Periodic Accounting Limit" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="monthly_traffic_paccounting_usage"} {/if}
	    This Period Usage
	{/strip}
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="traffic_periodic_accounting_monthly_usage"}
		    {$user_attrs.traffic_periodic_accounting_monthly_usage|byte}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		Not Applicable
		{helpicon subject="Monthly Traffic Periodic Accounting Usage" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Next Reset
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="traffic_periodic_accounting_monthly_reset"}
		    {$user_attrs.traffic_periodic_accounting_monthly_reset}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		Not Applicable
		{helpicon subject="Monthly Traffic Periodic Accounting Reset" category="user"}
    {/userInfoTD}


{/userInfoTable}

