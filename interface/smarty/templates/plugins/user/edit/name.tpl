{attrUpdateMethod update_method="name"}
{viewTable title="Name" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	Has Name
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_name" value="t" class=checkbox {if attrDefault($user_attrs,"name","has_name")!=""}checked{/if} onClick='name_select.toggle("name")'>
    {/addEditTD}

    {addEditTD type="left" name=TRUE}
	Name
    {/addEditTD}

    {addEditTD type="right" name=TRUE}
	<textarea name=name id=name class=text>{attrDefault target="user" default_var="name" default_request="name"}</textarea>
	{helpicon subject="name" category="user"}
    {/addEditTD}

{/viewTable}
<script language="javascript">
	name_select=new DomContainer();
	name_select.disable_unselected=true;
	name_select.addByID("name");
{if attrDefault($user_attrs,"name","has_name")!=""}
    name_select.select("name");
{else}
    name_select.select(null);
{/if}
</script>