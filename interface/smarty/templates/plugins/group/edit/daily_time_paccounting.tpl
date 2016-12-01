{attrUpdateMethod update_method="dailyTimePAccounting"}

  {viewTable title="Daily Time Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Daily Time Periodic Accounting
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_daily_time_paccounting" value="t" class=checkbox  onClick='daily_time_paccounting_select.toggle("time_periodic_accounting_daily")'>
    {/addEditTD}

    {addEditTD type="left"}
        Number of days in period 
    {/addEditTD}

    {addEditTD type="right"}
	<input id="time_periodic_accounting_daily" type=text name="time_periodic_accounting_daily" value="{attrDefault target="group" default_var="time_periodic_accounting_daily" default_request="time_periodic_accounting_daily"}" class=small_text> 
    {/addEditTD}

    {addEditTD type="left"}
	Daily Time Limit
    {/addEditTD}

    {addEditTD type="right"}
	{capture name="value"}{attrDefault target="group" default_var="time_periodic_accounting_daily_limit" default_request="time_periodic_accounting_daily_limit"}{/capture}
	<input id="time_periodic_accounting_daily_limit" type=text name="time_periodic_accounting_daily_limit" value="{$smarty.capture.value|duration}" class=text> Hours
    {/addEditTD}

  {/viewTable}
  <BR>
<script language="javascript">
	daily_time_paccounting_select=new DomContainer();
	daily_time_paccounting_select.disable_unselected=true;
	daily_time_paccounting_select.addByID("time_periodic_accounting_daily",["time_periodic_accounting_daily_limit"]);
{if attrDefault($group_attrs,"time_periodic_accounting_daily","has_daily_time_paccounting")!=""}
    daily_time_paccounting_select.select("time_periodic_accounting_daily");
    document.group_edit.has_daily_time_paccounting.checked = true;
{else}
    daily_time_paccounting_select.select(null);
{/if}
</script>