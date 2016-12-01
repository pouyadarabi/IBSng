{attrUpdateMethod update_method="dailyTimePAccounting"}
{userInfoTable title="Daily Time Periodic Accounting" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Daily Time Periodic Accounting
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_daily_time_paccounting" value="t" class=checkbox  onClick='daily_time_paccounting_select.toggle("time_periodic_accounting_daily")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="time_periodic_accounting_daily" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Number of days in period 
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input id="time_periodic_accounting_daily" type=text name="time_periodic_accounting_daily" value="{attrDefault target="user" default_var="time_periodic_accounting_daily" default_request="time_periodic_accounting_daily"}" class=small_text> 
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="time_periodic_accounting_daily"}
	    {$group_attrs.time_periodic_accounting_daily}
	{/ifHasAttr} 
	{helpicon subject="Daily Time Periodic Accounting" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Daily Time Limit
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{capture name="value"}{attrDefault target="user" default_var="time_periodic_accounting_daily_limit" default_request="time_periodic_accounting_daily_limit"}{/capture}
	<input id="time_periodic_accounting_daily_limit" type=text name="time_periodic_accounting_daily_limit" value="{$smarty.capture.value|duration}" class=text> Hours
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="time_periodic_accounting_daily_limit"}
	    {$group_attrs.time_periodic_accounting_daily_limit|duration}
	{/ifHasAttr} 
	{helpicon subject="Daily Time Periodic Accounting Limit" category="user"}
    {/userInfoTD}

{/userInfoTable}
<br>
<script language="javascript">
	daily_time_paccounting_select=new DomContainer();
	daily_time_paccounting_select.disable_unselected=true;
	daily_time_paccounting_select.addByID("time_periodic_accounting_daily",["time_periodic_accounting_daily_limit"]);
{if attrDefault($user_attrs,"time_periodic_accounting_daily","has_daily_time_paccounting")!=""}
    daily_time_paccounting_select.select("time_periodic_accounting_daily");
    document.user_edit.has_daily_time_paccounting.checked = true;
{else}
    daily_time_paccounting_select.select(null);
{/if}
</script>