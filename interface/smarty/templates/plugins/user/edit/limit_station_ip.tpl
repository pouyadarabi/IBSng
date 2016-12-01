{attrUpdateMethod update_method="limitStationIP"}
{userInfoTable title="Limit Station IP Address" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Station IP Address Limitation
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_limit_station_ip" value="t" class=checkbox {if attrDefault($user_attrs,"limit_station_ip","has_limit_station_ip")!=""}checked{/if} onClick='limit_station_ip_select.toggle("limit_station_ip")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="limit_station_ip" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left" comment=TRUE}
	Limit Station IP Address
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	<textarea name=limit_station_ip id=limit_station_ip class=text>{attrDefault target="user" default_var="limit_station_ip" default_request="limit_station_ip"|replace:",":",\n"}</textarea>
	{multistr form_name="user_edit" input_name="limit_station_ip"}
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="limit_station_ip"}
	    {$group_attrs.limit_station_ip|replace:",":"<br>"}
	{/ifHasAttr} 
	{helpicon subject="limit station ip address" category="user"}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	limit_station_ip_select=new DomContainer();
	limit_station_ip_select.disable_unselected=true;
	limit_station_ip_select.addByID("limit_station_ip");
{if attrDefault($user_attrs,"limit_station_ip","has_limit_station_ip")!=""}
    limit_station_ip_select.select("limit_station_ip");
{else}
    limit_station_ip_select.select(null);
{/if}
</script>