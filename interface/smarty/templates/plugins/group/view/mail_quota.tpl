{viewTable title="Mailbox" nofoot="TRUE"}
    {addEditTD type="left"}
	{if $can_change}{editCheckBox edit_tpl_name="mail_quota"}{/if} Mailbox Quota
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="mail_quota"}
	    {$group_attrs.mail_quota|byte}
	{/ifHasAttr} 
	{helpicon subject="has mailbox" category="user"}
    {/addEditTD}

{/viewTable}
