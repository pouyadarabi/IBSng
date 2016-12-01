{attrUpdateMethod update_method="phone"}
{viewTable title="Phone" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	Has Phone
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_phone" value="t" class=checkbox {if attrDefault($user_attrs,"phone","has_phone")!=""}checked{/if} onClick='phone_select.toggle("phone")'>
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Phone
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	<textarea name=phone id=phone class=text>{attrDefault target="user" default_var="phone" default_request="phone"}</textarea>
	{helpicon subject="phone" category="user"}
    {/addEditTD}

{/viewTable}
<script language="javascript">
	phone_select=new DomContainer();
	phone_select.disable_unselected=true;
	phone_select.addByID("phone");
{if attrDefault($user_attrs,"phone","has_phone")!=""}
    phone_select.select("phone");
{else}
    phone_select.select(null);
{/if}
</script>