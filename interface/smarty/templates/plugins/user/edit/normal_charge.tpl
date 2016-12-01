{attrUpdateMethod update_method="normalCharge"}
{userInfoTable title="Internet Charge" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Internet charge
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_normal_charge" value="t" class=checkbox {if attrDefault($user_attrs,"normal_charge","has_normal_charge")!=""}checked{/if} onClick='normal_charge_select.toggle("normal_charge")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="normal_charge" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
	{helpicon subject="normal charge" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Normal Charge
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{charge_names_select name="normal_charge" type="Internet" target="user" default_var="normal_charge" default_request="normal_charge" id="normal_charge"}
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="normal_charge"}
		    {$group_attrs.normal_charge}  
		{/ifHasAttr} 
		{helpicon subject="normal charge" category="user"}
    {/userInfoTD}

{/userInfoTable}
<br>
<script language="javascript">
	normal_charge_select=new DomContainer();
	normal_charge_select.disable_unselected=true;
	normal_charge_select.addByID("normal_charge");
{if attrDefault($user_attrs,"normal_charge","has_normal_charge")!=""}
    normal_charge_select.select("normal_charge");
{else}
    normal_charge_select.select(null);
{/if}
</script>