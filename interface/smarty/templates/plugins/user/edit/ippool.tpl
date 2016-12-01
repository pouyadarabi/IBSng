{attrUpdateMethod update_method="IPpool"}
{userInfoTable title="IP Pool" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has IPpool
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_ippool" value="t" class=checkbox {if attrDefault($user_attrs,"ippool","has_ippool")!=""}checked{/if} onClick='ippool_select.toggle("ippool")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="ippool" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	IPpool
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{ippool_names_select name="ippool" target="user" default_var="ippool" default_request="ippool" id="ippool"}
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="ippool"}
	    {$group_attrs.ippool}  
	{/ifHasAttr} 
	{helpicon subject="ippool" category="user"}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	ippool_select=new DomContainer();
	ippool_select.disable_unselected=true;
	ippool_select.addByID("ippool");
{if attrDefault($user_attrs,"ippool","has_ippool")!=""}
    ippool_select.select("ippool");
{else}
    ippool_select.select(null);
{/if}
</script>