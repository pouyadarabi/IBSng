{attrUpdateMethod update_method="monthlyTrafficPAccounting"}

  {viewTable title="Monthly Traffic Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Monthly Traffic Periodic Accounting
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_monthly_traffic_paccounting" value="t" class=checkbox  onClick='monthly_traffic_paccounting_select.toggle("traffic_periodic_accounting_monthly")'>
    {/addEditTD}

    {addEditTD type="left"}
        Monthly Reset Type
    {/addEditTD}

    {addEditTD type="right"}
	{monthlyResetType target="group" default_var="traffic_periodic_accounting_monthly" default_request="traffic_periodic_accounting_monthly" name="traffic_periodic_accounting_monthly" default="gregorian"}
    {/addEditTD}

    {addEditTD type="left"}
	Monthly Traffic Limit
    {/addEditTD}

    {addEditTD type="right"}
	{capture name="value"}{attrDefault target="group" default_var="traffic_periodic_accounting_monthly_limit" default_request="traffic_periodic_accounting_monthly_limit"}{/capture}
	<input id="traffic_periodic_accounting_monthly_limit" type=text name="traffic_periodic_accounting_monthly_limit" value="{math equation="x/(1024*1024)" x=`$smarty.capture.value`}" class=text> MBytes
    {/addEditTD}

  {/viewTable}
  <BR>
<script language="javascript">
	monthly_traffic_paccounting_select=new DomContainer();
	monthly_traffic_paccounting_select.disable_unselected=true;
	monthly_traffic_paccounting_select.addByID("traffic_periodic_accounting_monthly",["traffic_periodic_accounting_monthly_limit"]);
{if attrDefault($group_attrs,"traffic_periodic_accounting_monthly","has_monthly_traffic_paccounting")!=""}
    monthly_traffic_paccounting_select.select("traffic_periodic_accounting_monthly");
    document.group_edit.has_monthly_traffic_paccounting.checked = true;
{else}
    monthly_traffic_paccounting_select.select(null);
{/if}
</script>
