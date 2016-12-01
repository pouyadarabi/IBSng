{viewTable title="Basic User Informations" table_width="100%" nofoot="TRUE"} 

    {addEditTD type="left"}
	User ID
    {/addEditTD}

    {addEditTD type="right"}
	{$user_info.basic_info.user_id}
    {/addEditTD}

    {addEditTD type="left"}
	Credit
    {/addEditTD}

    {addEditTD type="right"}
	{$user_info.basic_info.credit|price} <a class="link_in_body" href="change_credit.php?user_id={$user_id|escape:"url"}">Change Credit</a>
    {/addEditTD}

    {addEditTD type="left"}
	{if $can_change} {editCheckBox edit_tpl_name="group_name"} {/if}
	Group
    {/addEditTD}

    {addEditTD type="right"}
        <a href="/IBSng/admin/group/group_info.php?group_name={$user_info.basic_info.group_name|escape:"url"}" class="link_in_body_black">
	    {$user_info.basic_info.group_name}
	</a>
    {/addEditTD}

    {addEditTD type="left"}
	{if $can_change and canDo("CHANGE USERS OWNER")} {editCheckBox edit_tpl_name="owner_name"} {/if}
	Owner Admin
    {/addEditTD}

    {addEditTD type="right"}
	{$user_info.basic_info.owner_name}
    {/addEditTD}
  
    {addEditTD type="left"}
	Creation Date
    {/addEditTD}

    {addEditTD type="right"}
	{$user_info.basic_info.creation_date}
    {/addEditTD}

    {addEditTD type="left"}
	Status
    {/addEditTD}

    {addEditTD type="right"}
	{if $user_info.online_status }
	    Online
	{else}
	    Offline
	{/if}
    {/addEditTD}

    
{/viewTable}
