{attrUpdateMethod update_method="ownerName"}
{viewTable title="Owner Name" nofoot="TRUE" table_width="380"} 
    {addEditTD type="left"}
	Owner Admin
    {/addEditTD}

    {addEditTD type="right"}
	{if $single_user}
    		{admin_names_select name="owner_name" default=`$user_info.basic_info.owner_name` default_request="owner_name"}
	{else}
		{admin_names_select name="owner_name" default_request="owner_name"}	    
	{/if}
    {/addEditTD}

{/viewTable}
<br>
