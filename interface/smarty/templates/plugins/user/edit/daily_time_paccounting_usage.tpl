{attrUpdateMethod update_method="dailyTimePAccountingUsage"}
{userInfoTable title="Daily Time Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	Daily Time Period Usage Change Amount
    {/addEditTD}

    {addEditTD type="right"}
	<input id="time_periodic_accounting_daily_usage" type=text name="time_periodic_accounting_daily_usage" value="0" class=text disabled=true> Hours
    {/addEditTD}

{/userInfoTable}
<br>
{if attrDefault($user_attrs,"time_periodic_accounting_daily_usage","")!=""}
<script language="javascript">
    document.user_edit.time_periodic_accounting_daily_usage.disabled = false;
</script>    
{/if}
