{viewTable title="Mailbox" nofoot="TRUE" table_width="100%"}
    {addEditTD type="left" comment=TRUE}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="email_address"} {/if}
	    Has MailBox
	{/strip}
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
	{ifHasAttr object="user" var_name="email_address" alternate="No"}
	    Yes 
	{/ifHasAttr} 
    {/addEditTD}
    
    {addEditTD type="left" comment=TRUE}
	Email Address
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
	{ifHasAttr object="user" var_name="email_address"}
	    {$user_attrs.email_address}
	{/ifHasAttr} 
	{helpicon subject="email address" category="user"}
    {/addEditTD}
{/viewTable}

