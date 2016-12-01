{* Admin Login Page


*}
{include file="stripped_header.tpl" title="Admin Login"}


<!-- Main Table -->
<table border="0" cellspacing="0" cellpadding="0" class="Main_Page">
	<tr>
		<td align="center">		
    {include file="err_head.tpl"}

<div id="non_secure_message" style="display: none">
{headerMsg}
    You are currently using an insecure connection. To establish a secure connection please click <a href="#" id="secure_link" class="link_in_body">Here</a>.
{/headerMsg}

</div>

    <form method=POST action="/IBSng/admin/">
        {addEditTable title="Admin Login"}
	{addEditTD type="left"}
	    Username
	{/addEditTD}
	{addEditTD type="right"}
	    <input type=text name=username class=text>
	{/addEditTD}

	{addEditTD type="left"}
	    Password
	{/addEditTD}

	{addEditTD type="right"}
    	    <input class=text type=password name=password>
	{/addEditTD}

    {/addEditTable}
    {if isInRequest("target")}
	<input type=hidden name=target value={$smarty.request.target}>
    {/if}
    </form>
	</td>
</tr>
</table>
<!-- End Main Table -->

{literal}
<script language="javascript">
    if(window.location.protocol != "https:")
    {
	document.getElementById('non_secure_message').style.display = "";
	document.getElementById('secure_link').href = "https://"+ window.location.hostname + window.location.pathname + window.location.search;
    }
</script>
{/literal}

{include file="stripped_footer.tpl"}