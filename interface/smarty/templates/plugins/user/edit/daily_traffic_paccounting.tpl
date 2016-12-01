{attrUpdateMethod update_method="dailyTrafficPAccounting"}
{userInfoTable title="Daily Traffic Periodic Accounting" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Daily Traffic Periodic Accounting
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_daily_traffic_paccounting" value="t" class=checkbox  onClick='daily_traffic_paccounting_select.toggle("traffic_periodic_accounting_daily")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="traffic_periodic_accounting_daily" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Number of days in period
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input id="traffic_periodic_accounting_daily" type=text name="traffic_periodic_accounting_daily" value="{attrDefault target="user" default_var="traffic_periodic_accounting_daily" default_request="traffic_periodic_accounting_daily"}" class=small_text> 
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="traffic_periodic_accounting_daily"}
	    {$group_attrs.traffic_periodic_accounting_daily}
	{/ifHasAttr} 
	{helpicon subject="Daily Traffic Periodic Accounting" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Daily Traffic Limit
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{capture name="value"}{attrDefault target="user" default_var="traffic_periodic_accounting_daily_limit" default_request="traffic_periodic_accounting_daily_limit"}{/capture}
	<input id="traffic_periodic_accounting_daily_limit" type=text name="traffic_periodic_accounting_daily_limit" value="{math equation="x/(1024*1024)" x=`$smarty.capture.value`}" class=text> MBytes
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="traffic_periodic_accounting_daily_limit"}
	    {$group_attrs.traffic_periodic_accounting_daily_limit|byte}
	{/ifHasAttr} 
	{helpicon subject="Daily Traffic Periodic Accounting Limit" category="user"}
    {/userInfoTD}

{/userInfoTable}
<br>
<script language="javascript">
	daily_traffic_paccounting_select=new DomContainer();
	daily_traffic_paccounting_select.disable_unselected=true;
	daily_traffic_paccounting_select.addByID("traffic_periodic_accounting_daily",["traffic_periodic_accounting_daily_limit"]);
{if attrDefault($user_attrs,"traffic_periodic_accounting_daily","has_daily_traffic_paccounting")!=""}
    daily_traffic_paccounting_select.select("traffic_periodic_accounting_daily");
    document.user_edit.has_daily_traffic_paccounting.checked = true;
{else}
    daily_traffic_paccounting_select.select(null);
{/if}
</script>