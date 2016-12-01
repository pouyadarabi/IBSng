{viewTable title="User  Information" table_width="380" nofoot="TRUE"}

    {addEditTD type="left" comment=TRUE}
	User ID
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
      <form name="user_id_header">
	{$user_id|replace:",":", "} {multistr form_name="user_id_header" input_name="user_id"}
	<input type=hidden name="user_id" value="{$user_id}">
      </form>
	
    {/addEditTD}

{/viewTable}
