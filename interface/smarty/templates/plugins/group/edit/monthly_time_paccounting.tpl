{attrUpdateMethod update_method="monthlyTimePAccounting"}

  {viewTable title="Monthly Time Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Monthly Time Periodic Accounting
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_monthly_time_paccounting" value="t" class=checkbox  onClick='monthly_time_paccounting_select.toggle("time_periodic_accounting_monthly")'>
    {/addEditTD}

    {addEditTD type="left"}
        Monthly Reset Type
    {/addEditTD}

    {addEditTD type="right"}
	{monthlyResetType target="group" default_var="time_periodic_accounting_monthly" default_request="time_periodic_accounting_monthly" name="time_periodic_accounting_monthly" default="gregorian"}
    {/addEditTD}

    {addEditTD type="left"}
	Monthly Time Limit
    {/addEditTD}

    {addEditTD type="right"}
	{capture name="value"}{attrDefault target="group" default_var="time_periodic_accounting_monthly_limit" default_request="time_periodic_accounting_monthly_limit"}{/capture}
	<input id="time_periodic_accounting_monthly_limit" type=text name="time_periodic_accounting_monthly_limit" value="{$smarty.capture.value|duration}" class=text> Hours
    {/addEditTD}

  {/viewTable}
  <BR>
<script language="javascript">
	monthly_time_paccounting_select=new DomContainer();
	monthly_time_paccounting_select.disable_unselected=true;
	monthly_time_paccounting_select.addByID("time_periodic_accounting_monthly",["time_periodic_accounting_monthly_limit"]);
{if attrDefault($group_attrs,"time_periodic_accounting_monthly","has_monthly_time_paccounting")!=""}
    monthly_time_paccounting_select.select("time_periodic_accounting_monthly");
    document.group_edit.has_monthly_time_paccounting.checked = true;
{else}
    monthly_time_paccounting_select.select(null);
{/if}
</script>