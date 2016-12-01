{attrUpdateMethod update_method="persistentLan"}
{viewTable title="Persistent Lan" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	Has Persistent Lan
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_plan" value="t" class=checkbox {if attrDefault($user_attrs,"persistent_lan_mac","has_plan")!=""}checked{/if} onClick='plan_select.toggle("persistent_lan_mac")'>
    {/addEditTD}

    {addEditTD type="left"}
	Persistent Lan Mac
    {/addEditTD}

    {addEditTD type="right"}
	<input id="persistent_lan_mac" type=text  class=text name="persistent_lan_mac" 
	    value="{attrDefault target="user" default_var="persistent_lan_mac" default_request="persistent_lan_mac"}" > 
	{multistr form_name="user_edit" input_name="persistent_lan_mac"}
	{helpicon subject="persistent lan mac" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Persistent Lan IP
    {/addEditTD}

    {addEditTD type="right"}
	<input id="persistent_lan_ip" type=text  class=text name="persistent_lan_ip" 
	    value="{attrDefault target="user" default_var="persistent_lan_ip" default_request="persistent_lan_ip"}" > 
	{multistr form_name="user_edit" input_name="persistent_lan_ip"}
	{helpicon subject="persistent lan ip" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Persistent Lan Ras IP
    {/addEditTD}

    {addEditTD type="right"}
	{ras_ips_select id="persistent_lan_ras_ip" name="persistent_lan_ras_ip" target="user" default_var="persistent_lan_ras_ip" default_request="persistent_lan_ras_ip"}
	{helpicon subject="persistent lan ras ip" category="user"}
    {/addEditTD}
{/viewTable}
<br>
<script language="javascript">
	plan_select=new DomContainer();
	plan_select.disable_unselected=true;
	plan_select.addByID("persistent_lan_mac",new Array("persistent_lan_ip","persistent_lan_ras_ip"));
{if attrDefault($user_attrs,"persistent_lan_mac","has_plan")!=""}
    plan_select.select("persistent_lan_mac");
{else}
    plan_select.select(null);
{/if}
</script>