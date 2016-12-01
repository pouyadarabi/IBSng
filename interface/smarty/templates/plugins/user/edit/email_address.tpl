{attrUpdateMethod update_method="emailAddress"}
{viewTable title="Mailbox" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	Has Mailbox
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_email_address" value="t" class=checkbox {if attrDefault($user_attrs,"email_address","has_email_address")!=""}checked{/if} onClick='email_address_select.toggle("email_address")'>
	{helpicon subject="email_address" category="user"}
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Email Address
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	<input name="email_address" id="email_address" class=text value="{attrDefault target="user" default_var="email_address" default_request="email_address"}">
    {/addEditTD}
{/viewTable}
<script language="javascript">
	email_address_select=new DomContainer();
	email_address_select.disable_unselected=true;
	email_address_select.addByID("email_address");
{if attrDefault($user_attrs,"email_address","has_email_address")!=""}
    email_address_select.select("email_address");
{else}
    email_address_select.select(null);
{/if}
</script>