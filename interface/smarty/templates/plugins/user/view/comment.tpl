{viewTable title="Comment" nofoot="TRUE" table_width="100%"}
    {addEditTD type="left" comment=TRUE}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="comment"} {/if}
	    Comment
	{/strip}
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
	{ifHasAttr object="user" var_name="comment"}
	    {$user_attrs.comment|nl2br|wordwrap:40:"<br />":true}
	{/ifHasAttr} 
	{helpicon subject="comment" category="user"}
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="name"} {/if}
	    Name
	{/strip}
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
	{ifHasAttr object="user" var_name="name"}
	    {$user_attrs.name|nl2br|wordwrap:40:"<br />":true}
	{/ifHasAttr} 
	{helpicon subject="Name" category="user"}
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="phone"} {/if}
	    Phone
	{/strip}
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
	{ifHasAttr object="user" var_name="phone"}
	    {$user_attrs.phone|nl2br|wordwrap:40:"<br />":true}
	{/ifHasAttr} 
	{helpicon subject="phone" category="user"}
    {/addEditTD}

{/viewTable}

