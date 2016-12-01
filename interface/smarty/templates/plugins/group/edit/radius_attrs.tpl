{attrUpdateMethod update_method="radiusAttrs"}

  {viewTable title="Radius Attributes" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Radius Attributes
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_radius_attrs" value="t" class=checkbox {if attrDefault($group_attrs,"radius_attrs","has_radius_attrs")!=""}checked{/if} onClick='radius_attrs_select.toggle("radius_attrs")'>
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Radius Attrs(x="y")
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	<textarea name=radius_attrs id=radius_attrs>{attrDefault target="group" default_var="radius_attrs" default_request="radius_attrs"}</textarea>
    {/addEditTD}

  {/viewTable}
<script language="javascript">
	radius_attrs_select=new DomContainer();
	radius_attrs_select.disable_unselected=true;
	radius_attrs_select.addByID("radius_attrs");
{if attrDefault($group_attrs,"radius_attrs","has_radius_attrs")!=""}
    radius_attrs_select.select("radius_attrs");
{else}
    radius_attrs_select.select(null);
{/if}
</script>


