{attrUpdateMethod update_method="monthlyTimePAccountingUsage"}
{userInfoTable title="Monthly Time Periodic Accounting" nofoot="TRUE"}
    {addEditTD type="left"}
	Monthly Time Period Usage Change Amount
    {/addEditTD}

    {addEditTD type="right"}
	<input id="time_periodic_accounting_monthly_usage" type=text name="time_periodic_accounting_monthly_usage" value="0" class=text disabled=true> Hours
    {/addEditTD}

{/userInfoTable}
<br>
{if attrDefault($user_attrs,"time_periodic_accounting_monthly_usage","")!=""}
<script language="javascript">
    document.user_edit.time_periodic_accounting_monthly_usage.disabled = false;
</script>    
{/if}
