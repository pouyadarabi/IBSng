{attrUpdateMethod update_method="dailyTrafficPAccountingUsage"}
{userInfoTable title="Daily Traffic Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	Daily Traffic Period Usage Change Amount
    {/addEditTD}

    {addEditTD type="right"}
	<input id="traffic_periodic_accounting_daily_usage" type=text name="traffic_periodic_accounting_daily_usage" value="0" class=text disabled=true> MBytes
    {/addEditTD}

{/userInfoTable}
<br>
{if attrDefault($user_attrs,"traffic_periodic_accounting_daily_usage","")!=""}
<script language="javascript">
    document.user_edit.traffic_periodic_accounting_daily_usage.disabled = false;
</script>    
{/if}
