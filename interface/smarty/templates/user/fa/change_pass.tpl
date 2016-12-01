{* Change Password

*}

{include file="user_header.tpl" title="تغییر رمز عبور" selected="change_pass"}
{include file="err_head.tpl"}

{headerMsg var_name="normal_change_success"}
    Internet Password for {$user_attrs.normal_username} Changed Successfully
{/headerMsg}

{headerMsg var_name="voip_change_success"}
    VoIP Password for {$user_attrs.voip_username} Changed Successfully
{/headerMsg}

{if array_key_exists("normal_username",$user_attrs) }
    <form method=POST>

    {addEditTable title="تغییر رمز عبور کاربران اینترنتی"}
	{addEditTD type="left"}
	    نام کاربر
	{/addEditTD}
	{addEditTD type="right"}
	    {$user_attrs.normal_username} 
	{/addEditTD}

	{addEditTD type="left"}
	    رمز عبور قدیم
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="old_normal_password">
	{/addEditTD}

	{addEditTD type="left"}
	    رمز عبور جدید
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="new_normal_password1">
	{/addEditTD}

	{addEditTD type="left"}
	    تایید رمز عبور جدید
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="new_normal_password2">
	{/addEditTD}
    {/addEditTable}
    </form>
{/if}

{if array_key_exists("voip_username",$user_attrs) }
    <form method=POST>
    {addEditTable title="تغییر رمز عبورکاربران VoIP"}
	{addEditTD type="left"}
	    نام کاربر
	{/addEditTD}
	{addEditTD type="right"}
	    {$user_attrs.voip_username} 
	{/addEditTD}

	{addEditTD type="left"}
	    رمزعبورقدیم
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="old_voip_password">
	{/addEditTD}

	{addEditTD type="left"}
	    رمز عبور جدید
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="new_voip_password1">
	{/addEditTD}

	{addEditTD type="left"}
	    تایید رمز عبور جدید
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=password class=text name="new_voip_password2">
	{/addEditTD}
    {/addEditTable}
    </form>
{/if}

{include file="user_footer.tpl"}
