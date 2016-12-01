{attrUpdateMethod update_method="absExpDate"}
{include file="util/calendar.tpl"}
  {viewTable title="Expiration Dates" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Absolute Expiration Date
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_abs_exp" value="t" class=checkbox {if attrDefault($group_attrs,"abs_exp_date","has_abs_exp")!=""}checked{/if} onClick='abs_exp_select.toggle("abs_exp_date_input")'>
    {/addEditTD}

    {addEditTD type="left"}
	Absolute Expiration Date
    {/addEditTD}

    {addEditTD type="right"}
	{absDateSelect name="abs_exp_date" default_request="abs_exp_date" default_var="abs_exp_date" target="group"}
    {/addEditTD}

  {/viewTable}
<BR>
<script language="javascript">
	abs_exp_select=new DomContainer();
	abs_exp_select.disable_unselected=true;
	abs_exp_select.addByID("abs_exp_date_input",Array("abs_exp_date_unit"));
{if attrDefault($group_attrs,"abs_exp_date","has_abs_exp")!=""}
    abs_exp_select.select("abs_exp_date_input");
{else}
    abs_exp_select.select(null);
{/if}
</script>
