{attrUpdateMethod update_method="voipCharge"}

  {viewTable title="VoIP Charge" nofoot="TRUE"}
    {addEditTD type="left"}
	Has VoIP Charge
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_voip_charge" value="t" class=checkbox {if attrDefault($group_attrs,"voip_charge","has_voip_charge")!=""}checked{/if} onClick='voip_charge_select.toggle("voip_charge")'>
    {/addEditTD}

    {addEditTD type="left"}
	VoIp Charge
    {/addEditTD}

    {addEditTD type="right"}
	{charge_names_select name="voip_charge" type="VoIP" target="group" default_var="voip_charge" default_request="voip_charge" id="voip_charge"}
    {/addEditTD}

  {/viewTable}
  <BR>
<script language="javascript">
	voip_charge_select=new DomContainer();
	voip_charge_select.disable_unselected=true;
	voip_charge_select.addByID("voip_charge");
{if attrDefault($group_attrs,"voip_charge","has_voip_charge")!=""}
    voip_charge_select.select("voip_charge");
{else}
    voip_charge_select.select(null);
{/if}
</script>

