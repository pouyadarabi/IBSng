{attrUpdateMethod update_method="dailyTrafficPAccounting"}

  {viewTable title="Daily Traffic Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Daily Traffic Periodic Accounting
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_daily_traffic_paccounting" value="t" class=checkbox  onClick='daily_traffic_paccounting_select.toggle("traffic_periodic_accounting_daily")'>
    {/addEditTD}

    {addEditTD type="left"}
        Number of days in period 
    {/addEditTD}

    {addEditTD type="right"}
	<input id="traffic_periodic_accounting_daily" type=text name="traffic_periodic_accounting_daily" value="{attrDefault target="group" default_var="traffic_periodic_accounting_daily" default_request="traffic_periodic_accounting_daily"}" class=small_text> 
    {/addEditTD}

    {addEditTD type="left"}
	Daily Traffic Limit
    {/addEditTD}

    {addEditTD type="right"}
	{capture name="value"}{attrDefault target="group" default_var="traffic_periodic_accounting_daily_limit" default_request="traffic_periodic_accounting_daily_limit"}{/capture}
	<input id="traffic_periodic_accounting_daily_limit" type=text name="traffic_periodic_accounting_daily_limit" value="{math equation="x/(1024*1024)" x=`$smarty.capture.value`}" class=text> MBytes
    {/addEditTD}

  {/viewTable}
  <BR>
<script language="javascript">
	daily_traffic_paccounting_select=new DomContainer();
	daily_traffic_paccounting_select.disable_unselected=true;
	daily_traffic_paccounting_select.addByID("traffic_periodic_accounting_daily",["traffic_periodic_accounting_daily_limit"]);
{if attrDefault($group_attrs,"traffic_periodic_accounting_daily","has_daily_traffic_paccounting")!=""}
    daily_traffic_paccounting_select.select("traffic_periodic_accounting_daily");
    document.group_edit.has_daily_traffic_paccounting.checked = true;
{else}
    daily_traffic_paccounting_select.select(null);
{/if}
</script>
