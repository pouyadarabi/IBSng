{attrUpdateMethod update_method="IPpool"}

  {viewTable title="IPpool" nofoot="TRUE"}
    {addEditTD type="left"}
	Has IPpool
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_ippool" value="t" class=checkbox {if attrDefault($group_attrs,"ippool","has_ippool")!=""}checked{/if} onClick='ippool_select.toggle("ippool")'>
    {/addEditTD}

    {addEditTD type="left"}
	IPpool Name
    {/addEditTD}

    {addEditTD type="right"}
	{ippool_names_select name="ippool" target="group" default_var="ippool" default_request="ippool" id="ippool"}
    {/addEditTD}

  {/viewTable}
  <BR>
<script language="javascript">
	ippool_select=new DomContainer();
	ippool_select.disable_unselected=true;
	ippool_select.addByID("ippool");
{if attrDefault($group_attrs,"ippool","has_ippool")!=""}
    ippool_select.select("ippool");
{else}
    ippool_select.select(null);
{/if}
</script>


