{attrUpdateMethod update_method="monthlyTrafficPAccountingUsage"}
{userInfoTable title="Monthly Traffic Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	Monthly Traffic Period Usage Change Amount
    {/addEditTD}

    {addEditTD type="right"}
	<input id="traffic_periodic_accounting_monthly_usage" type=text name="traffic_periodic_accounting_monthly_usage" value="0" class=text disabled=true> MBytes
    {/addEditTD}

{/userInfoTable}
<br>
{if attrDefault($user_attrs,"traffic_periodic_accounting_monthly_usage","")!=""}
<script language="javascript">
    document.user_edit.traffic_periodic_accounting_monthly_usage.disabled = false;
</script>    
{/if}
