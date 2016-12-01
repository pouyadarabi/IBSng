{* User Login Page


*}

{include file="stripped_header.tpl" title="User Login"}

<!-- Main Table -->
<table border="0" cellspacing="0" cellpadding="0" class="Main_Page">
	<tr>
		<td align="center">		
    {include file="err_head.tpl"}

    <form method=POST action="/IBSng/user/">
        {addEditTable title="Internet User Login"}
	{addEditTD type="left"}
	    Internet Username
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=text name=normal_username class=text>
	{/addEditTD}

	{addEditTD type="left"}
	    Internet Password
	{/addEditTD}

	{addEditTD type="right"}
    	    <input class=text type=password name=normal_password>
	{/addEditTD}

	{addEditTD type="left"}
	    Language
	{/addEditTD}

	{addEditTD type="right"}
    	    {languageSelect}
	{/addEditTD}

    {/addEditTable}
    </form>

    <form method=POST action="/IBSng/user/">
        {addEditTable title="VoIP User Login"}
	{addEditTD type="left"}
	    VoIP Username
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=text name=voip_username class=text>
	{/addEditTD}

	{addEditTD type="left"}
	    VoIP Password
	{/addEditTD}

	{addEditTD type="right"}
    	    <input class=text type=password name=voip_password>
	{/addEditTD}

	{addEditTD type="left"}
	    Language
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