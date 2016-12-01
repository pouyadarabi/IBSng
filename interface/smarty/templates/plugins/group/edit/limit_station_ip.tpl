{attrUpdateMethod update_method="limitStationIP"}

  {viewTable title="Limit Station IP Address" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Station IP Address Limitation
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_limit_station_ip" value="t" class=checkbox {if attrDefault($group_attrs,"limit_station_ip","has_limit_station_ip")!=""}checked{/if} onClick='limit_station_ip_select.toggle("limit_station_ip")'>
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Limit Station IP Address
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	<textarea name=limit_station_ip id=limit_station_ip>{attrDefault target="group" default_var="limit_station_ip" default_request="limit_station_ip"}</textarea>
	{multistr form_name="group_edit" input_name="limit_station_ip"}
    {/addEditTD}

  {/viewTable}
<script language="javascript">
	limit_station_ip_select=new DomContainer();
	limit_station_ip_select.disable_unselected=true;
	limit_station_ip_select.addByID("limit_station_ip");
{if attrDefault($group_attrs,"limit_station_ip","has_limit_station_ip")!=""}
    limit_station_ip_select.select("limit_station_ip");
{else}
    limit_station_ip_select.select(null);
{/if}
</script>


