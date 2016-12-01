{* User Login Page


*}

{include file="stripped_header.tpl" title="ورود به سیستم"}

<!-- Main Table -->
<table border="0" cellspacing="0" cellpadding="0" class="Main_Page">
	<tr>
		<td align="center">		
    {include file="err_head.tpl"}

    <form method=POST action="/IBSng/user/">
        {addEditTable title="ورود کاربران اینترنتی"}
	{addEditTD type="left"}
	    نام کاربر
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=text name=normal_username class=text>
	{/addEditTD}

	{addEditTD type="left"}
	    رمز عبور
	{/addEditTD}

	{addEditTD type="right"}
    	    <input class=text type=password name=normal_password>
	{/addEditTD}

	{addEditTD type="left"}
	    زبان
	{/addEditTD}

	{addEditTD type="right"}
    	    {languageSelect}
	{/addEditTD}

    {/addEditTable}
    </form>

    <form method=POST action="/IBSng/user/">
        {addEditTable title="VoIP ورود کاربران"}
	{addEditTD type="left"}
	    نام کاربر
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=text name=voip_username class=text>
	{/addEditTD}

	{addEditTD type="left"}
	    رمز عبور
	{/addEditTD}

	{addEditTD type="right"}
    	    <input class=text type=password name=voip_password>
	{/addEditTD}

	{addEditTD type="left"}
	    زبان
 	{/addEditTD}

	{addEditTD type="right"}
    	    {languageSelect}
	{/addEditTD}
    {/addEditTable}
    </form>
    
	</td>
</tr>
</table>
<!-- End Main Table -->


{include file="stripped_footer.tpl"}