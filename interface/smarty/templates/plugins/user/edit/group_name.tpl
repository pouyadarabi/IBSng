{attrUpdateMethod update_method="groupName"}

{viewTable title="Group Name" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	Group Name
    {/addEditTD}

    {addEditTD type="right"}
	{if $single_user}
	    {group_names_select name="group_name" default=`$user_info.basic_info.group_name` default_request="group_name"}
	{else}
	    {group_names_select name="group_name" default_request="group_name"}
	{/if}
    {/addEditTD}
{/viewTable}
<br>