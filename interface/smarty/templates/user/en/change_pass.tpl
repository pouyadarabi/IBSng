{* Change Password

*}

{include file="user_header.tpl" title="Change Password" selected="change_pass"}
{include file="err_head.tpl"}

{headerMsg var_name="normal_change_success"}
    Internet Password for {$user_attrs.normal_username} Changed Successfully
{/headerMsg}

{headerMsg var_name="voip_change_success"}
    VoIP Password for {$user_attrs.voip_username} Changed Successfully
{/headerMsg}

{if array_key_exists("normal_username",$user_attrs) }
    <form method=POST>

    {addEditTable title="Change Internet Password"}
	{addEditTD type="left"}
	    Internet Username
	{/addEditTD}
	{addEditTD type="right"}
	    {$user_attrs.normal_username} 
	{/addEditTD}

	{addEditTD type="left"}
	    Old Internet Password
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="old_normal_password">
	{/addEditTD}

	{addEditTD type="left"}
	    New Internet Password
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="new_normal_password1">
	{/addEditTD}

	{addEditTD type="left"}
	    Confirm New Internet Password
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="new_normal_password2">
	{/addEditTD}
    {/addEditTable}
    </form>
{/if}

{if array_key_exists("voip_username",$user_attrs) }
    <form method=POST>
    {addEditTable title="Change VoIP Password"}
	{addEditTD type="left"}
	    VoIP Username
	{/addEditTD}
	{addEditTD type="right"}
	    {$user_attrs.voip_username} 
	{/addEditTD}

	{addEditTD type="left"}
	    Old VoIP Password
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="old_voip_password">
	{/addEditTD}

	{addEditTD type="left"}
	    New VoIP Password
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="new_voip_password1">
	{/addEditTD}

	{addEditTD type="left"}
	    Confirm New VoIP Password
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="new_voip_password2">
	{/addEditTD}
    {/addEditTable}
    </form>
{/if}

{include file="user_footer.tpl"}