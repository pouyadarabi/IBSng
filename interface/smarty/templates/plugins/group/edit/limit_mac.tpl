{attrUpdateMethod update_method="limitMac"}

  {viewTable title="Limit Mac Address" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Mac Address Limitation
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_limit_mac" value="t" class=checkbox {if attrDefault($group_attrs,"limit_mac","has_limit_mac")!=""}checked{/if} onClick='limit_mac_select.toggle("limit_mac")'>
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Limit Mac Address
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	<textarea name=limit_mac id=limit_mac>{attrDefault target="group" default_var="limit_mac" default_request="limit_mac"}</textarea>
	{multistr form_name="group_edit" input_name="limit_mac"}
    {/addEditTD}

  {/viewTable}
<script language="javascript">
	limit_mac_select=new DomContainer();
	limit_mac_select.disable_unselected=true;
	limit_mac_select.addByID("limit_mac");
{if attrDefault($group_attrs,"limit_mac","has_limit_mac")!=""}
    limit_mac_select.select("limit_mac");
{else}
    limit_mac_select.select(null);
{/if}
</script>


