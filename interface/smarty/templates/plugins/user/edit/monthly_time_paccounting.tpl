{attrUpdateMethod update_method="monthlyTimePAccounting"}
{userInfoTable title="Monthly Time Periodic Accounting" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Monthly Time Periodic Accounting
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_monthly_time_paccounting" value="t" class=checkbox  onClick='monthly_time_paccounting_select.toggle("time_periodic_accounting_monthly")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="time_periodic_accounting_monthly" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Monthly Reset Type
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{monthlyResetType target="user" default_var="time_periodic_accounting_monthly" default_request="time_periodic_accounting_monthly" name="time_periodic_accounting_monthly" default="gregorian"}
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
	{capture name="value"}{attrDefault target="user" default_var="time_periodic_accounting_monthly_limit" default_request="time_periodic_accounting_monthly_limit"}{/capture}
	<input id="time_periodic_accounting_monthly_limit" type=text name="time_periodic_accounting_monthly_limit" value="{$smarty.capture.value|duration}" class=text> Hours
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="time_periodic_accounting_monthly_limit"}
	    {$group_attrs.time_periodic_accounting_monthly_limit|duration}
	{/ifHasAttr} 
	{helpicon subject="Monthly Time Periodic Accounting Limit" category="user"}
    {/userInfoTD}

{/userInfoTable}
<br>
<script language="javascript">
	monthly_time_paccounting_select=new DomContainer();
	monthly_time_paccounting_select.disable_unselected=true;
	monthly_time_paccounting_select.addByID("time_periodic_accounting_monthly",["time_periodic_accounting_monthly_limit"]);
{if attrDefault($user_attrs,"time_periodic_accounting_monthly","has_monthly_time_paccounting")!=""}
    monthly_time_paccounting_select.select("time_periodic_accounting_monthly");
    document.user_edit.has_monthly_time_paccounting.checked = true;
{else}
    monthly_time_paccounting_select.select(null);
{/if}
</script>