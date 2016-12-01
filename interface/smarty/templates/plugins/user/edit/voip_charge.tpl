{attrUpdateMethod update_method="voipCharge"}
{userInfoTable title="VoIP Charge" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has VoIP charge
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_voip_charge" value="t" class=checkbox {if attrDefault($user_attrs,"voip_charge","has_voip_charge")!=""}checked{/if} onClick='voip_charge_select.toggle("voip_charge")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="voip_charge" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
	{helpicon subject="voip charge" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    VoIP Charge
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{charge_names_select name="voip_charge" type="VoIP" target="user" default_var="voip_charge" default_request="voip_charge" id="voip_charge"}
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="voip_charge"}
		    {$group_attrs.voip_charge}  
		{/ifHasAttr} 
		{helpicon subject="voip charge" category="user"}
    {/userInfoTD}

{/userInfoTable}
<br>
<script language="javascript">
	voip_charge_select=new DomContainer();
	voip_charge_select.disable_unselected=true;
	voip_charge_select.addByID("voip_charge");
{if attrDefault($user_attrs,"voip_charge","has_voip_charge")!=""}
    voip_charge_select.select("voip_charge");
{else}
    voip_charge_select.select(null);
{/if}
</script>