{attrUpdateMethod update_method="monthlyTrafficPAccounting"}
{userInfoTable title="Monthly Traffic Periodic Accounting" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Monthly Traffic Periodic Accounting
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_monthly_traffic_paccounting" value="t" class=checkbox  onClick='monthly_traffic_paccounting_select.toggle("traffic_periodic_accounting_monthly")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="traffic_periodic_accounting_monthly" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Monthly Reset Type
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{monthlyResetType target="user" default_var="traffic_periodic_accounting_monthly" default_request="traffic_periodic_accounting_monthly" name="traffic_periodic_accounting_monthly" default="gregorian"}
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
	{capture name="value"}{attrDefault target="user" default_var="traffic_periodic_accounting_monthly_limit" default_request="traffic_periodic_accounting_monthly_limit"}{/capture}
	<input id="traffic_periodic_accounting_monthly_limit" type=text name="traffic_periodic_accounting_monthly_limit" value="{math equation="x/(1024*1024)" x=`$smarty.capture.value`}" class=text> MBytes
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="traffic_periodic_accounting_monthly_limit"}
	    {$group_attrs.traffic_periodic_accounting_monthly_limit|byte}
	{/ifHasAttr} 
	{helpicon subject="Monthly Traffic Periodic Accounting Limit" category="user"}
    {/userInfoTD}

{/userInfoTable}
<br>
<script language="javascript">
	monthly_traffic_paccounting_select=new DomContainer();
	monthly_traffic_paccounting_select.disable_unselected=true;
	monthly_traffic_paccounting_select.addByID("traffic_periodic_accounting_monthly",["traffic_periodic_accounting_monthly_limit"]);
{if attrDefault($user_attrs,"traffic_periodic_accounting_monthly","has_monthly_traffic_paccounting")!=""}
    monthly_traffic_paccounting_select.select("traffic_periodic_accounting_monthly");
    document.user_edit.has_monthly_traffic_paccounting.checked = true;
{else}
    monthly_traffic_paccounting_select.select(null);
{/if}
</script>