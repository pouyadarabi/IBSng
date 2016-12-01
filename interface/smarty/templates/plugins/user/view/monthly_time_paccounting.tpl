{userInfoTable title="Monthly Time" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="monthly_time_paccounting"} {/if}
	    Monthly Reset Type
	{/strip}
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="time_periodic_accounting_monthly"}
		    {$user_attrs.time_periodic_accounting_monthly|capitalize}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="time_periodic_accounting_monthly"}
		    {$group_attrs.time_periodic_accounting_monthly|capitalize}
		{/ifHasAttr} 
		{helpicon subject="Monthly Time Periodic Accounting" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Monthly Time Limit
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="time_periodic_accounting_monthly_limit"}
		    {$user_attrs.time_periodic_accounting_monthly_limit|duration}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="time_periodic_accounting_monthly_limit"}
		    {$group_attrs.time_periodic_accounting_monthly_limit|duration}
		{/ifHasAttr} 
		{helpicon subject="Monthly Time Periodic Accounting Limit" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="monthly_time_paccounting_usage"} {/if}
	    This Period Usage
	{/strip}
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="time_periodic_accounting_monthly_usage"}
		    {$user_attrs.time_periodic_accounting_monthly_usage|duration}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		Not Applicable
		{helpicon subject="Monthly Time Periodic Accounting Usage" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Next Reset
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="time_periodic_accounting_monthly_reset"}
		    {$user_attrs.time_periodic_accounting_monthly_reset}
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		Not Applicable
		{helpicon subject="Monthly Time Periodic Accounting Reset" category="user"}
    {/userInfoTD}


{/userInfoTable}

