{attrUpdateMethod update_method="normalCharge"}

  {viewTable title="Internet Charge" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Internet Charge
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_normal_charge" value="t" class=checkbox {if attrDefault($group_attrs,"normal_charge","has_normal_charge")!=""}checked{/if} onClick='normal_charge_select.toggle("normal_charge")'>
    {/addEditTD}

    {addEditTD type="left"}
	Normal Charge
    {/addEditTD}

    {addEditTD type="right"}
	{charge_names_select name="normal_charge" type="Internet" target="group" default_var="normal_charge" default_request="normal_charge" id="normal_charge"}
    {/addEditTD}

  {/viewTable}
  <BR>
<script language="javascript">
	normal_charge_select=new DomContainer();
	normal_charge_select.disable_unselected=true;
	normal_charge_select.addByID("normal_charge");
{if attrDefault($group_attrs,"normal_charge","has_normal_charge")!=""}
    normal_charge_select.select("normal_charge");
{else}
    normal_charge_select.select(null);
{/if}
</script>

