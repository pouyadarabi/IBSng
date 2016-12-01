{attrUpdateMethod update_method="normalAttrs"}
{viewTable title="Internet Username and Password" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	Has Internet Username
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_normal_username" value="t" class=checkbox {if attrDefault($user_attrs,"normal_username","has_normal_username")!=""}checked{/if} onClick='normal_select.toggle("normal_username")'>
    {/addEditTD}

    {addEditTD type="left"}
	Internet Username
    {/addEditTD}

    {addEditTD type="right"}
	<input type=hidden name=current_normal_username value='{attrDefault target="user" default_var="normal_username" default_request="current_normal_username"}'>
	<input id="normal_username" type=text  class=text name="normal_username" 
	    value="{attrDefault target="user" default_var="normal_username" default_request="normal_username"}" 
	    onChange="updateUserAddCheckImage('normal','{attrDefault target="user" default_var="normal_username" default_request="current_normal_username"}',0);" 
	    onKeyUp="updateUserAddCheckImage('normal','{attrDefault target="user" default_var="normal_username" default_request="current_normal_username"}',1);"
	> 
	{multistr form_name="user_edit" input_name="normal_username"}
	{helpicon subject="normal username" category="user"}
	<a href="#" onClick="showUserAddCheckWindow('normal','{attrDefault target="user" default_var="normal_username" default_request="normal_username"}');">
	    <img border=0 name="normal_user_exists" src="/IBSng/admin/user/check_user_for_add.php?image=t&username=&type=normal&current_username=" title="Users Exist">
	</a>
	<script language=javascript>
	    updateUserAddCheckImage('normal','{attrDefault target="user" default_var="normal_username" default_request="current_normal_username"}',1);
	</script>
    {/addEditTD}

    {addEditTD type="left"}
	Generate Password
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox id="generate_password" name="generate_password" value="t" class=checkbox {ifisinrequest name="generate_password" value="checked" } onClick='normalGeneratePasswordOnClick(this);'>
	{helpicon subject="generate password" category="user"}
    {/addEditTD}

    {addEditTD type="left" id="password_char_tr"}
	Password Includes
    {/addEditTD}

    {addEditTD type="right"}
	Character <input type=checkbox class=checkbox name="password_character" id="password_character" value="t" {ifisinrequest name="password_character" value="checked" default="checked"}> 
	Digit <input type=checkbox class=checkbox name="password_digit" id="password_digit" value="t" {ifisinrequest name="password_digit" value="checked" default="checked"}> 
	{helpicon subject="password characters" category="user"}
    {/addEditTD}

    {addEditTD type="left" id="password_len_tr"}
	Generated Password Length
    {/addEditTD}

    {addEditTD type="right"}
	<input type=text id="password_len" name="password_len" value="{ifisinrequest name="password_len" default="6"}" class=small_text>
	{helpicon subject="password length" category="user"}
    {/addEditTD}

    {addEditTD type="left" id="password_tr"}
	Password
    {/addEditTD}

    {addEditTD type="right"}
	<input type=text id="password" name="password" value="{attrDefault target="user" default_var="normal_password" default_request="password"}" class=text>
	{multistr form_name="user_edit" input_name="password"}
	{helpicon subject="password" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	Save In List<font size=1>[Usernames/Passwords]</font>
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="normal_save_user_add" id="normal_save_user_add" value="t" class=checkbox {ifisinrequest name="normal_save_user_add" value="checked"}>
	{helpicon subject="save username and password" category="user"}
    {/addEditTD}
{/viewTable}
{viewTable title="Upload Internet Username and Password From File" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	Upload Internet Usernames from file
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_normal_username_from_file" value="t" class=checkbox onClick='return normalUploadChanged(this)'>
    {/addEditTD}

    {addEditTD type="left"}
	File (Format: Username,Password)
    {/addEditTD}

    {addEditTD type="right"}
        <input type=file name="normal_username_from_file" class=text id="normal_username_from_file" size=15>
    {/addEditTD}
{/viewTable}
<br>




<script language="javascript">
	normal_select=new DomContainer();
	normal_select.disable_unselected=true;
	normal_select.addByID("normal_username",new Array("generate_password","password","password_len","password_character","password_digit","normal_save_user_add"));
{if attrDefault($user_attrs,"normal_username","has_normal_username")!=""}
    normal_select.select("normal_username");
{else}
    normal_select.select(null);
{/if}

	normal_from_file_select=new DomContainer();
	normal_from_file_select.disable_unselected=true;
	normal_from_file_select.addByID("normal_username_from_file",[]);
	normal_from_file_select.select(null);

	generate_password=new DomContainer();
	generate_password.addByID("password_tr",[]);
	generate_password.addByID("password_char_tr",new Array("password_len_tr"));
	generate_password.setOnSelect("display","");
	generate_password.setOnUnSelect("display","none");	
{if isInRequest("generate_password")}
	generate_password.select("password_char_tr");
{else}
	generate_password.select("password_tr");	
{/if}

{literal}

function normalUploadChanged(obj)
{
    if(document.user_edit.has_normal_username.checked)
    {
	alert("Please turn off Has Internet Username first");
	return false;
    }
    normal_from_file_select.toggle("normal_username_from_file");
    return true;
}

function normalGeneratePasswordOnClick(obj)
{
    if(obj.checked)
    {
	generate_password.select("password_char_tr");
	document.user_edit.normal_save_user_add.checked=true;
    }
    else
	generate_password.select("password_tr");
}
{/literal}
</script>